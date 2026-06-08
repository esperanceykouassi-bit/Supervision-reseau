# -*- coding: utf-8 -*-
"""
ping_monitor.py
===============
Module de sonde ICMP (ping).

Il teste la joignabilité d'un hôte au niveau de la couche 3 (réseau) en
envoyant des paquets ICMP Echo Request. C'est la sonde la plus élémentaire
de toute supervision : si un équipement ne répond plus au ping, il est
probablement injoignable (panne, câble débranché, équipement éteint...).

On extrait également la latence (RTT - Round Trip Time) qui est un indicateur
de qualité de service : une latence qui grimpe peut annoncer une saturation.
"""

import platform
import re
import subprocess

from config import config
from modules.logger import get_logger

logger = get_logger("ping")


def ping(adresse_ip: str):
    """Envoie des paquets ICMP vers `adresse_ip`.

    Args:
        adresse_ip: adresse IP ou nom d'hôte de la cible.

    Returns:
        tuple (statut, latence_ms) où :
          - statut   : 'UP' si l'hôte répond, 'DOWN' sinon ;
          - latence_ms : latence moyenne en millisecondes (None si DOWN).
    """
    # La commande ping diffère entre Windows (-n) et Linux/Mac (-c).
    systeme = platform.system().lower()
    param_count = "-n" if systeme == "windows" else "-c"
    param_timeout = "-w" if systeme == "windows" else "-W"

    commande = [
        "ping",
        param_count,
        str(config.PING_COUNT),
        param_timeout,
        str(config.PING_TIMEOUT),
        adresse_ip,
    ]

    try:
        # On capture la sortie pour en extraire la latence.
        # timeout global de sécurité pour ne jamais bloquer la sonde.
        resultat = subprocess.run(
            commande,
            capture_output=True,
            text=True,
            timeout=config.PING_TIMEOUT * config.PING_COUNT + 5,
        )

        if resultat.returncode == 0:
            latence = _extraire_latence(resultat.stdout)
            logger.debug("PING %s : UP (%.1f ms)", adresse_ip, latence or -1)
            return "UP", latence
        else:
            logger.debug("PING %s : DOWN (code retour %s)", adresse_ip, resultat.returncode)
            return "DOWN", None

    except subprocess.TimeoutExpired:
        logger.warning("PING %s : délai dépassé (timeout).", adresse_ip)
        return "DOWN", None
    except Exception as exc:  # robustesse : on ne laisse jamais planter la sonde
        logger.error("PING %s : erreur inattendue : %s", adresse_ip, exc)
        return "DOWN", None


def _extraire_latence(sortie: str):
    """Extrait la latence moyenne depuis la sortie texte de la commande ping.

    On gère les deux formats principaux :
      - Linux  : « rtt min/avg/max/mdev = 0.1/0.2/0.3/0.0 ms »
      - Windows: « Moyenne = 12ms » / « Average = 12ms »
    """
    # Format Linux : on récupère la valeur "avg" (2e nombre).
    match = re.search(r"=\s*[\d.]+/([\d.]+)/", sortie)
    if match:
        return float(match.group(1))

    # Format Windows (français ou anglais).
    match = re.search(r"(?:Moyenne|Average)\s*=\s*(\d+)\s*ms", sortie)
    if match:
        return float(match.group(1))

    return None
