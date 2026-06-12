"""
db.py - Gestion de la connexion MySQL et fonctions utilitaires.

Charge la configuration depuis le fichier .env via python-dotenv.
Utilise PyMySQL comme pilote MySQL pur-Python.
"""

import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

# Charger le fichier .env situé dans le dossier parent de ce module
_env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(_env_path)


def get_connection() -> pymysql.connections.Connection:
    """
    Crée et retourne une connexion PyMySQL configurée depuis les variables d'environnement.

    Variables requises :
        DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

    Returns:
        pymysql.connections.Connection
    """
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        database=os.environ.get('DB_NAME', 'supervision_reseau'),
        user=os.environ.get('DB_USER', 'supervisor'),
        password=os.environ.get('DB_PASS', 'SuperPass2024!'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        connect_timeout=10,
    )
    return connection


def execute_query(sql: str, params: tuple = None, connection=None) -> int:
    """
    Exécute une requête INSERT / UPDATE / DELETE.

    Args:
        sql:        Requête SQL avec placeholders %s.
        params:     Tuple de paramètres.
        connection: Connexion existante (si None, une nouvelle est créée).

    Returns:
        Nombre de lignes affectées.
    """
    close_after = connection is None
    conn = connection if connection else get_connection()
    try:
        with conn.cursor() as cursor:
            affected = cursor.execute(sql, params or ())
            if not conn.get_autocommit():
                conn.commit()
            return affected
    finally:
        if close_after:
            conn.close()


def fetch_all(sql: str, params: tuple = None, connection=None) -> list:
    """
    Exécute une requête SELECT et retourne toutes les lignes.

    Args:
        sql:        Requête SQL avec placeholders %s.
        params:     Tuple de paramètres.
        connection: Connexion existante (si None, une nouvelle est créée).

    Returns:
        Liste de dictionnaires représentant chaque ligne.
    """
    close_after = connection is None
    conn = connection if connection else get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
    finally:
        if close_after:
            conn.close()


def fetch_one(sql: str, params: tuple = None, connection=None) -> dict | None:
    """
    Exécute une requête SELECT et retourne la première ligne.

    Args:
        sql:        Requête SQL avec placeholders %s.
        params:     Tuple de paramètres.
        connection: Connexion existante (si None, une nouvelle est créée).

    Returns:
        Dictionnaire représentant la ligne, ou None si aucun résultat.
    """
    close_after = connection is None
    conn = connection if connection else get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchone()
    finally:
        if close_after:
            conn.close()


def get_last_insert_id(connection) -> int:
    """Retourne le dernier ID inséré sur la connexion donnée."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        row = cursor.fetchone()
        return row['id'] if row else 0
