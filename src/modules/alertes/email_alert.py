# -*- coding: utf-8 -*-
"""
email_alert.py
==============
Canal d'alerte par courrier électronique (SMTP).

Envoie un e-mail formaté en HTML aux administrateurs lorsqu'une panne est
détectée. Le protocole SMTP avec STARTTLS chiffre la communication avec le
serveur de messagerie (confidentialité des identifiants — bonne pratique
sécurité).
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config
from modules.logger import get_logger

logger = get_logger("alerte_email")


def _construire_message_html(equipement, type_alerte, severite, message):
    """Construit un corps d'e-mail HTML lisible et professionnel."""
    couleur = {"CRITIQUE": "#dc3545", "AVERTISSEMENT": "#ffc107", "INFO": "#0d6efd"}.get(
        severite, "#6c757d"
    )
    return f"""\
    <html><body style="font-family: Arial, sans-serif; color:#333;">
      <div style="border-left:6px solid {couleur}; padding:16px; background:#f8f9fa;">
        <h2 style="color:{couleur};margin:0 0 10px;">🚨 Alerte Supervision Réseau</h2>
        <table style="border-collapse:collapse;">
          <tr><td><b>Équipement&nbsp;:</b></td><td>{equipement['nom']}</td></tr>
          <tr><td><b>Adresse IP&nbsp;:</b></td><td>{equipement['adresse_ip']}</td></tr>
          <tr><td><b>Type d'alerte&nbsp;:</b></td><td>{type_alerte}</td></tr>
          <tr><td><b>Sévérité&nbsp;:</b></td><td>{severite}</td></tr>
          <tr><td><b>Message&nbsp;:</b></td><td>{message}</td></tr>
        </table>
        <p style="margin-top:16px;font-size:12px;color:#888;">
          Message automatique du système de supervision réseau. Ne pas répondre.
        </p>
      </div>
    </body></html>"""


def envoyer_alerte_email(equipement, type_alerte, severite, message):
    """Envoie l'alerte par e-mail. Retourne True si l'envoi a réussi."""
    if not config.SMTP_USER:
        logger.warning("SMTP non configuré : e-mail non envoyé.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[{severite}] {equipement['nom']} - {type_alerte}"
    msg["From"] = config.ALERT_EMAIL_FROM
    msg["To"] = ", ".join(config.ALERT_EMAIL_TO)
    msg.attach(MIMEText(_construire_message_html(equipement, type_alerte, severite, message), "html"))

    try:
        # Connexion sécurisée : STARTTLS chiffre la session avant l'authentification.
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10) as serveur:
            serveur.starttls()
            serveur.login(config.SMTP_USER, config.SMTP_PASSWORD)
            serveur.sendmail(config.ALERT_EMAIL_FROM, config.ALERT_EMAIL_TO, msg.as_string())
        logger.info("E-mail d'alerte envoyé pour %s (%s).", equipement["nom"], type_alerte)
        return True
    except Exception as exc:
        logger.error("Échec de l'envoi de l'e-mail d'alerte : %s", exc)
        return False
