# -*- coding: utf-8 -*-
"""
Package « alertes »
===================
Gestionnaire central des alertes (orchestrateur multi-canal).

Ce module joue le rôle de chef d'orchestre : lorsqu'une panne est confirmée,
il enregistre l'alerte en base puis la diffuse sur TOUS les canaux configurés
(e-mail + Telegram). Il applique aussi la logique anti-spam : une seule alerte
est émise par panne tant qu'elle n'est pas résolue/acquittée.
"""

from modules import database
from modules.logger import get_logger
from modules.alertes.email_alert import envoyer_alerte_email
from modules.alertes.telegram_alert import envoyer_alerte_telegram

logger = get_logger("alertes")


def declencher_alerte(equipement, type_alerte, severite, message):
    """Déclenche une alerte multi-canal avec dé-duplication.

    Args:
        equipement: dict décrivant l'équipement (doit contenir id, nom, adresse_ip).
        type_alerte: ex. « PANNE_ICMP », « SERVICE_INDISPONIBLE ».
        severite: « CRITIQUE », « AVERTISSEMENT » ou « INFO ».
        message: description lisible de l'événement.

    Returns:
        True si une alerte a été émise, False si elle a été ignorée (doublon).
    """
    # Anti-spam : si une alerte identique est déjà active, on ne ré-alerte pas.
    if database.derniere_alerte_active(equipement["id"], type_alerte):
        logger.debug("Alerte %s déjà active pour %s : ignorée (anti-spam).",
                     type_alerte, equipement["nom"])
        return False

    # 1) Persistance en base (traçabilité, historique, statistiques).
    database.add_alerte(equipement["id"], type_alerte, severite, message, canal="EMAIL+TELEGRAM")

    # 2) Diffusion sur les canaux de notification.
    envoyer_alerte_email(equipement, type_alerte, severite, message)
    envoyer_alerte_telegram(equipement, type_alerte, severite, message)

    logger.info("Alerte déclenchée : %s sur %s (%s).", type_alerte, equipement["nom"], severite)
    return True


def alerte_retablissement(equipement, message="Équipement de nouveau joignable"):
    """Émet une alerte INFO de rétablissement et acquitte les alertes de panne.

    Quand un équipement revient en ligne, on notifie le retour à la normale et
    on solde automatiquement les alertes de panne ouvertes pour repartir propre.
    """
    alertes_ouvertes = database.get_alertes(non_acquittees=True)
    for alerte in alertes_ouvertes:
        if alerte["equipement_id"] == equipement["id"]:
            database.acquitter_alerte(alerte["id"])

    database.add_alerte(equipement["id"], "RETABLISSEMENT", "INFO", message, canal="EMAIL+TELEGRAM")
    envoyer_alerte_telegram(equipement, "RETABLISSEMENT", "INFO", message)
    logger.info("Rétablissement notifié pour %s.", equipement["nom"])
