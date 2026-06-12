# -*- coding: utf-8 -*-
"""
generer_video_demo.py
=====================
Compose une vidéo de démonstration du prototype (maquette) à partir des
captures d'écran. Chaque scène = bandeau de titre + capture + légende, puis
assemblage avec fondus enchaînés (ffmpeg xfade).

Prérequis : Pillow, ffmpeg.
Sortie : soutenance/video/demo-prototype.mp4
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
CAPT = os.path.join(ICI, "captures")
OUTDIR = os.path.join(ICI, "video")
FRAMES = os.path.join(OUTDIR, "_frames")
os.makedirs(FRAMES, exist_ok=True)

W, H = 1920, 1080
NAVY = (0x0A, 0x23, 0x42); TEAL = (0x2E, 0xC4, 0xB6); MINT = (0x5F, 0xE3, 0xD3)
BG = (0xF4, 0xF8, 0xFB); WHITE = (255, 255, 255); LIGHT = (0xC7, 0xD7, 0xE2)
BORDER = (0xD0, 0xDB, 0xE6)

FT = "/usr/local/lib/python3.11/dist-packages/matplotlib/mpl-data/fonts/ttf/"
def font(name, size): return ImageFont.truetype(FT + name, size)
F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_BRAND = font("DejaVuSans-Bold.ttf", 26)
F_KICK = font("DejaVuSans-Bold.ttf", 22)
F_CAP = font("DejaVuSans-Bold.ttf", 34)
F_SUB = font("DejaVuSans.ttf", 26)
F_BADGE = font("DejaVuSans-Bold.ttf", 40)
F_BIG = font("DejaVuSans-Bold.ttf", 64)
F_SMALL = font("DejaVuSans.ttf", 22)


def center(draw, x0, x1, y, text, fnt, fill):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def scene(num, titre, sous, capture, fichier):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # bandeau supérieur (marque)
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([40, 30, 70, 62], fill=TEAL)
    d.text((86, 30), "SupervisionNet", font=F_BRAND, fill=WHITE)
    kick = "DÉMONSTRATION DU PROTOTYPE"
    kw = d.textbbox((0, 0), kick, font=F_KICK)[2]
    d.text((W - kw - 40, 36), kick, font=F_KICK, fill=MINT)
    # capture centrée dans une carte blanche
    cap = Image.open(os.path.join(CAPT, capture)).convert("RGB")
    maxw, maxh = W - 220, H - 92 - 150 - 60
    r = min(maxw / cap.width, maxh / cap.height)
    cw, ch = int(cap.width * r), int(cap.height * r)
    cap = cap.resize((cw, ch), Image.LANCZOS)
    cx, cy = (W - cw) // 2, 92 + (H - 92 - 150 - ch) // 2
    d.rectangle([cx - 10, cy - 10, cx + cw + 10, cy + ch + 10], fill=WHITE, outline=BORDER, width=2)
    img.paste(cap, (cx, cy))
    # bandeau de légende (bas)
    by = H - 150
    d.rectangle([0, by, W, H], fill=NAVY)
    # badge numéro
    d.rounded_rectangle([40, by + 38, 116, by + 114], radius=12, fill=TEAL)
    bw = d.textbbox((0, 0), str(num), font=F_BADGE)[2]
    d.text((40 + (76 - bw) / 2, by + 50), str(num), font=F_BADGE, fill=NAVY)
    d.text((150, by + 36), titre, font=F_CAP, fill=WHITE)
    d.text((150, by + 88), sous, font=F_SUB, fill=LIGHT)
    img.save(os.path.join(FRAMES, fichier))


def card(fichier, lignes):
    """Carte pleine (titre / fin) sur fond marine avec cercles décoratifs."""
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.ellipse([W - 360, -180, W + 120, 300], fill=(0x13, 0x3B, 0x5C))
    d.ellipse([-160, H - 320, 320, H + 160], fill=(0x13, 0x3B, 0x5C))
    d.ellipse([W - 220, -60, W - 20, 140], fill=(0x1C, 0x7C, 0x84))
    y = 360
    for txt, kind in lignes:
        if kind == "kick":
            center(d, 0, W, y, txt, F_KICK, MINT); y += 70
        elif kind == "big":
            # multi-ligne centrée
            for part in txt.split("\n"):
                center(d, 0, W, y, part, F_BIG, WHITE); y += 80
            y += 10
        elif kind == "sub":
            center(d, 0, W, y, txt, F_SUB, LIGHT); y += 50
        elif kind == "bar":
            d.rectangle([W/2 - 120, y, W/2 + 120, y + 6], fill=TEAL); y += 40
        elif kind == "small":
            center(d, 0, W, y, txt, F_SMALL, LIGHT); y += 36
    img.save(os.path.join(FRAMES, fichier))


# ---------------------------------------------------------------------- #
# Construction des scènes                                                 #
# ---------------------------------------------------------------------- #
SCENES = []  # (fichier, durée s)

card("00_intro.png", [
    ("MÉMOIRE DE PROJET DE FIN D'ÉTUDES — MASTER 2 RIT", "kick"),
    ("Automatisation de la Supervision\net de la Détection des Pannes Réseau", "big"),
    ("", "bar"),
    ("Démonstration du prototype (maquette) — solution open-source", "sub"),
    ("KOUASSI Yoo Nyong Kra Espérance", "small"),
])
SCENES.append(("00_intro.png", 4.5))

scene(1, "Connexion sécurisée", "Accès authentifié au tableau de bord (mots de passe hachés).",
      "capture-login.png", "01_login.png"); SCENES.append(("01_login.png", 4.5))

scene(2, "Tableau de bord temps réel",
      "Vue d'ensemble : KPI, disponibilité 75 %, 2 équipements en panne (DOWN).",
      "capture-dashboard.png", "02_dashboard.png"); SCENES.append(("02_dashboard.png", 6))

scene(3, "Alerte instantanée (Telegram + e-mail)",
      "L'astreinte est notifiée en moins de 2 minutes, où qu'elle soit.",
      "capture-telegram.png", "03_telegram.png"); SCENES.append(("03_telegram.png", 5.5))

scene(4, "Historique des alertes",
      "Traçabilité, sévérités et acquittement — preuve du respect des SLA.",
      "capture-alertes.png", "04_alertes.png"); SCENES.append(("04_alertes.png", 5))

scene(5, "Gestion des équipements",
      "Inventaire du parc, découverte automatique (scan CIDR), services supervisés.",
      "capture-equipements.png", "05_equipements.png"); SCENES.append(("05_equipements.png", 5))

scene(6, "Rapports & statistiques",
      "Taux de disponibilité, latence moyenne et graphiques exportables.",
      "capture-rapports.png", "06_rapports.png"); SCENES.append(("06_rapports.png", 5))

card("07_fin.png", [
    ("DE LA SUPERVISION RÉACTIVE VERS LA SUPERVISION PROACTIVE", "kick"),
    ("Merci de votre attention", "big"),
    ("", "bar"),
    ("Pile open-source : Ubuntu · Python · Cron · MySQL · Flask · Telegram", "sub"),
    ("Détection < 2 min   •   Coût de licence : 0 FCFA", "small"),
])
SCENES.append(("07_fin.png", 5))

print("Scènes composées :", len(SCENES))

# ---------------------------------------------------------------------- #
# Assemblage ffmpeg avec fondus enchaînés (xfade)                         #
# ---------------------------------------------------------------------- #
T = 0.7  # durée de transition
inputs = []
for f, dur in SCENES:
    inputs += ["-loop", "1", "-t", str(dur), "-i", os.path.join(FRAMES, f)]

n = len(SCENES)
# pré-normalisation de chaque entrée
fc = []
for i in range(n):
    fc.append(f"[{i}:v]format=yuv420p,fps=30,scale={W}:{H},setsar=1[v{i}]")
# chaîne xfade
prev = "v0"
offset = 0.0
for i in range(1, n):
    offset += SCENES[i - 1][1] - T
    out = f"x{i}"
    fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={T}:offset={offset:.3f}[{out}]")
    prev = out
filtre = ";".join(fc)

os.makedirs(OUTDIR, exist_ok=True)
out_mp4 = os.path.join(OUTDIR, "demo-prototype.mp4")
cmd = (["ffmpeg", "-y"] + inputs +
       ["-filter_complex", filtre, "-map", f"[{prev}]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-movflags", "+faststart", out_mp4])
print("Assemblage ffmpeg…")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr[-1500:])
else:
    print("Vidéo générée :", out_mp4)
