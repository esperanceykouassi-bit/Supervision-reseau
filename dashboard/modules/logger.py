# -*- coding: utf-8 -*-
"""
logger.py
=========
Module de journalisation (logging) du système de supervision.

Il fournit une fonction `get_logger()` qui retourne un logger configuré
pour écrire simultanément :
  - dans un fichier tournant (rotation automatique pour éviter la saturation
    du disque, point critique sur un serveur de supervision) ;
  - dans la console (utile en mode debug et pour systemd/journalctl).

La rotation des journaux est une exigence d'exploitation : sans elle, le
fichier de log croît indéfiniment et peut remplir la partition système.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from config import config


def get_logger(name: str = "supervision") -> logging.Logger:
    """Crée (ou récupère) un logger configuré.

    Args:
        name: nom logique du logger (permet de distinguer les modules).

    Returns:
        Un objet logging.Logger prêt à l'emploi.
    """
    logger = logging.getLogger(name)

    # Si le logger possède déjà des handlers, on évite de les dupliquer
    # (sinon chaque import ajouterait un nouveau handler -> logs en double).
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

    # Format commun : horodatage | niveau | module | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Handler fichier avec rotation (5 fichiers de 2 Mo max) --------- #
    os.makedirs(config.LOG_DIR, exist_ok=True)
    file_path = os.path.join(config.LOG_DIR, config.LOG_FILE)
    file_handler = RotatingFileHandler(
        file_path, maxBytes=2 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # --- Handler console ----------------------------------------------- #
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
