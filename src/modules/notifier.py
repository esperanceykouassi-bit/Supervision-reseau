"""
notifier.py - Envoi de notifications par e-mail et Telegram.

Fonctions principales :
    envoyer_email(sujet, corps, destinataire, config)  -> bool
    envoyer_telegram(message, config)                  -> bool
    traiter_alertes(db, config)                        -> None
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from .db import fetch_all, execute_query


# ---------------------------------------------------------------------------
# E-mail
# ---------------------------------------------------------------------------

def envoyer_email(sujet: str, corps: str, destinataire: str, config: dict) -> bool:
    """
    Envoie un e-mail via SMTP (STARTTLS).

    Args:
        sujet:        Objet du message.
        corps:        Corps en texte brut.
        destinataire: Adresse e-mail du destinataire.
        config:       Dictionnaire contenant SMTP_HOST, SMTP_PORT,
                      SMTP_USER, SMTP_PASS.

    Returns:
        True si l'envoi a réussi, False sinon.
    """
    smtp_host = config.get('SMTP_HOST', '')
    smtp_port = int(config.get('SMTP_PORT', 587))
    smtp_user = config.get('SMTP_USER', '')
    smtp_pass = config.get('SMTP_PASS', '')

    if not smtp_host or not smtp_user:
        print("Configuration SMTP incomplète – e-mail non envoyé.")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sujet
        msg['From']    = smtp_user
        msg['To']      = destinataire
        msg.attach(MIMEText(corps, 'plain', 'utf-8'))

        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, destinataire, msg.as_string())

        print(f"E-mail envoyé à {destinataire} : {sujet}")
        return True

    except Exception as exc:
        print(f"Erreur lors de l'envoi de l'e-mail : {exc}")
        return False


# ---------------------------------------------------------------------------
# Telegram
# ---------------------------------------------------------------------------

def envoyer_telegram(message: str, config: dict) -> bool:
    """
    Envoie un message via l'API Bot Telegram.

    Args:
        message: Texte du message.
        config:  Dictionnaire contenant TELEGRAM_TOKEN et TELEGRAM_CHAT_ID.

    Returns:
        True si l'envoi a réussi, False sinon.
    """
    token   = config.get('TELEGRAM_TOKEN', '')
    chat_id = config.get('TELEGRAM_CHAT_ID', '')

    if not token or not chat_id:
        print("Configuration Telegram incomplète – notification non envoyée.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(
            url,
            json={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'},
            timeout=10,
        )
        if response.status_code == 200:
            print(f"Message Telegram envoyé au chat {chat_id}.")
            return True
        else:
            print(f"Erreur Telegram HTTP {response.status_code}: {response.text}")
            return False

    except Exception as exc:
        print(f"Erreur lors de l'envoi Telegram : {exc}")
        return False


# ---------------------------------------------------------------------------
# Traitement des alertes en attente
# ---------------------------------------------------------------------------

def traiter_alertes(db, config: dict) -> None:
    """
    Récupère toutes les alertes non envoyées et tente de les notifier.

    Args:
        db:     Connexion MySQL active.
        config: Dictionnaire de configuration (clés SMTP_*, TELEGRAM_*, ALERT_EMAIL).
    """
    alertes = fetch_all(
        """SELECT a.id,
                  a.type_alerte,
                  a.message,
                  a.timestamp,
                  e.nom  AS equipement_nom,
                  e.ip   AS equipement_ip
           FROM alertes a
           JOIN equipements e ON a.equipement_id = e.id
           WHERE a.envoye = FALSE
           ORDER BY a.timestamp ASC""",
        connection=db,
    )

    for alerte in alertes:
        sujet = (
            f"[Supervision] {alerte['type_alerte'].upper()}: "
            f"{alerte['equipement_nom']}"
        )
        corps = (
            f"Alerte réseau détectée :\n\n"
            f"Équipement : {alerte['equipement_nom']} ({alerte['equipement_ip']})\n"
            f"Type       : {alerte['type_alerte']}\n"
            f"Message    : {alerte['message']}\n"
            f"Heure      : {alerte['timestamp']}\n\n"
            f"-- Système de Supervision Réseau"
        )

        email_ok    = False
        telegram_ok = False

        # Tentative e-mail
        destinataire = config.get('ALERT_EMAIL', '')
        if destinataire and config.get('SMTP_HOST'):
            email_ok = envoyer_email(sujet, corps, destinataire, config)

        # Tentative Telegram
        if config.get('TELEGRAM_TOKEN'):
            telegram_ok = envoyer_telegram(f"<b>{sujet}</b>\n{alerte['message']}", config)

        # Marquer comme envoyé si au moins un canal a réussi,
        # ou si aucun canal n'est configuré (pas de destinataire → alerte gérée)
        aucun_canal = not destinataire and not config.get('TELEGRAM_TOKEN')
        if email_ok or telegram_ok or aucun_canal:
            execute_query(
                "UPDATE alertes SET envoye = TRUE WHERE id = %s",
                (alerte['id'],),
                connection=db,
            )
            print(f"Alerte #{alerte['id']} marquée comme envoyée.")
        else:
            print(f"Alerte #{alerte['id']} : échec de notification, sera réessayée.")
