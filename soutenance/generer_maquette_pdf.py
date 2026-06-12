# -*- coding: utf-8 -*-
"""
generer_maquette_pdf.py
=======================
Assemble les captures d'écran du prototype en un document PDF (A4 paysage) :
page de garde + un écran par page (titre + capture + légende), style CERCO.

Prérequis : Pillow.
Sortie : soutenance/Maquette-Prototype.pdf
"""
import os
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
CAPT = os.path.join(ICI, "captures")
OUT = os.path.join(ICI, "Maquette-Prototype.pdf")

# A4 paysage à 150 dpi
W, H = 1754, 1240
NAVY = (0x0A, 0x23, 0x42); TEAL = (0x2E, 0xC4, 0xB6); MINT = (0x5F, 0xE3, 0xD3)
BG = (0xF4, 0xF8, 0xFB); WHITE = (255, 255, 255); LIGHT = (0xC7, 0xD7, 0xE2)
BORDER = (0xD0, 0xDB, 0xE6); GREY = (0x55, 0x66, 0x77)

FT = "/usr/local/lib/python3.11/dist-packages/matplotlib/mpl-data/fonts/ttf/"
def f(n, s): return ImageFont.truetype(FT + n, s)
F_BRAND = f("DejaVuSans-Bold.ttf", 24)
F_KICK = f("DejaVuSans-Bold.ttf", 20)
F_CAP = f("DejaVuSans-Bold.ttf", 30)
F_SUB = f("DejaVuSans.ttf", 22)
F_BADGE = f("DejaVuSans-Bold.ttf", 34)
F_BIG = f("DejaVuSans-Bold.ttf", 52)
F_SMALL = f("DejaVuSans.ttf", 20)


def center(d, x0, x1, y, t, fnt, fill):
    w = d.textbbox((0, 0), t, font=fnt)[2]
    d.text(((x0 + x1 - w) / 2, y), t, font=fnt, fill=fill)


def page_ecran(num, titre, sous, capture):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # bandeau marque
    d.rectangle([0, 0, W, 78], fill=NAVY)
    d.rectangle([36, 26, 62, 52], fill=TEAL)
    d.text((76, 26), "SupervisionNet — Maquette du prototype", font=F_BRAND, fill=WHITE)
    k = "DÉMONSTRATION"
    kw = d.textbbox((0, 0), k, font=F_KICK)[2]
    d.text((W - kw - 36, 30), k, font=F_KICK, fill=MINT)
    # capture
    cap = Image.open(os.path.join(CAPT, capture)).convert("RGB")
    maxw, maxh = W - 180, H - 78 - 130 - 40
    r = min(maxw / cap.width, maxh / cap.height)
    cw, ch = int(cap.width * r), int(cap.height * r)
    cap = cap.resize((cw, ch), Image.LANCZOS)
    cx, cy = (W - cw) // 2, 78 + (H - 78 - 130 - ch) // 2
    d.rectangle([cx - 8, cy - 8, cx + cw + 8, cy + ch + 8], fill=WHITE, outline=BORDER, width=2)
    img.paste(cap, (cx, cy))
    # légende
    by = H - 130
    d.rectangle([0, by, W, H], fill=NAVY)
    d.rounded_rectangle([36, by + 34, 100, by + 98], radius=10, fill=TEAL)
    bw = d.textbbox((0, 0), str(num), font=F_BADGE)[2]
    d.text((36 + (64 - bw) / 2, by + 44), str(num), font=F_BADGE, fill=NAVY)
    d.text((124, by + 32), titre, font=F_CAP, fill=WHITE)
    d.text((124, by + 78), sous, font=F_SUB, fill=LIGHT)
    return img


def page_garde():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.ellipse([W - 330, -160, W + 110, 280], fill=(0x13, 0x3B, 0x5C))
    d.ellipse([-150, H - 300, 300, H + 150], fill=(0x13, 0x3B, 0x5C))
    d.ellipse([W - 200, -50, W - 20, 130], fill=(0x1C, 0x7C, 0x84))
    y = 300
    center(d, 0, W, y, "MÉMOIRE DE PROJET DE FIN D'ÉTUDES — MASTER 2 RIT", F_KICK, MINT); y += 70
    center(d, 0, W, y, "Maquette du prototype", F_BIG, WHITE); y += 70
    center(d, 0, W, y, "Automatisation de la Supervision et de la", F_SUB, LIGHT); y += 36
    center(d, 0, W, y, "Détection des Pannes Réseau", F_SUB, LIGHT); y += 60
    d.rectangle([W/2 - 110, y, W/2 + 110, y + 6], fill=TEAL); y += 50
    center(d, 0, W, y, "Écrans du tableau de bord — solution open-source", F_SUB, LIGHT); y += 70
    center(d, 0, W, y, "KOUASSI Yoo Nyong Kra Espérance", F_SMALL, WHITE); y += 34
    center(d, 0, W, y, "Année académique 2025 – 2026", F_SMALL, MINT)
    return img


pages = [page_garde()]
pages.append(page_ecran(1, "Connexion sécurisée",
            "Accès authentifié au tableau de bord (mots de passe hachés).", "capture-login.png"))
pages.append(page_ecran(2, "Tableau de bord temps réel",
            "KPI, anneau de disponibilité (75 %), 2 équipements en panne (DOWN).", "capture-dashboard.png"))
pages.append(page_ecran(3, "Alerte instantanée (Telegram + e-mail)",
            "L'astreinte est notifiée en moins de 2 minutes, où qu'elle soit.", "capture-telegram.png"))
pages.append(page_ecran(4, "Historique des alertes",
            "Traçabilité, sévérités et acquittement — preuve du respect des SLA.", "capture-alertes.png"))
pages.append(page_ecran(5, "Gestion des équipements",
            "Inventaire du parc et découverte automatique (scan CIDR).", "capture-equipements.png"))
pages.append(page_ecran(6, "Rapports & statistiques",
            "Taux de disponibilité, latence moyenne et graphiques exportables.", "capture-rapports.png"))

# Sauvegarde sans perte via img2pdf (Pillow ne dispose pas de l'encodeur JPEG ici)
import img2pdf
tmp = []
tdir = os.path.join(ICI, "_maquette_png")
os.makedirs(tdir, exist_ok=True)
for i, pg in enumerate(pages):
    p = os.path.join(tdir, f"p{i:02d}.png")
    pg.save(p); tmp.append(p)
# A4 paysage
a4 = (img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(210))
layout = img2pdf.get_layout_fun(a4)
with open(OUT, "wb") as fp:
    fp.write(img2pdf.convert(tmp, layout_fun=layout))
for p in tmp:
    os.remove(p)
os.rmdir(tdir)
print("PDF généré :", OUT, "(", len(pages), "pages )")
