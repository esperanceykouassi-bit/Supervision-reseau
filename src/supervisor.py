#!/usr/bin/env python3
"""
supervisor.py - Point d'entrée CLI du système de supervision réseau.

Usage:
  python supervisor.py                        # un cycle de surveillance
  python supervisor.py --decouvrir <subnet>   # découverte d'un sous-réseau
"""

import argparse
import sys
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from modules.db import get_connection
from modules.discovery import decouvrir_reseau, sauvegarder_equipements
from modules.monitor import verifier_equipements
from modules.notifier import traiter_alertes


def main():
    parser = argparse.ArgumentParser(
        description='Supervision Réseau — outil de surveillance CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        '--decouvrir',
        metavar='SUBNET',
        help='Découvrir les hôtes actifs sur un sous-réseau (ex: 192.168.1.0/24)',
    )
    args = parser.parse_args()

    try:
        db = get_connection()
    except Exception as exc:
        print(f"[ERREUR] Impossible de se connecter à la base de données : {exc}", file=sys.stderr)
        sys.exit(1)

    if args.decouvrir:
        print(f"[INFO] Découverte du sous-réseau : {args.decouvrir}")
        try:
            hosts = decouvrir_reseau(args.decouvrir)
            sauvegarder_equipements(hosts, db)
            print(f"[OK] {len(hosts)} équipement(s) découvert(s) et sauvegardé(s).")
            for h in hosts:
                print(f"     • {h['ip']:15s}  {h['nom']}")
        except ValueError as exc:
            print(f"[ERREUR] {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        print("[INFO] Démarrage du cycle de supervision …")
        verifier_equipements(db)

        config = {
            key: os.environ.get(key)
            for key in [
                'SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASS',
                'ALERT_EMAIL', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID',
            ]
        }
        nb = traiter_alertes(db, config)
        print(f"[OK] Cycle de supervision terminé. {nb} alerte(s) envoyée(s).")

    try:
        db.close()
    except Exception:
        pass


if __name__ == '__main__':
    main()
