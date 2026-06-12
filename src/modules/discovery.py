"""
discovery.py - Découverte réseau par balayage ICMP (ping).

Fonctions principales :
    decouvrir_reseau(subnet)         -> list[dict]
    sauvegarder_equipements(hosts, db)
"""

import subprocess
import socket
import ipaddress
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from .db import execute_query, fetch_one


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ping_once(ip: str) -> bool:
    """Envoie 1 paquet ICMP vers ip avec timeout 1 s. Retourne True si répond."""
    systeme = platform.system().lower()
    if systeme == 'windows':
        cmd = ['ping', '-n', '1', '-w', '1000', str(ip)]
    else:
        cmd = ['ping', '-c', '1', '-W', '1', str(ip)]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _resolve_hostname(ip: str) -> str:
    """Tente une résolution DNS inverse. Retourne l'IP si impossible."""
    try:
        hostname, _, _ = socket.gethostbyaddr(str(ip))
        return hostname
    except (socket.herror, socket.gaierror, OSError):
        return str(ip)


def _scanner_hote(ip) -> dict | None:
    """Ping un hôte et retourne un dict si répond, sinon None."""
    ip_str = str(ip)
    if _ping_once(ip_str):
        nom = _resolve_hostname(ip_str)
        return {'ip': ip_str, 'nom': nom, 'statut': 'actif'}
    return None


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------

def decouvrir_reseau(subnet: str) -> list[dict]:
    """
    Scanne tous les hôtes d'un sous-réseau par ping ICMP.

    Args:
        subnet: Notation CIDR, ex. '192.168.1.0/24'.

    Returns:
        Liste de dicts {ip, nom, statut} pour chaque hôte qui répond.
    """
    try:
        reseau = ipaddress.ip_network(subnet, strict=False)
    except ValueError as exc:
        raise ValueError(f"Sous-réseau invalide : {subnet}") from exc

    hotes = list(reseau.hosts())
    resultats = []

    # Utiliser un pool de threads pour accélérer le scan
    max_workers = min(50, len(hotes)) if hotes else 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_scanner_hote, ip): ip for ip in hotes}
        for future in as_completed(futures):
            resultat = future.result()
            if resultat:
                resultats.append(resultat)

    # Trier par adresse IP
    resultats.sort(key=lambda h: ipaddress.ip_address(h['ip']))
    return resultats


def sauvegarder_equipements(hosts: list[dict], db) -> None:
    """
    Insère ou met à jour (UPSERT) les équipements découverts dans la base.

    Args:
        hosts: Liste de dicts {ip, nom, statut} retournée par decouvrir_reseau().
        db:    Connexion MySQL active.
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for host in hosts:
        ip     = host.get('ip', '')
        nom    = host.get('nom', ip)
        statut = host.get('statut', 'inconnu')

        if not ip:
            continue

        # Vérifier si l'équipement existe déjà
        existant = fetch_one(
            "SELECT id, statut FROM equipements WHERE ip = %s",
            (ip,),
            connection=db,
        )

        if existant:
            # Mise à jour du statut et de la dernière vérification
            execute_query(
                """
                UPDATE equipements
                SET statut = %s,
                    derniere_verification = %s,
                    nom = %s
                WHERE ip = %s
                """,
                (statut, now, nom, ip),
                connection=db,
            )
        else:
            # Insertion d'un nouvel équipement
            execute_query(
                """
                INSERT INTO equipements (nom, ip, type, localisation, statut, derniere_verification)
                VALUES (%s, %s, 'inconnu', '', %s, %s)
                """,
                (nom, ip, statut, now),
                connection=db,
            )

        # Journaliser la découverte
        execute_query(
            """
            INSERT INTO journaux (equipement_id, niveau, message)
            SELECT id, 'INFO', CONCAT('Équipement découvert/mis à jour : ', ip)
            FROM equipements WHERE ip = %s
            """,
            (ip,),
            connection=db,
        )
