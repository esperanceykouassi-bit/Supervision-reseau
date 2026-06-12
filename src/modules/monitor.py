"""
monitor.py - Vérification périodique de l'état des équipements.

Fonctions principales :
    verifier_equipements(db)                 -> None
    calculer_disponibilite(equipement_id, db, jours) -> float
"""

import subprocess
import platform
from datetime import datetime, timedelta

from .db import fetch_all, fetch_one, execute_query


# ---------------------------------------------------------------------------
# Ping
# ---------------------------------------------------------------------------

def ping_host(ip: str) -> bool:
    """
    Envoie 2 paquets ICMP vers ip avec timeout 2 s.

    Returns:
        True si l'hôte répond, False sinon.
    """
    systeme = platform.system().lower()
    if systeme == 'windows':
        cmd = ['ping', '-n', '2', '-w', '2000', str(ip)]
    else:
        cmd = ['ping', '-c', '2', '-W', '2', str(ip)]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=6,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


# ---------------------------------------------------------------------------
# Vérification des équipements
# ---------------------------------------------------------------------------

def verifier_equipements(db) -> None:
    """
    Parcourt tous les équipements, ping chacun, met à jour la base et
    génère des alertes si l'état change.

    Args:
        db: Connexion MySQL active.
    """
    equipements = fetch_all("SELECT * FROM equipements", connection=db)

    for eq in equipements:
        eq_id        = eq['id']
        eq_nom       = eq['nom']
        eq_ip        = eq['ip']
        ancien_statut = eq['statut']

        is_up = ping_host(eq_ip)
        nouveau_statut = 'actif' if is_up else 'inactif'

        # Mettre à jour l'équipement
        execute_query(
            "UPDATE equipements SET statut=%s, derniere_verification=NOW() WHERE id=%s",
            (nouveau_statut, eq_id),
            connection=db,
        )

        # Changement d'état
        if ancien_statut != nouveau_statut:
            # Historique
            execute_query(
                """INSERT INTO historique_statuts
                       (equipement_id, statut_ancien, statut_nouveau, timestamp)
                   VALUES (%s, %s, %s, NOW())""",
                (eq_id, ancien_statut, nouveau_statut),
                connection=db,
            )

            if nouveau_statut == 'inactif':
                niveau = 'CRITICAL'
                msg    = f"Équipement {eq_nom} ({eq_ip}) est HORS LIGNE"
                execute_query(
                    """INSERT INTO alertes (equipement_id, type_alerte, message, envoye, timestamp)
                       VALUES (%s, 'panne', %s, FALSE, NOW())""",
                    (eq_id, msg),
                    connection=db,
                )
            elif nouveau_statut == 'actif' and ancien_statut == 'inactif':
                niveau = 'INFO'
                msg    = f"Équipement {eq_nom} ({eq_ip}) est de retour EN LIGNE"
                execute_query(
                    """INSERT INTO alertes (equipement_id, type_alerte, message, envoye, timestamp)
                       VALUES (%s, 'retour', %s, FALSE, NOW())""",
                    (eq_id, msg),
                    connection=db,
                )
            else:
                niveau = 'INFO'
                msg    = f"Statut changé : {ancien_statut} -> {nouveau_statut}"
        else:
            niveau = 'INFO' if is_up else 'WARNING'
            msg    = f"Statut inchangé : {nouveau_statut}"

        # Journal
        execute_query(
            """INSERT INTO journaux (equipement_id, niveau, message, timestamp)
               VALUES (%s, %s, %s, NOW())""",
            (eq_id, niveau, msg),
            connection=db,
        )


# ---------------------------------------------------------------------------
# Disponibilité
# ---------------------------------------------------------------------------

def calculer_disponibilite(equipement_id: int, db, jours: int = 7) -> float:
    """
    Calcule le pourcentage de disponibilité d'un équipement sur une période.

    Args:
        equipement_id: Identifiant de l'équipement.
        db:            Connexion MySQL active.
        jours:         Nombre de jours à analyser (défaut 7).

    Returns:
        Pourcentage (float entre 0.0 et 100.0) arrondi à 2 décimales.
    """
    depuis = datetime.now() - timedelta(days=jours)

    historique = fetch_all(
        """SELECT statut_ancien, statut_nouveau, timestamp
           FROM historique_statuts
           WHERE equipement_id = %s AND timestamp >= %s
           ORDER BY timestamp ASC""",
        (equipement_id, depuis),
        connection=db,
    )

    # Aucun changement d'état : statut actuel = disponibilité totale ou nulle
    if not historique:
        eq = fetch_one(
            "SELECT statut FROM equipements WHERE id = %s",
            (equipement_id,),
            connection=db,
        )
        if eq and eq['statut'] == 'actif':
            return 100.0
        return 0.0

    total_seconds = jours * 86400
    down_seconds  = 0.0
    down_since    = None

    for entry in historique:
        ts = entry['timestamp']
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)

        if entry['statut_nouveau'] == 'inactif':
            down_since = ts
        elif entry['statut_nouveau'] == 'actif' and down_since is not None:
            down_seconds += (ts - down_since).total_seconds()
            down_since = None

    # Toujours en panne à la fin de la période
    if down_since is not None:
        down_seconds += (datetime.now() - down_since).total_seconds()

    up_seconds = max(0.0, total_seconds - down_seconds)
    return round((up_seconds / total_seconds) * 100.0, 2)
