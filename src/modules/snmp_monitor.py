# -*- coding: utf-8 -*-
"""
snmp_monitor.py
===============
Sonde SNMP (Simple Network Management Protocol) — supervision « profonde ».

Là où la sonde ICMP se contente de dire si un équipement répond, SNMP permet
d'interroger l'équipement sur son **état interne** : nom du système, description
(modèle, OS), temps de fonctionnement (uptime). C'est le protocole standard de
gestion des équipements réseau (routeurs, switchs, serveurs, imprimantes…).

Choix d'implémentation
----------------------
On s'appuie sur l'utilitaire **`snmpget`** du paquet *net-snmp*, appelé en
sous-processus — exactement comme la sonde ICMP s'appuie sur `ping`. Ce choix
est volontaire :
  * robustesse et légèreté (pas de dépendance Python lourde à compiler) ;
  * indépendance vis-à-vis de la version de Python ;
  * outil éprouvé et universel.

Pré-requis :
  * Côté serveur de supervision : ``sudo apt install -y snmp``
  * Côté équipement supervisé : un agent SNMP actif (ex. ``snmpd``) avec une
    communauté en lecture connue (``SNMP_COMMUNITY``).
"""

import subprocess

from config import config
from modules.logger import get_logger

logger = get_logger("snmp")

# OID standards de la MIB-II (RFC 1213) — présents sur TOUT agent SNMP.
OID_SYS_DESCR = "1.3.6.1.2.1.1.1.0"     # description du système (modèle / OS)
OID_SYS_UPTIME = "1.3.6.1.2.1.1.3.0"    # temps de fonctionnement (uptime)
OID_SYS_NAME = "1.3.6.1.2.1.1.5.0"      # nom (hostname) du système


def _snmpget(ip, oid):
    """Exécute un ``snmpget`` sur (ip, oid) et retourne la valeur, ou None.

    Options snmpget :
      -v <version>   version SNMP (1 ou 2c)
      -c <communaute> communauté en lecture
      -Oqv           sortie « quiet, value only » (juste la valeur, sans l'OID)
      -t <timeout>   délai d'attente par tentative (secondes)
      -r 1           une seule retransmission (évite d'allonger les cycles)
    """
    try:
        resultat = subprocess.run(
            ["snmpget", "-v", config.SNMP_VERSION, "-c", config.SNMP_COMMUNITY,
             "-Oqv", "-t", str(config.SNMP_TIMEOUT), "-r", "1", ip, oid],
            capture_output=True, text=True, timeout=config.SNMP_TIMEOUT + 3,
        )
        if resultat.returncode == 0 and resultat.stdout.strip():
            return resultat.stdout.strip().strip('"')
        return None
    except FileNotFoundError:
        logger.error("Outil 'snmpget' introuvable : installez le paquet "
                     "'snmp' (sudo apt install -y snmp).")
        return None
    except Exception as exc:                          # timeout, hôte injoignable…
        logger.debug("SNMP échec sur %s (%s) : %s", ip, oid, exc)
        return None


def interroger_snmp(ip):
    """Interroge un équipement par SNMP.

    Returns:
        dict : {"disponible": bool, "nom", "description", "uptime"}.
        Si l'équipement ne répond pas en SNMP, ``disponible`` vaut False.
    """
    description = _snmpget(ip, OID_SYS_DESCR)
    if description is None:
        return {"disponible": False}
    return {
        "disponible": True,
        "nom": _snmpget(ip, OID_SYS_NAME),
        "description": description,
        "uptime": _snmpget(ip, OID_SYS_UPTIME),
    }


def resume_snmp(ip):
    """Retourne une chaîne lisible résumant l'état SNMP (pour les journaux)."""
    infos = interroger_snmp(ip)
    if not infos["disponible"]:
        return None
    return "SNMP: %s (uptime %s)" % (infos.get("nom") or "?",
                                     infos.get("uptime") or "?")
