# -*- coding: utf-8 -*-
"""
config.py
=========
Module de configuration centralisée du système de supervision réseau.

Toutes les variables sensibles (mots de passe, jetons, etc.) sont chargées
depuis des variables d'environnement afin de ne JAMAIS apparaître en clair
dans le code source (bonne pratique de cybersécurité : principe du secret
hors du code, conforme aux recommandations OWASP).

Auteur  : Étudiant Master 2 RIT
Projet  : Mémoire - Automatisation de la supervision réseau
"""

import os
from dotenv import load_dotenv

# Chargement du fichier .env situé à la racine du projet (variables locales).
# En production, ces variables sont injectées par le système (systemd, Docker...).
load_dotenv()


class Config:
    """Classe de configuration commune à l'ensemble de l'application."""

    # ------------------------------------------------------------------ #
    # Configuration de l'application Flask                                #
    # ------------------------------------------------------------------ #
    # Clé secrète utilisée pour signer les sessions et jetons CSRF.
    SECRET_KEY = os.getenv("SECRET_KEY", "changez-moi-en-production")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", "5000"))
    # Clé d'API pour l'accès des clients mobiles à l'API REST (en-tête
    # « X-API-Key »). Laisser vide pour désactiver l'accès par clé.
    API_KEY = os.getenv("API_KEY", "")
    # Certificat TLS/HTTPS (optionnel). Si les deux fichiers existent, le
    # tableau de bord est servi en HTTPS (connexion chiffrée). Sinon, HTTP.
    SSL_CERT = os.getenv("SSL_CERT", "")
    SSL_KEY = os.getenv("SSL_KEY", "")

    # ------------------------------------------------------------------ #
    # Configuration de la base de données MySQL                          #
    # ------------------------------------------------------------------ #
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "supervision")
    DB_USER = os.getenv("DB_USER", "supervisor")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "supervision_pass")

    # ------------------------------------------------------------------ #
    # Paramètres de supervision (sondes)                                 #
    # ------------------------------------------------------------------ #
    # Nombre de paquets ICMP envoyés à chaque test de ping.
    PING_COUNT = int(os.getenv("PING_COUNT", "3"))
    # Délai d'attente (en secondes) avant de considérer un hôte injoignable.
    PING_TIMEOUT = int(os.getenv("PING_TIMEOUT", "2"))
    # Nombre d'échecs consécutifs avant de déclencher une alerte (anti-faux positif).
    FAILURE_THRESHOLD = int(os.getenv("FAILURE_THRESHOLD", "2"))

    # ------------------------------------------------------------------ #
    # Configuration des alertes E-mail (SMTP)                            #
    # ------------------------------------------------------------------ #
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM", "supervision@exemple.com")
    # Liste des destinataires séparés par des virgules.
    ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "admin@exemple.com").split(",")

    # ------------------------------------------------------------------ #
    # Configuration du bot Telegram                                      #
    # ------------------------------------------------------------------ #
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    # ------------------------------------------------------------------ #
    # Journalisation                                                     #
    # ------------------------------------------------------------------ #
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LOG_FILE = os.getenv("LOG_FILE", "supervision.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # ------------------------------------------------------------------ #
    # Supervision SNMP (Simple Network Management Protocol)              #
    # ------------------------------------------------------------------ #
    # Activé globalement : enrichit chaque cycle avec les infos SNMP des
    # équipements joignables (nom système, uptime). À laisser sur False si
    # le parc n'a pas d'agent SNMP, pour éviter des interrogations inutiles.
    SNMP_ENABLED = os.getenv("SNMP_ENABLED", "False").lower() == "true"
    # Version SNMP : « 1 » ou « 2c » (v2c recommandée).
    SNMP_VERSION = os.getenv("SNMP_VERSION", "2c")
    # Communauté en lecture seule (équivalent d'un mot de passe SNMP).
    SNMP_COMMUNITY = os.getenv("SNMP_COMMUNITY", "public")
    # Délai d'attente (secondes) d'une requête SNMP.
    SNMP_TIMEOUT = int(os.getenv("SNMP_TIMEOUT", "2"))


# Instance unique réutilisée dans toute l'application.
config = Config()
