# -*- coding: utf-8 -*-
"""
database.py
===========
Couche d'accès aux données (DAL - Data Access Layer).

Ce module encapsule TOUTES les interactions avec la base MySQL. Aucune
requête SQL ne doit être écrite ailleurs dans le projet : cela centralise
la logique, facilite la maintenance et limite la surface d'attaque par
injection SQL (toutes les requêtes sont paramétrées).

On utilise un gestionnaire de contexte (`with`) pour garantir la fermeture
systématique des connexions, même en cas d'exception.
"""

from contextlib import contextmanager
from datetime import datetime

from config import config
from modules.logger import get_logger

logger = get_logger("database")

# Pool de connexions : réutiliser les connexions est bien plus performant
# que d'en ouvrir une nouvelle à chaque requête (gain mesurable sous charge).
_pool = None


def init_pool():
    """Initialise le pool de connexions MySQL (appelé une seule fois).

    L'import du connecteur est différé ici (lazy import) afin que les modules
    métier restent importables — et donc testables — même sur une machine où
    le driver MySQL n'est pas installé.
    """
    global _pool
    if _pool is None:
        from mysql.connector import pooling  # import différé
        _pool = pooling.MySQLConnectionPool(
            pool_name="supervision_pool",
            pool_size=5,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            charset="utf8mb4",
        )
        logger.info("Pool de connexions MySQL initialisé (taille=5).")
    return _pool


@contextmanager
def get_connection():
    """Fournit une connexion issue du pool, refermée automatiquement."""
    pool = init_pool()
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()  # Rend la connexion au pool plutôt que de la détruire.


# ---------------------------------------------------------------------- #
# Opérations sur la table « equipements »                                #
# ---------------------------------------------------------------------- #
def get_all_equipements(actifs_seulement: bool = True):
    """Retourne la liste des équipements à superviser."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM equipements"
        if actifs_seulement:
            sql += " WHERE actif = 1"
        sql += " ORDER BY nom"
        cursor.execute(sql)
        return cursor.fetchall()


def get_equipement(equipement_id: int):
    """Retourne un équipement par son identifiant."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM equipements WHERE id = %s", (equipement_id,)
        )
        return cursor.fetchone()


def add_equipement(nom, adresse_ip, type_equipement, emplacement="", actif=1):
    """Ajoute un nouvel équipement. Requête paramétrée (anti-injection SQL)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO equipements (nom, adresse_ip, type_equipement,
                   emplacement, actif)
               VALUES (%s, %s, %s, %s, %s)""",
            (nom, adresse_ip, type_equipement, emplacement, actif),
        )
        conn.commit()
        return cursor.lastrowid


def update_statut_equipement(equipement_id, statut, latence_ms=None):
    """Met à jour le statut courant et la date de dernière vérification."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE equipements
               SET statut = %s, latence_ms = %s, derniere_verification = %s
               WHERE id = %s""",
            (statut, latence_ms, datetime.now(), equipement_id),
        )
        conn.commit()


def delete_equipement(equipement_id):
    """Supprime un équipement (les journaux/alertes liés sont supprimés en CASCADE)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM equipements WHERE id = %s", (equipement_id,))
        conn.commit()


# ---------------------------------------------------------------------- #
# Opérations sur la table « journaux »                                   #
# ---------------------------------------------------------------------- #
def add_journal(equipement_id, statut, latence_ms, message=""):
    """Enregistre une ligne d'historique pour chaque vérification effectuée."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO journaux (equipement_id, statut, latence_ms,
                   message, date_evenement)
               VALUES (%s, %s, %s, %s, %s)""",
            (equipement_id, statut, latence_ms, message, datetime.now()),
        )
        conn.commit()


def get_journaux(limit=100, equipement_id=None):
    """Retourne l'historique des vérifications (récent d'abord)."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        if equipement_id:
            cursor.execute(
                """SELECT j.*, e.nom, e.adresse_ip
                   FROM journaux j JOIN equipements e ON e.id = j.equipement_id
                   WHERE j.equipement_id = %s
                   ORDER BY j.date_evenement DESC LIMIT %s""",
                (equipement_id, limit),
            )
        else:
            cursor.execute(
                """SELECT j.*, e.nom, e.adresse_ip
                   FROM journaux j JOIN equipements e ON e.id = j.equipement_id
                   ORDER BY j.date_evenement DESC LIMIT %s""",
                (limit,),
            )
        return cursor.fetchall()


# ---------------------------------------------------------------------- #
# Opérations sur la table « alertes »                                    #
# ---------------------------------------------------------------------- #
def add_alerte(equipement_id, type_alerte, severite, message, canal):
    """Crée une alerte et retourne son identifiant."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO alertes (equipement_id, type_alerte, severite,
                   message, canal, date_alerte, acquittee)
               VALUES (%s, %s, %s, %s, %s, %s, 0)""",
            (equipement_id, type_alerte, severite, message, canal, datetime.now()),
        )
        conn.commit()
        return cursor.lastrowid


def get_alertes(limit=100, non_acquittees=False):
    """Retourne les alertes (option : uniquement non acquittées)."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT a.*, e.nom, e.adresse_ip
                 FROM alertes a JOIN equipements e ON e.id = a.equipement_id"""
        if non_acquittees:
            sql += " WHERE a.acquittee = 0"
        sql += " ORDER BY a.date_alerte DESC LIMIT %s"
        cursor.execute(sql, (limit,))
        return cursor.fetchall()


def acquitter_alerte(alerte_id):
    """Marque une alerte comme traitée par un administrateur."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alertes SET acquittee = 1, date_acquittement = %s WHERE id = %s",
            (datetime.now(), alerte_id),
        )
        conn.commit()


def derniere_alerte_active(equipement_id, type_alerte):
    """Vérifie s'il existe déjà une alerte non acquittée du même type.

    Sert à éviter le « spam » d'alertes : on n'alerte qu'une fois par panne,
    tant que l'administrateur n'a pas acquitté ou que l'équipement n'est pas
    revenu en ligne.
    """
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM alertes
               WHERE equipement_id = %s AND type_alerte = %s AND acquittee = 0
               ORDER BY date_alerte DESC LIMIT 1""",
            (equipement_id, type_alerte),
        )
        return cursor.fetchone()


# ---------------------------------------------------------------------- #
# Statistiques (pour le tableau de bord)                                 #
# ---------------------------------------------------------------------- #
def get_statistiques():
    """Calcule les indicateurs clés affichés sur le tableau de bord."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        stats = {}

        cursor.execute("SELECT COUNT(*) AS total FROM equipements WHERE actif = 1")
        stats["total_equipements"] = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS up FROM equipements WHERE statut = 'UP' AND actif = 1"
        )
        stats["equipements_up"] = cursor.fetchone()["up"]

        cursor.execute(
            "SELECT COUNT(*) AS down FROM equipements WHERE statut = 'DOWN' AND actif = 1"
        )
        stats["equipements_down"] = cursor.fetchone()["down"]

        cursor.execute("SELECT COUNT(*) AS a FROM alertes WHERE acquittee = 0")
        stats["alertes_actives"] = cursor.fetchone()["a"]

        # Taux de disponibilité global = UP / total * 100
        total = stats["total_equipements"] or 1  # évite la division par zéro
        stats["taux_disponibilite"] = round(stats["equipements_up"] / total * 100, 2)

        # Latence moyenne des équipements joignables
        cursor.execute(
            "SELECT AVG(latence_ms) AS lat FROM equipements WHERE statut = 'UP'"
        )
        lat = cursor.fetchone()["lat"]
        stats["latence_moyenne"] = round(lat, 2) if lat else 0

        return stats
