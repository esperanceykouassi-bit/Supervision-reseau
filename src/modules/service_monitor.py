# -*- coding: utf-8 -*-
"""
service_monitor.py
==================
Module de sonde de SERVICES (couche transport / application).

Un équipement peut répondre au ping (couche 3) tout en ayant un service
applicatif hors service (ex : serveur web injoignable sur le port 80). Cette
sonde teste l'ouverture d'un port TCP, ce qui constitue une vérification de
disponibilité plus fine et plus représentative de l'expérience utilisateur.

On peut superviser : HTTP(80/443), SSH(22), DNS(53), base de données(3306)...
"""

import socket
import time

from modules.logger import get_logger

logger = get_logger("service")

# Correspondance indicative entre nom de service et port par défaut.
PORTS_CONNUS = {
    "HTTP": 80,
    "HTTPS": 443,
    "SSH": 22,
    "DNS": 53,
    "FTP": 21,
    "SMTP": 25,
    "MYSQL": 3306,
    "RDP": 3389,
}


def verifier_port(adresse_ip: str, port: int, timeout: float = 2.0):
    """Teste l'ouverture d'un port TCP via une tentative de connexion (3-way handshake).

    Args:
        adresse_ip: hôte cible.
        port: port TCP à tester.
        timeout: délai max d'attente en secondes.

    Returns:
        tuple (ouvert: bool, temps_reponse_ms: float | None)
    """
    debut = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        # connect_ex retourne 0 si la connexion réussit (port ouvert).
        code = sock.connect_ex((adresse_ip, port))
        temps_ms = round((time.time() - debut) * 1000, 2)
        if code == 0:
            logger.debug("SERVICE %s:%s : OUVERT (%.1f ms)", adresse_ip, port, temps_ms)
            return True, temps_ms
        logger.debug("SERVICE %s:%s : FERMÉ (code %s)", adresse_ip, port, code)
        return False, None
    except socket.gaierror:
        logger.warning("SERVICE %s : résolution DNS impossible.", adresse_ip)
        return False, None
    except Exception as exc:
        logger.error("SERVICE %s:%s : erreur : %s", adresse_ip, port, exc)
        return False, None
    finally:
        sock.close()  # On ferme toujours la socket pour éviter les fuites de descripteurs.


def verifier_service(adresse_ip: str, nom_service: str):
    """Teste un service identifié par son nom (HTTP, SSH...) sur son port standard."""
    port = PORTS_CONNUS.get(nom_service.upper())
    if port is None:
        logger.error("Service inconnu : %s", nom_service)
        return False, None
    return verifier_port(adresse_ip, port)
