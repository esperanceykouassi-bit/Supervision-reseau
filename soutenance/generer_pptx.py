# -*- coding: utf-8 -*-
"""
generer_pptx.py
===============
Génère le support de soutenance au format PowerPoint (.pptx) ÉDITABLE.

Le fichier produit (« presentation-projet.pptx ») suit le canevas
mémoire-projet en 12 sections. Chaque diapositive contient un titre, un
contenu structuré (puces / tableaux) et les NOTES DE L'ORATEUR.

Utilisation :
    pip install python-pptx
    python generer_pptx.py
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

# Racine du dépôt (pour retrouver les images des diagrammes).
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------- #
# Charte graphique                                                       #
# ---------------------------------------------------------------------- #
BLEU_FONCE = RGBColor(0x0D, 0x3B, 0x66)   # titres
BLEU = RGBColor(0x0D, 0x6E, 0xFD)         # accents
ROUGE = RGBColor(0xD6, 0x28, 0x28)        # emphase
GRIS = RGBColor(0x33, 0x33, 0x33)         # texte
GRIS_CLAIR = RGBColor(0xF1, 0xF3, 0xF5)   # fonds
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
VERT = RGBColor(0x19, 0x87, 0x54)

# Format 16:9
LARGEUR = Inches(13.333)
HAUTEUR = Inches(7.5)

prs = Presentation()
prs.slide_width = LARGEUR
prs.slide_height = HAUTEUR

LAYOUT_VIDE = prs.slide_layouts[6]  # diapositive vierge


# ---------------------------------------------------------------------- #
# Fonctions utilitaires de mise en page                                  #
# ---------------------------------------------------------------------- #
def ajouter_diapo():
    return prs.slides.add_slide(LAYOUT_VIDE)


def fond(slide, couleur=BLANC):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = couleur


def rectangle(slide, x, y, w, h, couleur):
    from pptx.enum.shapes import MSO_SHAPE
    forme = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    forme.fill.solid()
    forme.fill.fore_color.rgb = couleur
    forme.line.fill.background()
    forme.shadow.inherit = False
    return forme


def zone_texte(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tb.text_frame.word_wrap = True
    return tb


def style_run(run, taille=18, gras=False, couleur=GRIS, italique=False):
    run.font.size = Pt(taille)
    run.font.bold = gras
    run.font.italic = italique
    run.font.color.rgb = couleur
    run.font.name = "Calibri"


def notes(slide, texte):
    slide.notes_slide.notes_text_frame.text = texte


def bandeau_titre(slide, numero, titre):
    """Bandeau d'en-tête coloré avec numéro de section et titre."""
    rectangle(slide, 0, 0, LARGEUR, Inches(1.15), BLEU_FONCE)
    if numero:
        # pastille numéro
        from pptx.enum.shapes import MSO_SHAPE
        past = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.35), Inches(0.22),
                                      Inches(0.72), Inches(0.72))
        past.fill.solid(); past.fill.fore_color.rgb = BLEU
        past.line.fill.background(); past.shadow.inherit = False
        tf = past.text_frame; tf.word_wrap = False
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(numero)
        style_run(r, 26, True, BLANC)
        tx = Inches(1.25)
    else:
        tx = Inches(0.5)
    tb = zone_texte(slide, tx, Inches(0.18), LARGEUR - tx - Inches(0.3), Inches(0.8))
    tb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tb.text_frame.paragraphs[0]
    r = p.add_run(); r.text = titre
    style_run(r, 30, True, BLANC)


def puces(slide, items, x=Inches(0.7), y=Inches(1.5),
          w=Inches(11.9), h=Inches(5.4), taille=20, interligne=8):
    """Ajoute une liste à puces. `items` = liste de (texte, niveau, gras, couleur)."""
    tb = zone_texte(slide, x, y, w, h)
    tf = tb.text_frame
    first = True
    for item in items:
        texte = item[0]
        niveau = item[1] if len(item) > 1 else 0
        gras = item[2] if len(item) > 2 else False
        couleur = item[3] if len(item) > 3 else GRIS
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = niveau
        p.space_after = Pt(interligne)
        puce = "•  " if niveau == 0 else "–  "
        if texte == "":
            puce = ""
        r = p.add_run(); r.text = puce + texte
        style_run(r, taille - niveau * 2, gras, couleur)
    return tb


def tableau(slide, donnees, x=Inches(0.7), y=Inches(1.5),
            w=Inches(11.9), h=Inches(5.0), taille=15, surligne_derniere_col=False):
    """Crée un tableau stylé. `donnees` = liste de lignes (listes de cellules)."""
    nb_lignes = len(donnees)
    nb_cols = len(donnees[0])
    g = slide.shapes.add_table(nb_lignes, nb_cols, x, y, w, h).table
    for j, cell_txt in enumerate(donnees[0]):
        cell = g.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = BLEU_FONCE
        p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(cell_txt)
        style_run(r, taille, True, BLANC)
    for i in range(1, nb_lignes):
        for j in range(nb_cols):
            cell = g.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BLANC if i % 2 else GRIS_CLAIR
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(donnees[i][j])
            couleur = GRIS
            gras = False
            if surligne_derniere_col and j == nb_cols - 1:
                couleur = VERT; gras = True
            style_run(r, taille, gras, couleur)
    return g


def encadre(slide, texte, x=Inches(0.7), y=Inches(5.9),
            w=Inches(11.9), h=Inches(1.0), fond_c=GRIS_CLAIR, barre=BLEU):
    """Encadré « citation / message clé » avec barre latérale."""
    rectangle(slide, x, y, Inches(0.12), h, barre)
    boite = rectangle(slide, x + Inches(0.12), y, w - Inches(0.12), h, fond_c)
    tf = boite.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.2)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = texte
    style_run(r, 17, True, BLEU_FONCE, italique=True)


def _dim_ajustee(chemin, max_w, max_h):
    """Retourne (largeur, hauteur) en EMU pour faire tenir l'image en gardant
    le ratio d'aspect dans la boîte (max_w x max_h)."""
    iw, ih = Image.open(chemin).size
    aspect = iw / ih
    w = max_w
    h = int(w / aspect)
    if h > max_h:
        h = max_h
        w = int(h * aspect)
    return w, h


def diapo_image(numero, titre, chemin, legende="", note_txt="",
                max_w=Inches(11.8), max_h=Inches(5.3), top=Inches(1.35),
                fond_clair=True):
    """Crée une diapositive « titre + image centrée » (diagramme pleine page)."""
    s = ajouter_diapo(); fond(s, BLANC if fond_clair else GRIS_CLAIR)
    bandeau_titre(s, numero, titre)
    chemin = os.path.join(RACINE, chemin)
    w, h = _dim_ajustee(chemin, int(max_w), int(max_h))
    left = int((int(LARGEUR) - w) / 2)
    s.shapes.add_picture(chemin, left, top, width=w, height=h)
    if legende:
        tb = zone_texte(s, Inches(0.5), Inches(6.75), Inches(12.3), Inches(0.5))
        p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = legende
        style_run(r, 13, False, GRIS, italique=True)
    if note_txt:
        notes(s, note_txt)
    return s


def diapo_deux_images(numero, titre, g_chemin, g_lbl, d_chemin, d_lbl, note_txt=""):
    """Crée une diapositive avec deux images côte à côte (ex. MCD | MLD)."""
    s = ajouter_diapo(); fond(s)
    bandeau_titre(s, numero, titre)
    for chemin, lbl, x in [(g_chemin, g_lbl, Inches(0.4)),
                           (d_chemin, d_lbl, Inches(6.9))]:
        # libellé
        tb = zone_texte(s, x, Inches(1.3), Inches(6.0), Inches(0.4))
        p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = lbl
        style_run(r, 16, True, BLEU_FONCE)
        # image
        ch = os.path.join(RACINE, chemin)
        w, h = _dim_ajustee(ch, int(Inches(5.9)), int(Inches(5.0)))
        left = int(x) + int((int(Inches(6.0)) - w) / 2)
        s.shapes.add_picture(ch, left, Inches(1.75), width=w, height=h)
    if note_txt:
        notes(s, note_txt)
    return s


def diapo_grille_images(numero, titre, items, note_txt=""):
    """Grille d'aperçus (4 colonnes). items = liste de (chemin, label)."""
    s = ajouter_diapo(); fond(s)
    bandeau_titre(s, numero, titre)
    cols = 4
    cell_w = Inches(3.0)
    cell_h = Inches(2.35)
    x0, y0 = Inches(0.35), Inches(1.45)
    gx, gy = Inches(0.18), Inches(0.55)
    for idx, (chemin, label) in enumerate(items):
        col = idx % cols
        row = idx // cols
        cx = int(x0) + col * (int(cell_w) + int(gx))
        cy = int(y0) + row * (int(cell_h) + int(gy))
        ch = os.path.join(RACINE, chemin)
        w, h = _dim_ajustee(ch, int(cell_w), int(cell_h))
        left = cx + int((int(cell_w) - w) / 2)
        s.shapes.add_picture(ch, left, cy, width=w, height=h)
        tb = zone_texte(s, cx, cy + int(cell_h) + Inches(0.02), cell_w, Inches(0.4))
        p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = label
        style_run(r, 11, True, BLEU_FONCE)
    if note_txt:
        notes(s, note_txt)
    return s


# ====================================================================== #
#  DIAPO 0 — TITRE                                                       #
# ====================================================================== #
s = ajouter_diapo(); fond(s, BLEU_FONCE)
rectangle(s, 0, Inches(2.5), LARGEUR, Inches(2.6), BLEU)
tb = zone_texte(s, Inches(0.8), Inches(2.65), Inches(11.7), Inches(2.3))
tf = tb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Automatisation de la Supervision et de la\nDétection des Pannes Réseau"
style_run(r, 36, True, BLANC)
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
r = p2.add_run(); r.text = "Une solution open-source pour une infrastructure toujours disponible"
style_run(r, 18, False, RGBColor(0xDD, 0xE6, 0xF2), italique=True)
tb = zone_texte(s, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.6))
for i, (txt, sz, g) in enumerate([
    ("[NOM Prénom] — Master 2 RIT", 20, True),
    ("Sous la direction de [Directeur de mémoire]", 16, False),
    ("Structure d'accueil : OPEN MOISE  •  Année académique 2025–2026", 14, False),
]):
    p = tf2 = (s.shapes[-1].text_frame.paragraphs[0] if i == 0 else s.shapes[-1].text_frame.add_paragraph())
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = txt
    style_run(r, sz, g, BLANC)
notes(s, "Bonjour Mesdames et Messieurs les membres du jury. Je vous remercie de "
         "votre présence. Je vais vous présenter mon mémoire-projet : une solution "
         "d'automatisation de la supervision et de la détection des pannes réseau, "
         "pensée comme un véritable produit, du besoin du marché au modèle économique.")

# ====================================================================== #
#  DIAPO 1 — PLAN                                                        #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, None, "Plan de la présentation")
gauche = [
    ("Introduction — L'annonce du sujet", 0, True, BLEU_FONCE),
    ("1.  Contexte et identification du problème", 0, False, GRIS),
    ("2.  Objectifs et résultats attendus", 0, False, GRIS),
    ("3.  Démarche méthodologique", 0, False, GRIS),
    ("4.  État des lieux & solution proposée", 0, False, GRIS),
    ("5.  Axe de différenciation (innovation)", 0, False, GRIS),
    ("6.  Étude de faisabilité & conception", 0, False, GRIS),
]
droite = [
    ("7.  Fonctionnement technique", 0, False, GRIS),
    ("8.  Démonstration", 0, True, ROUGE),
    ("9.  Marketing, vente & concurrence", 0, False, GRIS),
    ("10. Prévisions financières", 0, False, GRIS),
    ("11. Limites & perspectives", 0, False, GRIS),
    ("", 0, False, GRIS),
    ("Conclusion", 0, True, BLEU_FONCE),
]
puces(s, gauche, x=Inches(0.7), y=Inches(1.6), w=Inches(6.0), taille=20, interligne=12)
puces(s, droite, x=Inches(6.9), y=Inches(1.6), w=Inches(6.0), taille=20, interligne=12)
notes(s, "Mon exposé suit le fil d'un projet d'entreprise : je pars du problème du "
         "marché, je présente la solution et sa technique, je la démontre, puis "
         "j'aborde son modèle économique avant de conclure sur les perspectives.")

# ====================================================================== #
#  INTRODUCTION                                                          #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, None, "Introduction — L'annonce du sujet")
puces(s, [
    ("Le sujet : concevoir, réaliser et valoriser un système qui surveille un "
     "réseau en continu, détecte automatiquement les pannes et alerte "
     "instantanément les administrateurs — 100 % open-source.", 0, False, GRIS),
    ("", 0, False, GRIS),
    ("Pourquoi ce thème ?", 0, True, BLEU_FONCE),
    ("Le réseau est devenu le « système nerveux » de toute organisation", 1, False, GRIS),
    ("Une minute d'indisponibilité peut coûter très cher", 1, False, GRIS),
    ("Vécu de terrain : pannes découvertes trop tard, par les utilisateurs", 1, False, GRIS),
    ("Conviction : l'open-source rend la supervision accessible à tous", 1, False, GRIS),
], y=Inches(1.5), h=Inches(4.0), taille=20)
encadre(s, "Allier une expertise réseau à une démarche entrepreneuriale.", y=Inches(6.0))
notes(s, "J'ai choisi ce thème car il croise une réalité observée en stage - les "
         "pannes détectées trop tard - et une conviction : on peut résoudre ce "
         "problème sans budget colossal grâce à l'open-source. C'est à la fois un "
         "défi d'ingénieur et une opportunité de marché.")

# ====================================================================== #
#  PRÉSENTATION DE LA STRUCTURE D'ACCUEIL — OPEN MOISE                   #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, None, "Structure d'accueil — OPEN MOISE")
puces(s, [
    ("OPEN MOISE — Entreprise de Services du Numérique (ESN)", 0, True, BLEU_FONCE),
    ("", 0, False, GRIS),
    ("Activités : infogérance, intégration réseau & systèmes, développement, "
     "cybersécurité", 1, False, GRIS),
    ("Mission : garantir un SI performant, disponible et sécurisé à ses clients", 1, False, GRIS),
    ("[Effectif] collaborateurs · implantée à [ville] · depuis [année]", 1, False, GRIS),
    ("Projet mené au sein du [Pôle Infrastructures & Supervision]", 1, False, GRIS),
], y=Inches(1.5), h=Inches(3.6), taille=20)
encadre(s, "ESN qui supervise les réseaux de ses clients, OPEN MOISE est "
           "directement concernée : ce projet est un outil interne stratégique pour "
           "tenir ses engagements de service (SLA) et maîtriser ses coûts.",
        y=Inches(5.5), h=Inches(1.3))
notes(s, "Quelques mots sur mon entreprise d'accueil, OPEN MOISE : une ESN qui "
         "assure notamment l'infogérance et la supervision des réseaux de ses "
         "clients. Mon projet répond donc à un besoin direct de l'entreprise : "
         "détecter plus vite les pannes des parcs qu'elle exploite et respecter ses "
         "engagements de service.")

# ====================================================================== #
#  1 — CONTEXTE ET PROBLÈME                                             #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 1, "Contexte et identification du problème")
puces(s, [
    ("Contexte : densification des réseaux (cloud, virtualisation, IoT) face à "
     "des exigences de disponibilité de plus en plus fortes (« 99,9 % »).", 0, False, GRIS),
    ("", 0, False, GRIS),
    ("Constat de terrain (PME / administrations) :", 0, True, BLEU_FONCE),
    ("Supervision manuelle et épisodique (ping à la main)", 1, False, GRIS),
    ("Pannes signalées par les utilisateurs → réaction tardive", 1, False, GRIS),
    ("Aucune traçabilité des incidents, pas d'historique exploitable", 1, False, GRIS),
    ("Solutions professionnelles jugées trop chères ou trop complexes", 1, False, GRIS),
], y=Inches(1.5), h=Inches(4.8), taille=20)
notes(s, "Le contexte : des réseaux toujours plus complexes et critiques. Pourtant, "
         "sur le terrain, beaucoup surveillent encore à la main. Résultat : on "
         "apprend la panne par les plaintes, sans aucune trace, et les outils du "
         "marché paraissent inaccessibles.")

# ---- PROBLÉMATIQUE (diapo dédiée) ----
s = ajouter_diapo(); fond(s, BLEU_FONCE)
tb = zone_texte(s, Inches(0.5), Inches(0.5), Inches(12.3), Inches(0.8))
p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "LA PROBLÉMATIQUE"
style_run(r, 24, True, BLEU)
boite = rectangle(s, Inches(1.0), Inches(1.7), Inches(11.3), Inches(2.6), BLANC)
tf = boite.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.4); tf.margin_right = Inches(0.4)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = ("« Comment détecter en temps réel les pannes d'un réseau et "
                           "réduire le temps d'intervention des administrateurs, à l'aide "
                           "d'une solution automatisée, fiable et économiquement accessible ? »")
style_run(r, 22, True, BLEU_FONCE, italique=True)
tb = zone_texte(s, Inches(1.0), Inches(4.6), Inches(11.3), Inches(2.5))
tf = tb.text_frame
items = [
    ("Sous-questions :", True, BLEU),
    ("Comment automatiser une surveillance continue et fiable (sans fausses alertes) ?", False, BLANC),
    ("Comment notifier l'administrateur où qu'il soit, instantanément ?", False, BLANC),
    ("Comment offrir cette valeur à un coût quasi nul ?", False, BLANC),
]
for i, (txt, g, c) in enumerate(items):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(8)
    r = p.add_run(); r.text = ("" if i == 0 else "•  ") + txt
    style_run(r, 18, g, c)
notes(s, "Tout le projet répond à cette question centrale, que je formule "
         "clairement : détecter en temps réel et réduire le temps d'intervention, "
         "avec une solution automatisée, fiable ET accessible financièrement. Les "
         "trois sous-questions guident ma conception.")

# ====================================================================== #
#  2 — OBJECTIFS ET RÉSULTATS                                           #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 2, "Objectifs et résultats attendus")
tableau(s, [
    ["Objectif", "Résultat attendu (indicateur)"],
    ["Détecter les pannes en temps réel", "MTTD < 2 min  (vs ~60 min)"],
    ["Alerter instantanément", "MTTR < 5 min  (vs ~45 min)"],
    ["Automatiser la surveillance", "0 intervention humaine sur la collecte"],
    ["Assurer la traçabilité", "100 % des événements journalisés"],
    ["Améliorer la disponibilité", "+2 pts  (~97,5 % → ~99,5 %)"],
    ["Maîtriser le coût", "0 € de licence (open-source)"],
], y=Inches(1.5), h=Inches(3.8), taille=17, surligne_derniere_col=True)
encadre(s, "Objectif général : livrer un produit fonctionnel, mesurablement plus "
           "performant que la supervision manuelle, pour un coût négligeable.", y=Inches(5.7), h=Inches(1.1))
notes(s, "Mes objectifs sont chiffrés, donc vérifiables. Le cœur : faire chuter le "
         "temps de détection de l'ordre de l'heure à moins de deux minutes, et le "
         "temps de réaction à moins de cinq minutes, sans coût de licence.")

# ====================================================================== #
#  3 — DÉMARCHE MÉTHODOLOGIQUE                                          #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 3, "Démarche méthodologique")
puces(s, [
    ("Type : recherche appliquée / expérimentale — paradigme Design Science "
     "(on conçoit un artefact et on MESURE son efficacité).", 0, False, GRIS),
    ("", 0, False, GRIS),
    ("Cycle de travail itératif (inspiré DevOps) :", 0, True, BLEU_FONCE),
], y=Inches(1.5), h=Inches(1.8), taille=20)
boite = rectangle(s, Inches(0.9), Inches(3.5), Inches(11.5), Inches(0.9), GRIS_CLAIR)
tf = boite.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Analyse → Conception (UML/MERISE) → Développement → Test → Intégration → Mesure"
style_run(r, 17, True, BLEU_FONCE)
puces(s, [
    ("Outils & livrables : recherche documentaire · observation terrain · "
     "prototypage · collecte automatisée des métriques (journaux) · "
     "comparaison avant/après (manuel vs automatisé).", 0, False, GRIS),
], y=Inches(4.7), h=Inches(1.6), taille=19)
notes(s, "Ma démarche est celle de l'ingénieur-chercheur : je conçois un système "
         "réel et je prouve sa valeur par la mesure. J'ai travaillé en cycles "
         "itératifs, à la DevOps, et j'évalue par comparaison avant/après sur des "
         "indicateurs objectifs.")

# ====================================================================== #
#  4 — ÉTAT DES LIEUX                                                   #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 4, "État des lieux des solutions existantes")
tableau(s, [
    ["Solution", "Type", "Atout", "Frein majeur"],
    ["Nagios", "Open-source", "Éprouvé, extensible", "Config. complexe"],
    ["Zabbix", "Open-source", "Très complet", "Gourmand en ressources"],
    ["Centreon", "Mixte", "Interface soignée", "Modules avancés payants"],
    ["PRTG", "Propriétaire", "Simple", "Payant, Windows"],
    ["SolarWinds", "Propriétaire", "Haut de gamme", "Très coûteux"],
], y=Inches(1.5), h=Inches(3.4), taille=15)
encadre(s, "Le vide identifié : rien de léger + gratuit + simple + sur mesure, avec "
           "notification mobile native, pour les petites structures.", y=Inches(5.4), h=Inches(1.1))
notes(s, "J'ai analysé les références du marché : soit des usines à gaz puissantes "
         "mais complexes, soit des produits simples mais propriétaires et chers. Il "
         "existe un vide pour une solution légère, gratuite et sur mesure.")

# ---- Solution proposée ----
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 4, "Solution proposée")
puces(s, [
    ("Un système automatisé, modulaire et 100 % open-source qui :", 0, True, BLEU_FONCE),
    ("découvre automatiquement les équipements du réseau", 1, False, GRIS),
    ("sonde en continu la disponibilité (ICMP) et les services (TCP)", 1, False, GRIS),
    ("confirme la panne (anti-faux positif) et journalise tout", 1, False, GRIS),
    ("alerte en temps réel par e-mail ET Telegram (push mobile)", 1, False, GRIS),
    ("offre un tableau de bord web temps réel + rapports", 1, False, GRIS),
], y=Inches(1.5), h=Inches(3.6), taille=20)
encadre(s, "Stack : Ubuntu · Python · Cron · MySQL · Flask · Bootstrap · Bot Telegram",
        y=Inches(5.6), h=Inches(1.0), fond_c=BLEU_FONCE, barre=BLEU)
# corrige couleur texte de l'encadré (fond foncé)
notes(s, "Ma réponse à ce vide : une solution complète mais légère. Elle découvre, "
         "surveille, confirme, journalise, alerte et affiche - le tout assemblé à "
         "partir de briques open-source éprouvées.")

# ====================================================================== #
#  5 — DIFFÉRENCIATION                                                  #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 5, "Axe de différenciation (innovation)")
tableau(s, [
    ["Différenciateur", "Bénéfice client"],
    ["Alerte Telegram native", "Notification push gratuite, admin alerté partout"],
    ["Ultra-légère", "Tourne sur un mini-serveur / VM 1 vCPU"],
    ["Code 100 % ouvert & maîtrisé", "Personnalisation totale, zéro vendor lock-in"],
    ["« Plug & supervise »", "Découverte auto. + déploiement en < 30 min"],
    ["Prête pour l'IA", "Historique structuré → maintenance prédictive"],
], y=Inches(1.5), h=Inches(3.4), taille=16)
encadre(s, "L'innovation n'est pas une brique isolée, mais l'ASSEMBLAGE : simplicité "
           "+ gratuité + notification mobile + extensibilité IA.", y=Inches(5.4), h=Inches(1.1))
notes(s, "Mon innovation ne réside pas dans un protocole nouveau, mais dans un "
         "positionnement unique : combiner simplicité, gratuité, alerte mobile "
         "instantanée et ouverture vers l'IA. Là où chaque concurrent impose un "
         "sacrifice, ma solution réunit ces atouts. Telegram natif est mon marqueur.")

# ====================================================================== #
#  6 — FAISABILITÉ & CONCEPTION                                        #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 6, "Étude de faisabilité & conception")
puces(s, [
    ("Faisabilité technique ✓ — briques matures, compétences maîtrisées, "
     "prototype réalisé et testé.", 0, False, VERT),
    ("Faisabilité économique ✓ — coût de licence nul, matériel minimal.", 0, False, VERT),
    ("Faisabilité organisationnelle ✓ — déploiement et prise en main rapides.", 0, False, VERT),
    ("", 0, False, GRIS),
    ("Conception formalisée :", 0, True, BLEU_FONCE),
    ("UML : 7 diagrammes (contexte, cas d'usage, séquence, activité, classes, "
     "composants, déploiement)", 1, False, GRIS),
    ("MERISE : MCD → MLD → base MySQL (5 tables)", 1, False, GRIS),
    ("Architecture en 5 couches", 1, False, GRIS),
], y=Inches(1.5), h=Inches(5.2), taille=19)
notes(s, "Le projet est faisable sur les trois plans : technique - le prototype "
         "fonctionne -, économique - coût quasi nul - et organisationnel. J'ai "
         "rigoureusement conçu le système en UML et MERISE, sur une architecture en "
         "cinq couches.")

# ---- Architecture en 5 couches (IMAGE générée) ----
diapo_image(6, "Architecture en 5 couches",
            "architecture/architecture-5couches.png",
            legende="Découplage Moteur (Cron) ↔ Interface (Flask) : la surveillance "
                    "continue même si le tableau de bord est arrêté.",
            note_txt="Voici l'architecture en cinq couches. Le choix d'ingénierie le "
                     "plus important est le découplage entre la collecte et "
                     "l'affichage : ils communiquent uniquement par la base de "
                     "données, ce qui rend le système robuste.")

# ---- UML : 7 diagrammes (grille d'aperçu) ----
diapo_grille_images(6, "Conception UML — les 7 diagrammes", [
    ("architecture/diagrammes/diagramme-contexte.png", "1. Contexte"),
    ("architecture/diagrammes/cas-utilisation.png", "2. Cas d'utilisation"),
    ("architecture/diagrammes/diagramme-sequence.png", "3. Séquence"),
    ("architecture/diagrammes/diagramme-activite.png", "4. Activité"),
    ("architecture/diagrammes/diagramme-classes.png", "5. Classes"),
    ("architecture/diagrammes/diagramme-composants.png", "6. Composants"),
    ("architecture/diagrammes/diagramme-deploiement.png", "7. Déploiement"),
], note_txt="J'ai formalisé toute la conception avec sept diagrammes UML, du "
            "diagramme de contexte au diagramme de déploiement. Les versions "
            "pleine page figurent en annexe pour le détail.")

# ---- MERISE : MCD -> MLD ----
diapo_deux_images(6, "MERISE : du MCD au MLD (base MySQL, 5 tables)",
                  "database/mcd.png", "MCD — Modèle Conceptuel",
                  "database/mld.png", "MLD — Modèle Logique",
                  note_txt="Pour la base de données, j'ai suivi la méthode MERISE : "
                           "du modèle conceptuel - les entités et leurs associations - "
                           "vers le modèle logique - les cinq tables relationnelles "
                           "avec leurs clés - implémenté ensuite en MySQL.")

# ====================================================================== #
#  7 — FONCTIONNEMENT TECHNIQUE                                         #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 7, "Fonctionnement technique — le cycle automatisé")
etapes = [
    "1.  CRON déclenche le moteur toutes les 2 minutes",
    "2.  Charge les équipements (MySQL) puis sonde ICMP (ping) + TCP (service)",
    "3.  Met à jour le statut + journalise chaque vérification",
    "4.  Seuil d'échecs atteint ? (anti-faux positif)",
    "5.  ALERTE e-mail + Telegram  (avec anti-spam / dé-duplication)",
    "6.  Retour en ligne (UP) → notification de rétablissement automatique",
]
puces(s, [(e, 0, False, GRIS) for e in etapes], y=Inches(1.6), h=Inches(3.6), taille=19, interligne=12)
encadre(s, "Robustesse : seuil d'échecs (pas de fausse alerte), dé-duplication (pas "
           "de spam), sondes parallélisées (scan d'un /24 en ~12 s), journaux à rotation.",
        y=Inches(5.7), h=Inches(1.1))
notes(s, "Techniquement : toutes les deux minutes, Cron lance le moteur qui teste "
         "chaque équipement. Une panne n'est confirmée qu'après plusieurs échecs - "
         "pour éviter les fausses alertes - et une seule notification est envoyée "
         "par panne. Tout est parallélisé pour rester rapide.")

# ---- Sécurité by design ----
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 7, "Sécurité « by design »")
tableau(s, [
    ["Risque", "Parade implémentée"],
    ["Secrets dans le code", "Variables d'environnement (.env non versionné)"],
    ["Vol de mots de passe", "Hachage pbkdf2:sha256 (jamais en clair)"],
    ["Injection SQL", "Requêtes paramétrées systématiques"],
    ["Écoute des notifications", "SMTP STARTTLS + Telegram HTTPS"],
    ["Accès BDD trop large", "Compte applicatif au moindre privilège"],
    ["Accès non autorisé", "Authentification du tableau de bord"],
], y=Inches(1.5), h=Inches(4.0), taille=16)
notes(s, "La sécurité a été pensée dès la conception, pas ajoutée après : secrets "
         "hors du code, mots de passe hachés, requêtes paramétrées contre "
         "l'injection SQL, communications chiffrées et moindre privilège sur la base.")

# ====================================================================== #
#  8 — DÉMONSTRATION                                                    #
# ====================================================================== #
s = ajouter_diapo(); fond(s, BLEU_FONCE)
rectangle(s, 0, Inches(0.6), LARGEUR, Inches(1.0), BLEU)
tb = zone_texte(s, Inches(0.5), Inches(0.65), Inches(12.3), Inches(0.9))
tf = tb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "8.  DÉMONSTRATION — scénario en direct"
style_run(r, 30, True, BLANC)
etapes = [
    "Tableau de bord — vue temps réel : équipements UP, KPI, graphiques",
    "Je débranche / éteins un équipement supervisé",
    "Au cycle suivant → le statut bascule en DOWN (badge rouge)",
    "L'alerte arrive : e-mail + notification Telegram sur le téléphone",
    "Je rallume → notification de rétablissement + acquittement auto",
    "Page Rapports : historique, taux de disponibilité, latences",
]
tb = zone_texte(s, Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.2))
tf = tb.text_frame
for i, e in enumerate(etapes):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(12)
    r = p.add_run(); r.text = f"{i+1}.  {e}"
    style_run(r, 20, False, BLANC)
encadre(s, "Plan B : captures d'écran + courte vidéo si la démo live est impossible.",
        y=Inches(6.4), h=Inches(0.8), fond_c=BLEU, barre=BLANC)
notes(s, "Pour la démonstration, je propose un scénario vivant : je montre le "
         "tableau de bord, j'éteins un équipement devant vous, et vous verrez "
         "l'alerte Telegram arriver sur mon téléphone en temps réel. Puis je le "
         "rallume pour montrer le rétablissement. J'ai un plan B en captures et vidéo.")

# ---- Démonstration : captures ----
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 8, "Démonstration — captures clés")
tableau(s, [
    ["Écran", "Ce qu'il prouve"],
    ["Connexion", "Accès sécurisé"],
    ["Tableau de bord", "Supervision temps réel, KPI, anneau de disponibilité"],
    ["Équipements", "Inventaire + découverte automatique"],
    ["Alertes", "Historique + acquittement"],
    ["Notification Telegram", "Alerte push reçue sur smartphone"],
    ["Rapports", "Statistiques & graphiques exportables"],
], y=Inches(1.5), h=Inches(3.8), taille=16)
encadre(s, "À insérer : les captures d'écran réelles de l'application déployée.",
        y=Inches(5.7), h=Inches(0.9))
notes(s, "Ces captures matérialisent chaque fonctionnalité clé. La plus parlante "
         "est la notification Telegram reçue sur le téléphone : la preuve concrète "
         "de la valeur ajoutée pour l'administrateur.")

# ====================================================================== #
#  9 — MARKETING, VENTE & CONCURRENCE                                   #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 9, "Marketing, vente et concurrence")
puces(s, [
    ("Cible : PME, écoles, administrations, cybercafés, hébergeurs, MSP (infogérants).", 0, False, GRIS),
    ("", 0, False, GRIS),
    ("Proposition de valeur :", 0, True, BLEU_FONCE),
    ("« Supervisez votre réseau et soyez alerté sur votre téléphone en cas de "
     "panne — sans licence, sans complexité. »", 1, False, BLEU),
    ("", 0, False, GRIS),
    ("Modèle économique (open-core) :", 0, True, BLEU_FONCE),
    ("Cœur open-source gratuit (adoption & confiance)", 1, False, GRIS),
    ("Services : installation, formation, support (abonnement)", 1, False, GRIS),
    ("Édition Pro : SNMP, multi-sites, IA prédictive, rapports avancés", 1, False, GRIS),
], y=Inches(1.5), h=Inches(5.0), taille=18)
notes(s, "Côté business, je vise les structures sans gros budget IT et les "
         "infogérants. Mon modèle est l'open-core : le cœur est gratuit pour créer "
         "l'adoption, et je monétise les services et une édition Pro avec SNMP et IA.")

# ---- Positionnement concurrentiel ----
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 9, "Positionnement concurrentiel")
tableau(s, [
    ["Critère", "Nagios/Zabbix", "PRTG/SolarWinds", "Notre solution"],
    ["Prix", "Gratuit mais coûteux", "€€€", "Gratuit + services"],
    ["Simplicité", "Faible", "Élevée", "Élevée"],
    ["Légèreté", "Moyenne/Faible", "Faible", "Très élevée"],
    ["Alerte mobile native", "Plugin", "Appli", "Telegram natif"],
    ["Sur-mesure / ouvert", "Limité", "Non", "Total"],
], y=Inches(1.5), h=Inches(3.4), taille=15, surligne_derniere_col=True)
encadre(s, "Stratégie : ne pas affronter les géants sur le haut de gamme, mais "
           "dominer le segment délaissé des petites structures (« océan bleu »).",
        y=Inches(5.4), h=Inches(1.1))
notes(s, "Je ne prétends pas battre Zabbix sur les très grandes infrastructures. Ma "
         "stratégie est celle de l'océan bleu : occuper le segment que les géants "
         "négligent - les petites structures - avec un produit simple et gratuit.")

# ====================================================================== #
#  10 — PRÉVISIONS FINANCIÈRES                                          #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 10, "Prévisions financières")
tb = zone_texte(s, Inches(0.7), Inches(1.35), Inches(5.9), Inches(0.5))
p = tb.text_frame.paragraphs[0]
r = p.add_run(); r.text = "Coûts de mise en place"
style_run(r, 17, True, BLEU_FONCE)
tableau(s, [
    ["Poste", "Coût"],
    ["Licences logicielles", "0 € (open-source)"],
    ["Serveur (VM / mini-PC)", "~150–300 €"],
    ["Déploiement (temps)", "~1 j de prestation"],
    ["Total entrée", "≈ 200 €"],
], x=Inches(0.7), y=Inches(1.9), w=Inches(5.9), h=Inches(2.6), taille=15)
tb = zone_texte(s, Inches(6.9), Inches(1.35), Inches(5.9), Inches(0.5))
p = tb.text_frame.paragraphs[0]
r = p.add_run(); r.text = "Revenus (scénario prestataire, an 1)"
style_run(r, 17, True, BLEU_FONCE)
tableau(s, [
    ["Source", "Hypothèse", "Revenu"],
    ["Installation+formation", "10 × 300 €", "3 000 €"],
    ["Support (abonnement)", "10 × 40 €/mois", "4 800 €"],
    ["Édition Pro", "3 × 500 €", "1 500 €"],
    ["Total an 1", "", "≈ 9 300 €"],
], x=Inches(6.9), y=Inches(1.9), w=Inches(5.9), h=Inches(2.6), taille=14, surligne_derniere_col=True)
encadre(s, "ROI client : 1 h de panne évitée ≫ coût de la solution (≈ 200 €). "
           "Elle s'autofinance dès le premier incident majeur évité.", y=Inches(5.7), h=Inches(1.1))
notes(s, "Financièrement, l'entrée est quasi nulle : pas de licence, juste un petit "
         "serveur. Côté revenus, même avec des hypothèses prudentes, on dépasse "
         "9 000 € la première année. Pour le client, le retour vient de la réduction "
         "des coûts d'indisponibilité : la solution est rentabilisée dès le premier "
         "incident majeur évité.")

# ====================================================================== #
#  11 — LIMITES & PERSPECTIVES                                          #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, 11, "Limites du projet et perspectives")
puces(s, [
    ("Limites assumées :", 0, True, ROUGE),
    ("Supervision active → pas de métriques internes (CPU/RAM) sans SNMP", 1, False, GRIS),
    ("Réactivité bornée par l'intervalle de cycle (2 min)", 1, False, GRIS),
    ("Alertes dépendantes de la connectivité sortante", 1, False, GRIS),
    ("« Qui surveille le surveillant ? » → besoin de redondance", 1, False, GRIS),
    ("", 0, False, GRIS),
    ("Perspectives :", 0, True, VERT),
    ("Intégration SNMP (performances détaillées)", 1, False, GRIS),
    ("Machine Learning : détection d'anomalies", 1, False, GRIS),
    ("Maintenance prédictive (anticiper la panne) · Auto-remédiation (AIOps)", 1, False, GRIS),
    ("Conteneurisation (Docker/K8s) · Canaux SMS, Slack, Teams", 1, False, GRIS),
], y=Inches(1.4), h=Inches(5.4), taille=18, interligne=6)
notes(s, "Je reste lucide sur les limites : pas encore de SNMP, réactivité bornée à "
         "deux minutes, et la question du superviseur lui-même. Mais ces limites "
         "tracent ma feuille de route : SNMP, puis l'IA pour passer d'une "
         "supervision réactive à une supervision prédictive.")

# ====================================================================== #
#  CONCLUSION                                                           #
# ====================================================================== #
s = ajouter_diapo(); fond(s)
bandeau_titre(s, None, "Conclusion")
puces(s, [
    ("Un produit fonctionnel, testé, 100 % open-source", 0, True, VERT),
    ("Détection temps réel (< 2 min) & temps d'intervention réduit", 0, True, VERT),
    ("Un modèle économique viable (open-core) sur un segment délaissé", 0, True, VERT),
    ("Une base extensible vers l'IA et la maintenance prédictive", 0, True, VERT),
], y=Inches(1.6), h=Inches(2.8), taille=22, interligne=14)
encadre(s, "De la supervision réactive vers une supervision proactive, accessible "
           "et intelligente. L'automatisation transforme la disponibilité réseau en "
           "avantage à la portée de toutes les organisations.",
        y=Inches(5.0), h=Inches(1.6), fond_c=BLEU_FONCE, barre=BLEU)
notes(s, "En conclusion, ce projet livre un produit réel et performant, doublé d'un "
         "modèle économique crédible, et ouvert vers l'avenir de la supervision : le "
         "prédictif. J'ai montré qu'on pouvait rendre la haute disponibilité "
         "accessible à tous.")

# ---- Remerciements ----
s = ajouter_diapo(); fond(s, BLEU_FONCE)
tb = zone_texte(s, Inches(1.0), Inches(2.8), Inches(11.3), Inches(2.0))
tf = tb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Merci de votre attention"
style_run(r, 40, True, BLANC)
p = tf.add_paragraph(); p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Je me tiens à votre disposition pour vos questions"
style_run(r, 20, False, RGBColor(0xDD,0xE6,0xF2), italique=True)
p = tf.add_paragraph(); p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "\n[NOM Prénom] — Master 2 RIT — 2026"
style_run(r, 16, True, BLANC)
notes(s, "Je vous remercie de votre attention et je suis prêt à répondre à toutes "
         "vos questions, qu'elles soient techniques ou sur le volet économique.")

# ====================================================================== #
#  ANNEXES — diagrammes détaillés (diapos de secours pour le Q&A)        #
# ====================================================================== #
# Intercalaire
s = ajouter_diapo(); fond(s, BLEU_FONCE)
tb = zone_texte(s, Inches(1.0), Inches(3.0), Inches(11.3), Inches(1.5))
tf = tb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "ANNEXES — Diagrammes de conception détaillés"
style_run(r, 30, True, BLANC)
p = tf.add_paragraph(); p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Diapositives de secours pour les questions du jury"
style_run(r, 16, False, RGBColor(0xDD, 0xE6, 0xF2), italique=True)
notes(s, "Voici en annexe les diagrammes détaillés, que je peux afficher pour "
         "répondre précisément à vos questions sur la conception.")

# UML pleine page (1 par diapo)
_uml = [
    ("architecture/diagrammes/diagramme-contexte.png", "Annexe — Diagramme de contexte"),
    ("architecture/diagrammes/cas-utilisation.png", "Annexe — Diagramme de cas d'utilisation"),
    ("architecture/diagrammes/diagramme-sequence.png", "Annexe — Diagramme de séquence"),
    ("architecture/diagrammes/diagramme-activite.png", "Annexe — Diagramme d'activité"),
    ("architecture/diagrammes/diagramme-classes.png", "Annexe — Diagramme de classes"),
    ("architecture/diagrammes/diagramme-composants.png", "Annexe — Diagramme de composants"),
    ("architecture/diagrammes/diagramme-deploiement.png", "Annexe — Diagramme de déploiement"),
]
for chemin, titre in _uml:
    diapo_image(None, titre, chemin)

# MLD pleine page (schéma relationnel détaillé)
diapo_image(None, "Annexe — Modèle Logique de Données (MLD)", "database/mld.png",
            legende="5 tables : utilisateurs, equipements, journaux, alertes, statistiques "
                    "(clés primaires PK, clés étrangères FK).")

# ---------------------------------------------------------------------- #
sortie = os.path.join(os.path.dirname(__file__), "presentation-projet.pptx")
prs.save(sortie)
print(f"PowerPoint généré : {sortie}  ({len(prs.slides.__iter__.__self__._sldIdLst)} diapositives)")
