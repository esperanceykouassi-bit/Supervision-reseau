#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
supervisor.py
=============
MOTEUR DE SUPERVISION — script principal exécuté périodiquement par Cron.

Cycle d'exécution (à chaque appel) :
  1. Récupère la liste des équipements actifs depuis la base ;
  2. Pour chacun, lance la sonde ICMP (ping) ;
  3. Met à jour le statut et journalise le résultat ;
  4. Applique un seuil d'échecs consécutifs (anti-faux positif) avant d'alerter ;
  5. Déclenche les alertes multi-canal en cas de panne confirmée ;
  6. Notifie le rétablissement quand un équipement revient en ligne.

Ce découplage « moteur (cron) / interface (Flask) » est un choix d'architecture
important : la collecte tourne en tâche de fond indépendamment de l'interface
web, qui se contente de lire la base. Le système reste donc opérationnel même
si le tableau de bord est arrêté.

Utilisation :
    python3 supervisor.py            # un cycle complet de supervision
    python3 supervisor.py --decouvrir 192.168.1.0/24   # découverte réseau
"""

import argparse
import sys

from modules import database
from modules import alertes
from modules.detection import enregistrer_decouverte
from modules.logger import get_logger
from modules.ping_monitor import ping
from modules.service_monitor import verifier_service
from modules.snmp_monitor import interroger_snmp, resume_snmp
from config import config

logger = get_logger("supervisor")

# Compteur d'échecs consécutifs par équipement, conservé en mémoire entre les
# cycles via un fichier d'état n'est pas nécessaire ici : on s'appuie sur la
# base. On lit les derniers journaux pour décider. Pour rester simple et
# robuste, on stocke le compteur dans la table equipements (champ echecs).


def superviser_equipement(equipement):
    """Supervise un équipement unique : ping + éventuelle sonde de service."""
    nom = equipement["nom"]
    ip = equipement["adresse_ip"]
    ancien_statut = equipement.get("statut")

    # --- Sonde ICMP (couche réseau) ------------------------------------ #
    statut, latence = ping(ip)

    # --- Sonde de service optionnelle (couche application) ------------- #
    # Si un service est défini pour l'équipement (ex. HTTP), on le vérifie.
    service = equipement.get("service_supervise")
    message = ""
    if statut == "UP" and service:
        ouvert, _ = verifier_service(ip, service)
        if not ouvert:
            statut = "DOWN"
            message = f"Hôte joignable mais service {service} indisponible."

    # --- Sonde SNMP optionnelle (supervision « profonde ») ------------- #
    # Si SNMP est activé, on enrichit le journal des équipements joignables
    # avec leur nom système et leur uptime (informations internes de l'agent).
    if config.SNMP_ENABLED and statut == "UP":
        info_snmp = resume_snmp(ip)
        if info_snmp:
            message = (message + " | " if message else "") + info_snmp

    # --- Persistance : statut courant + ligne d'historique ------------- #
    database.update_statut_equipement(equipement["id"], statut, latence)
    database.add_journal(
        equipement["id"], statut, latence,
        message or ("OK" if statut == "UP" else "Aucune réponse ICMP"),
    )

    # --- Logique d'alerte ---------------------------------------------- #
    if statut == "DOWN":
        # On confirme la panne avec le seuil d'échecs consécutifs (anti-faux positif).
        echecs = _compter_echecs_consecutifs(equipement["id"])
        if echecs >= config.FAILURE_THRESHOLD:
            alertes.declencher_alerte(
                equipement,
                type_alerte="PANNE_RESEAU" if not service else "SERVICE_INDISPONIBLE",
                severite="CRITIQUE",
                message=message or f"{nom} ({ip}) ne répond plus après {echecs} tentatives.",
            )
    elif statut == "UP" and ancien_statut == "DOWN":
        # Transition DOWN -> UP : on notifie le rétablissement.
        alertes.alerte_retablissement(equipement, f"{nom} ({ip}) est de nouveau en ligne.")

    return statut, latence


def _compter_echecs_consecutifs(equipement_id, fenetre=10):
    """Compte les échecs consécutifs récents à partir du journal.

    On parcourt les dernières entrées du journal (les plus récentes d'abord)
    et on compte les 'DOWN' jusqu'au premier 'UP'.
    """
    journaux = database.get_journaux(limit=fenetre, equipement_id=equipement_id)
    echecs = 0
    for ligne in journaux:
        if ligne["statut"] == "DOWN":
            echecs += 1
        else:
            break
    return echecs


def cycle_supervision():
    """Exécute un cycle complet sur l'ensemble des équipements actifs."""
    equipements = database.get_all_equipements(actifs_seulement=True)
    logger.info("=== Début du cycle de supervision (%d équipements) ===", len(equipements))

    up, down = 0, 0
    for equipement in equipements:
        statut, _ = superviser_equipement(equipement)
        if statut == "UP":
            up += 1
        else:
            down += 1

    logger.info("=== Fin du cycle : %d UP / %d DOWN ===", up, down)
    return up, down


def main():
    """Point d'entrée : analyse les arguments et lance l'action demandée."""
    parser = argparse.ArgumentParser(description="Moteur de supervision réseau.")
    parser.add_argument(
        "--decouvrir", metavar="CIDR",
        help="Découvre et enregistre les équipements d'un sous-réseau (ex. 192.168.1.0/24).",
    )
    parser.add_argument(
        "--snmp", metavar="IP",
        help="Interroge un équipement par SNMP et affiche ses informations.",
    )
    parser.add_argument(
        "--anomalies", action="store_true",
        help="Analyse l'historique (IA) et émet des alertes préventives "
             "pour les comportements anormaux (panne possible).",
    )
    args = parser.parse_args()

    try:
        if args.decouvrir:
            nb = enregistrer_decouverte(args.decouvrir)
            print(f"{nb} nouvel(aux) équipement(s) découvert(s).")
        elif args.snmp:
            infos = interroger_snmp(args.snmp)
            if infos["disponible"]:
                print(f"Réponse SNMP de {args.snmp} :")
                print(f"  Nom système : {infos.get('nom')}")
                print(f"  Description : {infos.get('description')}")
                print(f"  Uptime      : {infos.get('uptime')}")
            else:
                print(f"Aucune réponse SNMP de {args.snmp} "
                      f"(agent SNMP actif ? communauté '{config.SNMP_COMMUNITY}' correcte ?).")
        elif args.anomalies:
            from modules import anomalies
            nb = anomalies.analyser_et_alerter()
            print(f"Analyse prédictive terminée : {nb} alerte(s) préventive(s) émise(s).")
        else:
            cycle_supervision()
    except Exception as exc:
        logger.critical("Erreur fatale du moteur de supervision : %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
