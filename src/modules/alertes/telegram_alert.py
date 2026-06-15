# -*- coding: utf-8 -*-
"""
telegram_alert.py
=================
Canal d'alerte instantanée via un bot Telegram.

Telegram offre une notification « push » gratuite, fiable et quasi instantanée
sur smartphone, ce qui réduit considérablement le temps de réaction de
l'administrateur (objectif central du mémoire). On utilise l'API HTTP du bot
(méthode sendMessage) via une simple requête POST.

Pré-requis : créer un bot via @BotFather pour obtenir le TELEGRAM_BOT_TOKEN,
puis récupérer le chat_id de l'administrateur ou du groupe d'astreinte.
"""

import html

import requests

from config import config
from modules.logger import get_logger

logger = get_logger("alerte_telegram")

# Modèle d'URL de l'API Telegram Bot.
API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def _construire_message(equipement, type_alerte, severite, message):
    """Construit le texte de la notification au format HTML Telegram.

    On utilise le mode HTML (et non Markdown) car certaines valeurs dynamiques
    contiennent des caractères réservés au Markdown — par exemple l'underscore
    de « PANNE_RESEAU » ou « SERVICE_INDISPONIBLE » — qui faisaient échouer le
    rendu (HTTP 400 « can't parse entities »). Les valeurs variables sont
    échappées pour neutraliser les caractères spéciaux HTML (<, >, &).
    """
    icone = {"CRITIQUE": "🔴", "AVERTISSEMENT": "🟠", "INFO": "🔵"}.get(severite, "⚪")

    def esc(valeur):
        return html.escape(str(valeur))

    return (
        f"{icone} <b>ALERTE SUPERVISION</b>\n\n"
        f"<b>Équipement :</b> {esc(equipement['nom'])}\n"
        f"<b>IP :</b> <code>{esc(equipement['adresse_ip'])}</code>\n"
        f"<b>Type :</b> {esc(type_alerte)}\n"
        f"<b>Sévérité :</b> {esc(severite)}\n"
        f"<b>Détail :</b> {esc(message)}"
    )


def envoyer_alerte_telegram(equipement, type_alerte, severite, message):
    """Envoie l'alerte via Telegram. Retourne True si l'envoi a réussi."""
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        logger.warning("Bot Telegram non configuré : notification non envoyée.")
        return False

    url = API_URL.format(token=config.TELEGRAM_BOT_TOKEN)
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": _construire_message(equipement, type_alerte, severite, message),
        "parse_mode": "HTML",
    }

    try:
        reponse = requests.post(url, data=payload, timeout=10)
        if reponse.status_code == 200:
            logger.info("Notification Telegram envoyée pour %s.", equipement["nom"])
            return True
        logger.error("Échec Telegram (HTTP %s) : %s", reponse.status_code, reponse.text)
        return False
    except Exception as exc:
        logger.error("Erreur lors de l'envoi Telegram : %s", exc)
        return False
