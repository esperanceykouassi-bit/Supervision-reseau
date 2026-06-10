#!/usr/bin/env bash
# ====================================================================== #
#  Assemble les parties du mémoire-projet et génère le document Word.    #
#  Prérequis : pandoc (+ libreoffice pour le PDF, optionnel).            #
#  Usage : cd memoire && bash build.sh                                   #
# ====================================================================== #
set -e
cd "$(dirname "$0")"

PARTS=(
  _build/00-liminaires.md
  _build/01-intro-contexte.md
  _build/02-objectifs-demarche.md
  _build/03-etat-solution.md
  _build/04-differenciation-conception.md
  _build/05-fonctionnement-technique.md
  _build/06-demonstration.md
  _build/07-marketing-finance.md
  _build/08-limites-conclusion.md
)

echo "→ Assemblage des parties..."
cat "${PARTS[@]}" > memoire-projet-OPEN-MOISE.md

echo "→ Génération du document Word (.docx)..."
pandoc memoire-projet-OPEN-MOISE.md \
  -o memoire-projet-OPEN-MOISE.docx \
  --toc --toc-depth=2 \
  --resource-path=.:..

# PDF optionnel (nécessite LibreOffice)
if command -v soffice >/dev/null 2>&1; then
  echo "→ Génération du PDF (LibreOffice)..."
  soffice --headless --convert-to pdf --outdir . memoire-projet-OPEN-MOISE.docx >/dev/null 2>&1 || true
fi

echo "✓ Terminé : memoire-projet-OPEN-MOISE.docx"
