# -*- coding: utf-8 -*-
"""
mise_en_forme_cerco.py
======================
Applique la mise en forme « CERCO » au mémoire :
  - page de garde (3 logos, année, mémoire, thème, titre, encadreurs) ;
  - sommaire automatique (champ TOC Word, pointillés) ;
  - en-tête (titre courant) et pied de page (nom — CERCO — année | Page N)
    en sarcelle, avec filets ;
  - titres de sections en sarcelle.

Prérequis : pandoc, python-docx, Pillow.
Usage : cd memoire && python mise_en_forme_cerco.py
"""
import os, re, subprocess
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ICI = os.path.dirname(os.path.abspath(__file__))
SRC_MD = os.path.join(ICI, "memoire-KOUASSI-ESPERANCE.md")
BODY_MD = os.path.join(ICI, "_body_cerco.md")
BODY_DOCX = os.path.join(ICI, "_body_cerco.docx")
OUT = os.path.join(ICI, "Memoire-KOUASSI-ESPERANCE-CERCO.docx")
LOGOS = os.path.join(ICI, "assets", "cerco")

TEAL = RGBColor(0x1F, 0x7A, 0x8C)
BLUE = RGBColor(0x3E, 0x7C, 0xB5)
ACCENT = RGBColor(0x2E, 0xC4, 0xB6)
BLACK = RGBColor(0x11, 0x11, 0x11)
GREY = RGBColor(0x55, 0x66, 0x77)

NOM = "KOUASSI Yoo Nyong Kra Espérance"
TITRE = "Automatisation de la Supervision et de la Détection des Pannes Réseau"
ANNEE = "2025 – 2026"

# ---------------------------------------------------------------------- #
# 1) Préparer le corps : retirer la page de garde du Markdown            #
# ---------------------------------------------------------------------- #
md = open(SRC_MD, encoding="utf-8").read()
i = md.find("# DÉDICACE")
body = md[i:] if i != -1 else md
# on retire la note sur la TdM (le vrai sommaire est en tête)
body = body.replace("> *La table des matières détaillée est générée automatiquement ci-après.*\n", "")
open(BODY_MD, "w", encoding="utf-8").write(body)

# ---------------------------------------------------------------------- #
# 2) Pandoc -> docx (sans TOC ; on insère un vrai champ Word ensuite)    #
# ---------------------------------------------------------------------- #
subprocess.run(["pandoc", BODY_MD, "-o", BODY_DOCX,
                "--resource-path", ".:..", ], cwd=ICI, check=True)

doc = Document(BODY_DOCX)

# ---------------------------------------------------------------------- #
# Helpers                                                                #
# ---------------------------------------------------------------------- #
def set_run(r, size=11, bold=False, italic=False, color=BLACK, font="Calibri"):
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font

def para(text="", size=11, bold=False, italic=False, color=BLACK,
         align=WD_ALIGN_PARAGRAPH.CENTER, font="Calibri", space_after=6, space_before=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if text:
        set_run(p.add_run(text), size, bold, italic, color, font)
    return p

def bottom_border(p, color="1F7A8C", size="12", space="4"):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), space); bottom.set(qn("w:color"), color)
    pbdr.append(bottom); pPr.append(pbdr)

def page_break_para():
    p = doc.add_paragraph()
    run = p.add_run()
    br = OxmlElement("w:br"); br.set(qn("w:type"), "page")
    run._r.append(br)
    return p

def add_field(paragraph, instr, placeholder=""):
    r = paragraph.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = placeholder
    f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
    for e in (f1, it, f2, t, f3):
        r._r.append(e)
    return r

# ---------------------------------------------------------------------- #
# 3) Construire les éléments de garde + sommaire (puis les remonter)     #
# ---------------------------------------------------------------------- #
debut = len(doc.paragraphs)  # tout ce qu'on ajoute après sera remonté

# --- Logos (table 1x3 sans bordure) ---
tlogo = doc.add_table(rows=1, cols=3)
tlogo.alignment = WD_TABLE_ALIGNMENT.CENTER
logos = [("logo-ministere.png", 1.5), ("armoiries.png", 0.9), ("logo-cerco.png", 1.1)]
for cell, (fichier, larg) in zip(tlogo.rows[0].cells, logos):
    cp = cell.paragraphs[0]; cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.add_run().add_picture(os.path.join(LOGOS, fichier), width=Inches(larg))

para("", space_after=4)
para("ANNÉE ACADÉMIQUE : " + ANNEE, 13, True, color=BLACK, space_after=14)
para("MÉMOIRE DE FIN DE CYCLE MASTER", 22, True, color=BLUE, font="Cambria", space_after=6)
para("RÉSEAUX INFORMATIQUES ET TÉLÉCOMMUNICATIONS : OPTION [À PRÉCISER]",
     14, True, color=BLACK, font="Cambria", space_after=18)
para("THÈME", 14, True, color=BLUE, font="Cambria", space_after=2)
pr = para("", space_after=8); bottom_border(pr, "1F7A8C", "12")
para(TITRE, 22, True, color=BLACK, font="Cambria", space_after=4)
pa = para("", space_after=18); bottom_border(pa, "2EC4B6", "18")
para("Présenté par", 12, True, color=BLACK, space_after=2)
para(NOM, 13, False, color=BLACK, space_after=26)

# --- Encadreurs (table 1x2 sans bordure) ---
tdir = doc.add_table(rows=1, cols=2)
tdir.alignment = WD_TABLE_ALIGNMENT.CENTER
g, d = tdir.rows[0].cells
def cell_lines(cell, lines):
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    first = True
    for txt, bold, italic in lines:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        set_run(p.add_run(txt), 11, bold, italic, BLACK)
cell_lines(g, [("DIRECTEUR DE MÉMOIRE", True, False),
               ("Dr Alain CAPO-CHICHI", False, False),
               ("(Maître de Conférences des Universités", False, True),
               ("du CAMES en Génie Informatique)", False, True)])
cell_lines(d, [("ASSISTANT DIRECTEUR DE MÉMOIRE", True, False),
               ("M. Maxime LOKOSSOU", False, False),
               ("Directeur Chargé des Affaires Académiques", False, False),
               ("CERCO-CI", False, False)])

page_break_para()

# --- Sommaire ---
psom = doc.add_paragraph(); psom.paragraph_format.space_after = Pt(10)
set_run(psom.add_run("SOMMAIRE"), 18, True, color=TEAL, font="Cambria")
ptoc = doc.add_paragraph()
add_field(ptoc, 'TOC \\o "1-3" \\h \\z \\u',
          "  ⟳  Clic droit sur ce sommaire puis « Mettre à jour les champs » pour l'afficher.")
page_break_para()

# Récupérer les éléments ajoutés (paragraphes ET tables) dans l'ordre du document
nouveaux = []
for el in list(doc.element.body):
    # on prend tout ce qui a été ajouté après 'debut' : repérage par contenu
    pass
# Méthode robuste : on identifie les éléments ajoutés = les derniers ajoutés.
# On reconstruit l'ordre voulu explicitement :
ordre = [tlogo._tbl]
# paragraphes ajoutés après les logos jusqu'au page-break du sommaire :
# on parcourt body et on collecte les éléments situés APRÈS la table logos.
body_el = doc.element.body
idx_logo = list(body_el).index(tlogo._tbl)
apres = list(body_el)[idx_logo:]  # de la table logos jusqu'à la fin (incluant sectPr)
# retirer le sectPr final s'il est present
apres = [e for e in apres if e.tag != qn("w:sectPr")]

# Déplacer 'apres' (la garde + sommaire) tout au début du document
for el in apres:
    body_el.remove(el)
for pos, el in enumerate(apres):
    body_el.insert(pos, el)

# ---------------------------------------------------------------------- #
# 4) En-tête et pied de page (section)                                   #
# ---------------------------------------------------------------------- #
section = doc.sections[0]
section.different_first_page_header_footer = True  # pas d'en-tête sur la garde

# En-tête (pages courantes)
hdr = section.header
hp = hdr.paragraphs[0]; hp.text = ""; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
set_run(hp.add_run(TITRE), 8.5, False, italic=True, color=TEAL)
bottom_border(hp, "1F7A8C", "6")

# Pied de page (pages courantes) : nom — CERCO — année | Page N
ftr = section.footer
fp = ftr.paragraphs[0]; fp.text = ""; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(fp.add_run(f"{NOM} — CERCO — Année académique {ANNEE}    |    Page "), 8.5, False, color=TEAL)
add_field(fp, "PAGE", "1");
# bordure haute du pied
pPr = fp._p.get_or_add_pPr(); pbdr = OxmlElement("w:pBdr")
top = OxmlElement("w:top"); top.set(qn("w:val"), "single"); top.set(qn("w:sz"), "6")
top.set(qn("w:space"), "4"); top.set(qn("w:color"), "1F7A8C"); pbdr.append(top); pPr.append(pbdr)

# Première page (garde) : en-tête/pied vides
section.first_page_header.paragraphs[0].text = ""
section.first_page_footer.paragraphs[0].text = ""

# ---------------------------------------------------------------------- #
# 5) Titres de sections en sarcelle (styles Heading)                     #
# ---------------------------------------------------------------------- #
tailles = {"Heading 1": 16, "Heading 2": 13, "Heading 3": 12, "Heading 4": 11}
for st in doc.styles:
    if st.name in tailles:
        st.font.color.rgb = TEAL
        st.font.name = "Cambria"
        st.font.bold = True
        st.font.size = Pt(tailles[st.name])

# ---------------------------------------------------------------------- #
# 6) Forcer Word à mettre à jour tous les champs (sommaire) à l'ouverture #
# ---------------------------------------------------------------------- #
settings = doc.settings.element
upd = OxmlElement("w:updateFields")
upd.set(qn("w:val"), "true")
settings.insert(0, upd)

doc.save(OUT)
print("Mémoire mis en forme CERCO :", OUT)
print("Pages liminaires + sommaire + en-tête/pied appliqués.")
