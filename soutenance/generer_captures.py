# -*- coding: utf-8 -*-
"""
generer_captures.py
===================
Génère des CAPTURES haute-fidélité du tableau de bord de supervision
(reproduisant le rendu réel des templates Flask + Bootstrap) au format PNG,
pour la partie « Démonstration » de la soutenance.

Pages produites :
  - capture-dashboard.png    : tableau de bord (KPI, anneau de dispo, tables)
  - capture-equipements.png  : gestion des équipements
  - capture-alertes.png      : historique des alertes
  - capture-telegram.png     : notification reçue sur smartphone

Utilisation :
    pip install matplotlib
    python generer_captures.py
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

# ----------------------- Charte Bootstrap ------------------------------ #
PRIMARY = "#0d6efd"; SUCCESS = "#198754"; DANGER = "#dc3545"; WARNING = "#ffc107"
DARK = "#212529"; BODY = "#f4f6f9"; LIGHT = "#f8f9fa"; MUTED = "#6c757d"
WHITE = "#ffffff"; TXT = "#333333"; BORDER = "#e3e6ea"; PURPLE = "#6f42c1"
W, H = 1366, 868  # dimensions « écran »

# Données d'exemple réalistes (parc client supervisé par OPEN MOISE)
EQUIPEMENTS = [
    ("Routeur-Principal", "192.168.1.1",   "Routeur",    "UP",   "1.2 ms",  "11:24:58"),
    ("Switch-Etage1",     "192.168.1.2",   "Switch",     "UP",   "0.8 ms",  "11:24:58"),
    ("Serveur-Web",       "192.168.1.10",  "Serveur",    "UP",   "4.5 ms",  "11:24:59"),
    ("Serveur-BDD",       "192.168.1.11",  "Serveur",    "DOWN", "—",       "11:24:59"),
    ("Serveur-Fichiers",  "192.168.1.12",  "Serveur",    "UP",   "2.1 ms",  "11:24:59"),
    ("Point-Acces-WiFi",  "192.168.1.20",  "Borne",      "UP",   "3.7 ms",  "11:25:00"),
    ("Imprimante-RH",     "192.168.1.30",  "Imprimante", "DOWN", "—",       "11:25:00"),
    ("Pare-feu",          "192.168.1.254", "Firewall",   "UP",   "0.9 ms",  "11:25:01"),
]
ALERTES = [
    ("Serveur-BDD",   "192.168.1.11", "PANNE_RESEAU", "CRITIQUE", "10/06 11:20"),
    ("Imprimante-RH", "192.168.1.30", "PANNE_RESEAU", "CRITIQUE", "10/06 11:18"),
]
NB_UP, NB_DOWN = 6, 2
TOTAL = NB_UP + NB_DOWN
DISPO = round(NB_UP / TOTAL * 100, 1)


# ----------------------- Primitives de dessin -------------------------- #
def new_fig():
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off"); ax.invert_yaxis()  # origine en haut à gauche
    ax.add_patch(Rectangle((0, 0), W, H, color=BODY, zorder=0))
    return fig, ax


def rrect(ax, x, y, w, h, color, r=8, ec=None, lw=0, z=1):
    p = FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                       boxstyle=f"round,pad={r},rounding_size={r}",
                       facecolor=color, edgecolor=ec or color,
                       linewidth=lw, zorder=z)
    ax.add_patch(p); return p


def txt(ax, x, y, s, size=12, color=TXT, bold=False, ha="left", va="center",
        family="DejaVu Sans", z=3):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=z,
            fontweight="bold" if bold else "normal", family=family)


def icone(ax, x, y, color, s=15):
    """Petite icône carrée arrondie (remplace les emojis non rendus)."""
    rrect(ax, x, y, s, s, color, r=3, z=3)


def navbar(ax, page_active="Tableau de bord"):
    """Barre de navigation supérieure, identique à base.html."""
    ax.add_patch(Rectangle((0, 0), W, 52, color=DARK, zorder=2))
    icone(ax, 22, 18, PRIMARY, 16)
    txt(ax, 48, 26, "SupervisionNet", 16, WHITE, True)
    menu = ["Tableau de bord", "Équipements", "Alertes", "Journaux", "Rapports"]
    x = 300
    for m in menu:
        actif = (m == page_active)
        txt(ax, x, 26, m, 12.5, WHITE if actif else "#c8ccd0", actif)
        x += len(m) * 9.2 + 40
    ax.add_patch(Circle((W - 360, 26), 8, color="#6d7f8f", zorder=3))
    txt(ax, W - 344, 26, "admin (admin)", 12, "#c8ccd0")
    rrect(ax, W - 134, 14, 116, 26, "#343a40", r=5, z=2)
    txt(ax, W - 76, 27, "Déconnexion", 10.5, WHITE, ha="center")


def badge(ax, x, y, label, color, w=58, h=22):
    rrect(ax, x, y, w, h, color, r=6, z=3)
    tc = "#212529" if color == WARNING else WHITE
    txt(ax, x + w / 2, y + h / 2 + 1, label, 10.5, tc, True, ha="center")


# ----------------------- Page : Tableau de bord ------------------------ #
def page_dashboard(chemin):
    fig, ax = new_fig()
    navbar(ax, "Tableau de bord")
    icone(ax, 24, 70, "#0d3b66", 18); txt(ax, 52, 78, "Tableau de bord", 21, "#0d3b66", True)

    # --- 4 cartes KPI ---
    cartes = [
        ("Équipements supervisés", str(TOTAL), PRIMARY),
        ("En ligne (UP)", str(NB_UP), SUCCESS),
        ("Hors ligne (DOWN)", str(NB_DOWN), DANGER),
        ("Alertes actives", "2", WARNING),
    ]
    m, gap = 24, 18
    cw = (W - 2 * m - 3 * gap) / 4
    cy, ch = 102, 92
    for i, (titre, val, coul) in enumerate(cartes):
        cx = m + i * (cw + gap)
        rrect(ax, cx, cy, cw, ch, coul, r=10, z=1)
        tc = "#212529" if coul == WARNING else WHITE
        txt(ax, cx + 18, cy + 26, titre, 12, tc, True)
        txt(ax, cx + 18, cy + 62, val, 34, tc, True)

    # --- Carte gauche : anneau de disponibilité ---
    gy, gh = 214, 250
    gw = 500
    rrect(ax, m, gy, gw, gh, WHITE, r=10, ec=BORDER, lw=1, z=1)
    txt(ax, m + 18, gy + 26, f"Disponibilité globale : {DISPO} %", 13, TXT, True)
    ax.add_patch(Rectangle((m, gy + 44), gw, 1.4, color="#f0f0f0", zorder=2))
    # anneau (doughnut) via axes encart
    axd = fig.add_axes([(m + 60) / W, 1 - (gy + gh - 12) / H, 168 / W, 168 / H])
    axd.pie([NB_UP, NB_DOWN], colors=[SUCCESS, DANGER], startangle=90,
            wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
    axd.set_aspect("equal"); axd.patch.set_visible(False)
    axd.text(0, 0.12, f"{DISPO}%", fontsize=20, color="#0d3b66",
             fontweight="bold", ha="center", va="center")
    axd.text(0, -0.28, "disponible", fontsize=10, color=MUTED, ha="center", va="center")
    # légende
    lx = m + 270
    badge(ax, lx, gy + 95, "", SUCCESS, w=18, h=18)
    txt(ax, lx + 28, gy + 104, f"En ligne (UP) — {NB_UP}", 12, TXT)
    badge(ax, lx, gy + 135, "", DANGER, w=18, h=18)
    txt(ax, lx + 28, gy + 144, f"Hors ligne (DOWN) — {NB_DOWN}", 12, TXT)

    # --- Carte droite : alertes actives ---
    ax2 = m + gw + gap
    aw = W - ax2 - m
    rrect(ax, ax2, gy, aw, gh, WHITE, r=10, ec=BORDER, lw=1, z=1)
    icone(ax, ax2 + 18, gy + 16, DANGER, 14); txt(ax, ax2 + 40, gy + 26, "Alertes actives", 13, DANGER, True)
    ax.add_patch(Rectangle((ax2, gy + 44), aw, 1.4, color="#f0f0f0", zorder=2))
    cols = [("Équipement", ax2 + 18), ("Type", ax2 + 300),
            ("Sévérité", ax2 + 470), ("Date", ax2 + 600)]
    for c, cx in cols:
        txt(ax, cx, gy + 62, c, 11.5, MUTED, True)
    ry = gy + 88
    for nom, ip, typ, sev, date in ALERTES:
        txt(ax, ax2 + 18, ry, nom, 12, TXT, True)
        txt(ax, ax2 + 18, ry + 17, ip, 10, MUTED)
        txt(ax, ax2 + 300, ry + 6, typ, 11, TXT)
        badge(ax, ax2 + 470, ry - 4, sev, DANGER, w=78)
        txt(ax, ax2 + 600, ry + 6, date, 11, TXT)
        ry += 52
        ax.add_patch(Rectangle((ax2 + 14, ry - 16), aw - 28, 1, color="#f3f3f3", zorder=2))

    # --- Table : état des équipements ---
    ty = gy + gh + 16
    th = H - ty - 16
    rrect(ax, m, ty, W - 2 * m, th, WHITE, r=10, ec=BORDER, lw=1, z=1)
    icone(ax, m + 18, ty + 14, PRIMARY, 14); txt(ax, m + 40, ty + 24, "État des équipements", 13, TXT, True)
    # en-tête
    hy = ty + 48
    ax.add_patch(Rectangle((m, hy - 16), W - 2 * m, 30, color=LIGHT, zorder=2))
    colonnes = [("Nom", m + 18), ("Adresse IP", m + 260), ("Type", m + 470),
                ("Statut", m + 650), ("Latence", m + 800), ("Dernière vérif.", m + 950)]
    for c, cx in colonnes:
        txt(ax, cx, hy, c, 11.5, "#495057", True)
    ry = hy + 34
    for nom, ip, typ, statut, lat, vu in EQUIPEMENTS:
        txt(ax, m + 18, ry, nom, 12, TXT)
        txt(ax, m + 260, ry, ip, 11.5, PURPLE, family="DejaVu Sans Mono")
        txt(ax, m + 470, ry, typ, 12, TXT)
        badge(ax, m + 650, ry - 11, statut, SUCCESS if statut == "UP" else DANGER, w=64)
        txt(ax, m + 800, ry, lat, 12, TXT)
        txt(ax, m + 950, ry, "10/06 " + vu, 11.5, MUTED)
        ry += 34
        ax.add_patch(Rectangle((m + 14, ry - 17), W - 2 * m - 28, 1, color="#f1f1f1", zorder=2))

    fig.savefig(chemin, dpi=100); plt.close(fig)
    print("Capture générée :", chemin)


# ----------------------- Page générique à table ----------------------- #
def page_table(chemin, page, titre_icone, colonnes, largeurs, lignes, badges_col=None):
    fig, ax = new_fig()
    navbar(ax, page)
    titre_propre = titre_icone.split("  ", 1)[-1]  # retire l'emoji éventuel
    icone(ax, 24, 70, "#0d3b66", 18); txt(ax, 52, 78, titre_propre, 21, "#0d3b66", True)
    ty, m = 102, 24
    th = H - ty - 16
    rrect(ax, m, ty, W - 2 * m, th, WHITE, r=10, ec=BORDER, lw=1, z=1)
    hy = ty + 34
    ax.add_patch(Rectangle((m, hy - 18), W - 2 * m, 32, color=LIGHT, zorder=2))
    xs = []
    cx = m + 18
    for c, lw in zip(colonnes, largeurs):
        txt(ax, cx, hy, c, 12, "#495057", True); xs.append(cx); cx += lw
    ry = hy + 40
    for li, ligne in enumerate(lignes):
        for ci, val in enumerate(ligne):
            if badges_col and ci in badges_col:
                coul = badges_col[ci](val)
                badge(ax, xs[ci], ry - 12, val, coul, w=max(64, len(val) * 9 + 26))
            else:
                mono = (ci == 1 and val.count(".") == 3)
                txt(ax, xs[ci], ry, val, 12, PURPLE if mono else TXT,
                    family="DejaVu Sans Mono" if mono else "DejaVu Sans")
        ry += 40
        ax.add_patch(Rectangle((m + 14, ry - 20), W - 2 * m - 28, 1, color="#f1f1f1", zorder=2))
    fig.savefig(chemin, dpi=100); plt.close(fig)
    print("Capture générée :", chemin)


# ----------------------- Page : notification Telegram ------------------ #
def page_telegram(chemin):
    fig = plt.figure(figsize=(4.6, 8.4), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 460); ax.set_ylim(0, 840)
    ax.axis("off"); ax.invert_yaxis()
    ax.add_patch(Rectangle((0, 0), 460, 840, color="#0e1621", zorder=0))  # fond Telegram
    # en-tête chat
    ax.add_patch(Rectangle((0, 0), 460, 70, color="#17212b", zorder=1))
    ax.add_patch(Circle((40, 35), 20, color="#0d6efd", zorder=2))
    txt(ax, 40, 36, "OM", 13, WHITE, True, ha="center")
    txt(ax, 75, 28, "Supervision OPEN MOISE", 14, WHITE, True)
    txt(ax, 75, 48, "bot", 11, "#6d7f8f")
    # bulle d'alerte
    bx, by, bw = 24, 110, 380
    msgs = [
        ("ALERTE SUPERVISION", True, "#ff5c5c", DANGER),
        ("", False, WHITE, None),
        ("Équipement : Serveur-BDD", False, WHITE, None),
        ("IP : 192.168.1.11", False, "#9fb4c7", None),
        ("Type : PANNE_RESEAU", False, WHITE, None),
        ("Sévérité : CRITIQUE", True, "#ff8a8a", None),
        ("Détail : Serveur-BDD (192.168.1.11)", False, WHITE, None),
        ("ne répond plus après 2 tentatives.", False, WHITE, None),
    ]
    bh = 36 + len(msgs) * 26
    rrect(ax, bx, by, bw, bh, "#182533", r=12, z=2)
    yy = by + 28
    for s, b, c, dot in msgs:
        if dot:
            ax.add_patch(Circle((bx + 26, yy), 7, color=dot, zorder=3))
            txt(ax, bx + 40, yy, s, 12.5, c, b)
        else:
            txt(ax, bx + 20, yy, s, 12.5, c, b)
        yy += 26
    txt(ax, bx + bw - 20, by + bh - 14, "11:20  OK", 10, "#5b6b7a", ha="right")
    # 2e notif rétablissement
    by2 = by + bh + 20
    bh2 = 30 + 2 * 26
    rrect(ax, bx, by2, bw, bh2, "#182533", r=12, z=2)
    ax.add_patch(Circle((bx + 26, by2 + 26), 7, color=PRIMARY, zorder=3))
    txt(ax, bx + 40, by2 + 26, "RÉTABLISSEMENT", 12.5, "#5ab0ff", True)
    txt(ax, bx + 20, by2 + 52, "Serveur-BDD est de nouveau en ligne.", 12.5, WHITE)
    txt(ax, bx + bw - 20, by2 + bh2 - 14, "11:27  OK", 10, "#5b6b7a", ha="right")
    fig.savefig(chemin, dpi=100); plt.close(fig)
    print("Capture générée :", chemin)


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captures")
    os.makedirs(base, exist_ok=True)

    page_dashboard(os.path.join(base, "capture-dashboard.png"))

    sev_color = lambda v: {"CRITIQUE": DANGER, "AVERTISSEMENT": WARNING, "INFO": PRIMARY}.get(v, MUTED)
    statut_color = lambda v: SUCCESS if v == "UP" else DANGER
    etat_color = lambda v: SUCCESS if v == "Actif" else MUTED

    page_table(
        os.path.join(base, "capture-equipements.png"),
        "Équipements", "🖥️  Gestion des équipements",
        ["Nom", "Adresse IP", "Type", "Emplacement", "Statut", "Actif"],
        [240, 200, 170, 230, 160, 120],
        [(e[0], e[1], e[2], "Datacenter" if "Serveur" in e[2] else "Site client",
          e[3], "Actif") for e in EQUIPEMENTS],
        badges_col={4: statut_color},
    )

    page_table(
        os.path.join(base, "capture-alertes.png"),
        "Alertes", "🔔  Historique des alertes",
        ["Date", "Équipement", "Adresse IP", "Type", "Sévérité", "État"],
        [180, 230, 200, 230, 160, 150],
        [
            ("10/06 11:20", "Serveur-BDD", "192.168.1.11", "PANNE_RESEAU", "CRITIQUE", "En attente"),
            ("10/06 11:18", "Imprimante-RH", "192.168.1.30", "PANNE_RESEAU", "CRITIQUE", "En attente"),
            ("10/06 09:05", "Serveur-Web", "192.168.1.10", "SERVICE_INDISPONIBLE", "CRITIQUE", "Acquittée"),
            ("09/06 22:41", "Point-Acces-WiFi", "192.168.1.20", "PANNE_RESEAU", "AVERTISSEMENT", "Acquittée"),
            ("09/06 16:12", "Serveur-BDD", "192.168.1.11", "RETABLISSEMENT", "INFO", "Acquittée"),
        ],
        badges_col={4: sev_color},
    )

    page_telegram(os.path.join(base, "capture-telegram.png"))
    print("Toutes les captures ont été générées dans :", base)
