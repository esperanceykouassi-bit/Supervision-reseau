# -*- coding: utf-8 -*-
"""
detection.py
============
Module de DÉCOUVERTE automatique des équipements (auto-discovery).

Il balaie une plage d'adresses IP (sous-réseau) afin de détecter les hôtes
actifs et de les pré-enregistrer dans la base. Cela évite la saisie manuelle
fastidieuse de chaque équipement et garantit que la cartographie réseau reste
à jour (un nouvel équipement branché est repéré automatiquement).

La découverte combine un ping ICMP et une tentative de résolution du nom
d'hôte (reverse DNS) pour proposer un nom lisible.
"""

import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.logger import get_logger
from modules.ping_monitor import ping
from modules import database

logger = get_logger("detection")


def _scanner_hote(adresse_ip: str):
    """Teste un hôte unique : retourne ses infos s'il est actif, sinon None."""
    statut, latence = ping(adresse_ip)
    if statut != "UP":
        return None

    # Tentative de reverse DNS pour obtenir un nom convivial.
    try:
        nom = socket.gethostbyaddr(adresse_ip)[0]
    except (socket.herror, socket.gaierror):
        nom = f"hote-{adresse_ip.replace('.', '-')}"

    return {"adresse_ip": adresse_ip, "nom": nom, "latence_ms": latence}


def decouvrir_reseau(cidr: str, max_threads: int = 50):
    """Découvre les hôtes actifs d'un sous-réseau au format CIDR.

    Args:
        cidr: sous-réseau, ex. « 192.168.1.0/24 ».
        max_threads: parallélisme (le scan séquentiel d'un /24 serait trop lent).

    Returns:
        Liste de dictionnaires décrivant les hôtes actifs trouvés.
    """
    try:
        reseau = ipaddress.ip_network(cidr, strict=False)
    except ValueError as exc:
        logger.error("CIDR invalide « %s » : %s", cidr, exc)
        return []

    hotes = [str(ip) for ip in reseau.hosts()]
    logger.info("Découverte du réseau %s (%d adresses à scanner)...", cidr, len(hotes))

    actifs = []
    # On parallélise les pings : un /24 (254 hôtes) passe de plusieurs minutes
    # à quelques secondes grâce au pool de threads.
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(_scanner_hote, ip): ip for ip in hotes}
        for future in as_completed(futures):
            resultat = future.result()
            if resultat:
                actifs.append(resultat)
                logger.info("  -> Hôte actif détecté : %s (%s)",
                            resultat["adresse_ip"], resultat["nom"])

    logger.info("Découverte terminée : %d hôte(s) actif(s).", len(actifs))
    return actifs


def enregistrer_decouverte(cidr: str, type_par_defaut: str = "Inconnu"):
    """Découvre le réseau et insère en base les nouveaux équipements.

    Les équipements déjà présents (même IP) ne sont pas dupliqués.
    """
    actifs = decouvrir_reseau(cidr)
    existants = {e["adresse_ip"] for e in database.get_all_equipements(actifs_seulement=False)}

    nouveaux = 0
    for hote in actifs:
        if hote["adresse_ip"] not in existants:
            database.add_equipement(
                nom=hote["nom"],
                adresse_ip=hote["adresse_ip"],
                type_equipement=type_par_defaut,
                emplacement="Découvert automatiquement",
            )
            nouveaux += 1

    logger.info("%d nouvel(aux) équipement(s) enregistré(s) en base.", nouveaux)
    return nouveaux
