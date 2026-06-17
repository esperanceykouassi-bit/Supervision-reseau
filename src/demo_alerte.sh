#!/usr/bin/env bash
# ====================================================================== #
#  demo_alerte.sh — Démonstration contrôlée des alertes (pour la vidéo).  #
#  ----------------------------------------------------------------------#
#  Usage (depuis ~/supervision/src) :                                     #
#     bash demo_alerte.sh down   -> provoque une PANNE   (alerte rouge)   #
#     bash demo_alerte.sh up     -> RÉTABLIT l'équipement (notif. orange) #
#                                                                         #
#  Le script utilise un équipement dédié « PC-DEMO » qu'il crée au besoin #
#  et dont il bascule l'adresse IP entre joignable (127.0.0.1) et         #
#  injoignable (192.0.2.99), puis lance les cycles de supervision pour    #
#  déclencher l'envoi Telegram + e-mail tout de suite.                    #
# ====================================================================== #
cd "$(dirname "$0")"
DB() { mysql -u supervisor -psupervision_pass supervision -N -e "$1"; }
PY="venv/bin/python"

# Crée l'équipement de démo s'il n'existe pas déjà.
DB "INSERT IGNORE INTO equipements (nom,adresse_ip,type_equipement,statut) VALUES ('PC-DEMO','127.0.0.1','Serveur','UP');"

case "$1" in
  down)
    echo ">> Mise en panne de PC-DEMO (adresse injoignable)..."
    DB "UPDATE equipements SET adresse_ip='192.0.2.99' WHERE nom='PC-DEMO';"
    # On efface une éventuelle alerte précédente -> l'alerte pourra se redéclencher.
    DB "UPDATE alertes SET acquittee=1 WHERE equipement_id=(SELECT id FROM equipements WHERE nom='PC-DEMO');"
    echo ">> Cycle 1/2..."; $PY supervisor.py >/dev/null 2>&1
    echo ">> Cycle 2/2 (seuil atteint -> ALERTE)..."; $PY supervisor.py
    echo ">> Une alerte 🔴 PANNE_RESEAU a dû partir sur Telegram + e-mail."
    ;;
  up)
    echo ">> Rétablissement de PC-DEMO (adresse joignable)..."
    DB "UPDATE equipements SET adresse_ip='127.0.0.1' WHERE nom='PC-DEMO';"
    echo ">> Cycle de supervision..."; $PY supervisor.py
    echo ">> Une notification 🟠 de RÉTABLISSEMENT a dû partir sur Telegram."
    ;;
  *)
    echo "Usage : bash demo_alerte.sh down   (provoque une panne)"
    echo "        bash demo_alerte.sh up     (rétablit l'équipement)"
    ;;
esac
