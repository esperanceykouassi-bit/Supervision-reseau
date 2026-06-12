#!/usr/bin/env python3
"""
supervisor.py - Point d'entrée principal du daemon de supervision réseau.

Usage :
    python src/supervisor.py [--discover <subnet>]

Options :
    --discover <subnet>   Lance une découverte réseau sur le sous-réseau indiqué
                          avant la boucle de vérification habituelle.
                          Exemple : --discover 192.168.1.0/24

Sans option, effectue uniquement la vérification ICMP de tous les équipements
enregistrés en base et envoie les alertes en attente.
"""

import os
import sys
import argparse
from datetime import datetime

# Assurer que le dossier src/ est dans le chemin Python
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from dotenv import load_dotenv

# Charger .env depuis le répertoire src/
load_dotenv(os.path.join(_src_dir, '.env'))

from modules.db import get_connection
from modules.monitor import verifier_equipements, calculer_disponibilite
from modules.discovery import decouvrir_reseau, sauvegarder_equipements
from modules.notifier import traiter_alertes


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_config() -> dict:
    """Retourne la configuration depuis les variables d'environnement."""
    return {
        'SMTP_HOST':        os.environ.get('SMTP_HOST', ''),
        'SMTP_PORT':        os.environ.get('SMTP_PORT', '587'),
        'SMTP_USER':        os.environ.get('SMTP_USER', ''),
        'SMTP_PASS':        os.environ.get('SMTP_PASS', ''),
        'ALERT_EMAIL':      os.environ.get('ALERT_EMAIL', ''),
        'TELEGRAM_TOKEN':   os.environ.get('TELEGRAM_TOKEN', ''),
        'TELEGRAM_CHAT_ID': os.environ.get('TELEGRAM_CHAT_ID', ''),
    }


def _log(msg: str) -> None:
    """Affiche un message horodaté sur la sortie standard."""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)


# ---------------------------------------------------------------------------
# Phases
# ---------------------------------------------------------------------------

def phase_decouverte(subnet: str, db) -> None:
    """Scanne le sous-réseau et sauvegarde les hôtes découverts."""
    _log(f"Découverte réseau sur {subnet} …")
    try:
        hotes = decouvrir_reseau(subnet)
        _log(f"  → {len(hotes)} hôte(s) découvert(s).")
        sauvegarder_equipements(hotes, db)
        _log("  → Équipements sauvegardés en base.")
    except ValueError as exc:
        _log(f"  [ERREUR] {exc}")


def phase_verification(db) -> None:
    """Ping tous les équipements enregistrés et met à jour leur statut."""
    _log("Vérification des équipements …")
    verifier_equipements(db)
    _log("  → Vérification terminée.")


def phase_notifications(db, config: dict) -> None:
    """Envoie les alertes non encore notifiées."""
    _log("Traitement des alertes non envoyées …")
    traiter_alertes(db, config)
    _log("  → Traitement des alertes terminé.")


def phase_rapport_disponibilite(db) -> None:
    """Calcule et affiche la disponibilité de chaque équipement (7 derniers jours)."""
    from modules.db import fetch_all
    equipements = fetch_all("SELECT id, nom, ip FROM equipements", connection=db)
    if not equipements:
        _log("Aucun équipement enregistré.")
        return

    _log("Disponibilité (7 derniers jours) :")
    for eq in equipements:
        dispo = calculer_disponibilite(eq['id'], db, jours=7)
        _log(f"  {eq['nom']} ({eq['ip']}) : {dispo:.2f} %")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Daemon de supervision réseau – vérification ICMP + alertes."
    )
    parser.add_argument(
        '--discover',
        metavar='SUBNET',
        default=None,
        help="Sous-réseau CIDR à scanner avant la vérification (ex: 192.168.1.0/24).",
    )
    parser.add_argument(
        '--rapport',
        action='store_true',
        default=False,
        help="Afficher le rapport de disponibilité après la vérification.",
    )
    args = parser.parse_args()

    _log("=== Démarrage du superviseur réseau ===")
    config = _get_config()

    try:
        db = get_connection()
    except Exception as exc:
        _log(f"[FATAL] Impossible de se connecter à la base de données : {exc}")
        sys.exit(1)

    try:
        # 1. Découverte réseau (optionnelle)
        if args.discover:
            phase_decouverte(args.discover, db)

        # 2. Vérification ICMP de tous les équipements
        phase_verification(db)

        # 3. Envoi des alertes
        phase_notifications(db, config)

        # 4. Rapport de disponibilité (optionnel)
        if args.rapport:
            phase_rapport_disponibilite(db)

    except Exception as exc:
        _log(f"[ERREUR] Exception non gérée : {exc}")
        raise
    finally:
        try:
            db.close()
        except Exception:
            pass

    _log("=== Superviseur terminé avec succès ===")


if __name__ == '__main__':
    main()
