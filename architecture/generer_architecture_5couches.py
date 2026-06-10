# -*- coding: utf-8 -*-
"""
generer_architecture_5couches.py
================================
Génère le schéma de l'architecture en 5 couches du système de supervision
au format PNG (image haute résolution prête pour la soutenance / le mémoire).

Utilisation :
    pip install matplotlib
    python generer_architecture_5couches.py
"""

import os
import matplotlib
matplotlib.use("Agg")  # rendu sans interface graphique (serveur)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Charte graphique (dégradé de bleus, du clair au foncé)
COUCHES = [
    ("PRÉSENTATION", "Tableau de bord Flask  •  Bootstrap 5  •  Chart.js  •  API REST", "#3a86ff"),
    ("NOTIFICATION", "Alerte e-mail (SMTP, STARTTLS)   +   Telegram (push mobile, HTTPS)", "#2a6fb0"),
    ("TRAITEMENT", "Moteur Python (supervisor.py)  •  Cron  •  Sondes ICMP / TCP  •  Découverte", "#1b4f72"),
    ("DONNÉES", "Base MySQL : équipements · journaux · alertes · utilisateurs · statistiques", "#14415c"),
    ("SYSTÈME", "Serveur Linux Ubuntu Server 22.04 LTS", "#0d3b66"),
]

fig, ax = plt.subplots(figsize=(12, 7.2), dpi=150)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Titre
ax.text(5, 9.55, "Architecture en 5 couches du système de supervision",
        ha="center", va="center", fontsize=17, fontweight="bold", color="#0d3b66")

# Dessin des couches (de haut en bas)
hauteur = 1.25
y = 8.4
largeur = 8.6
x0 = 0.7
boites_y = []
for nom, desc, couleur in COUCHES:
    boite = FancyBboxPatch((x0, y - hauteur), largeur, hauteur,
                           boxstyle="round,pad=0.02,rounding_size=0.12",
                           linewidth=0, facecolor=couleur)
    ax.add_patch(boite)
    ax.text(x0 + 0.25, y - hauteur / 2 + 0.18, nom,
            ha="left", va="center", fontsize=14.5, fontweight="bold", color="white")
    ax.text(x0 + 0.25, y - hauteur / 2 - 0.25, desc,
            ha="left", va="center", fontsize=11, color="#e8eef4")
    boites_y.append(y - hauteur / 2)
    y -= (hauteur + 0.16)

# Flèches verticales bidirectionnelles entre couches (flux de données)
for i in range(len(boites_y) - 1):
    fleche = FancyArrowPatch((x0 + largeur + 0.35, boites_y[i] - 0.5),
                             (x0 + largeur + 0.35, boites_y[i + 1] + 0.5),
                             arrowstyle="<|-|>", mutation_scale=14,
                             linewidth=1.6, color="#888888")
    ax.add_patch(fleche)

# Accolade / légende latérale "flux"
ax.text(x0 + largeur + 0.75, 4.4, "Flux\nde\ndonnées", ha="left", va="center",
        fontsize=10, color="#666666", rotation=0, style="italic")

# Encadré "choix clé"
note = FancyBboxPatch((x0, 0.15), largeur + 0.9, 0.8,
                      boxstyle="round,pad=0.02,rounding_size=0.08",
                      linewidth=1.4, edgecolor="#0d6efd", facecolor="#f1f5fb")
ax.add_patch(note)
ax.text(x0 + 0.25, 0.55,
        "Choix clé : découplage Moteur de collecte (Cron) ↔ Interface (Flask).\n"
        "La surveillance se poursuit même si le tableau de bord est arrêté.",
        ha="left", va="center", fontsize=10.5, color="#0d3b66", fontweight="bold")

sortie = os.path.join(os.path.dirname(__file__), "architecture-5couches.png")
plt.savefig(sortie, bbox_inches="tight", facecolor="white")
print(f"Image générée : {sortie}")
