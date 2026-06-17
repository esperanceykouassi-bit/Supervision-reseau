#!/usr/bin/env bash
# ====================================================================== #
#  demo_alerte.sh — Démonstration contrôlée des alertes (pour la vidéo).  #
#  ----------------------------------------------------------------------#
#  Usage (depuis ~/supervision/src) :                                     #
#     bash demo_alerte.sh down   -> provoque une PANNE   (alerte rouge)   #
#     bash demo_alerte.sh up     -> RÉTABLIT l'équipement (notif. orange) #
#     bash demo_alerte.sh clean  -> retire le PC-DEMO après la démo       #
#                                                                         #
#  Principe : un équipement dédié « PC-DEMO » dont on bascule l'adresse   #
#  entre injoignable (192.0.2.99) et joignable (127.0.0.1, la boucle      #
#  locale qui répond toujours), puis on lance les cycles de supervision   #
#  pour déclencher l'envoi Telegram + e-mail immédiatement.               #
#                                                                         #
#  NB : « down » repart toujours d'une ligne PC-DEMO propre (on supprime  #
#  d'éventuels doublons et on évite tout conflit d'adresse IP unique).    #
# ====================================================================== #
cd "$(dirname "$0")"
DB() { mysql -u supervisor -psupervision_pass supervision -N -e "$1" 2>/dev/null; }
PY="venv/bin/python"

case "$1" in
  down)
    echo ">> Préparation d'un PC-DEMO propre..."
    # On efface toute trace précédente (la ligne et ses IP de démo) pour
    # éviter les doublons et les conflits sur la contrainte d'IP unique.
    DB "DELETE FROM equipements WHERE nom='PC-DEMO' OR adresse_ip IN ('192.0.2.99','127.0.0.1');"
    # On (re)crée l'équipement avec une adresse INJOIGNABLE, état initial UP.
    DB "INSERT INTO equipements (nom,adresse_ip,type_equipement,statut) VALUES ('PC-DEMO','192.0.2.99','Serveur','UP');"

    echo ">> Mise en panne de PC-DEMO (adresse injoignable 192.0.2.99)..."
    echo ">> Cycle 1/2 (1er echec)..."
    $PY supervisor.py >/dev/null 2>&1
    echo ">> Cycle 2/2 (seuil atteint -> ALERTE)..."
    $PY supervisor.py
    echo ">> Une alerte PANNE_RESEAU a du partir sur Telegram + e-mail."
    ;;
  up)
    if [ -z "$(DB "SELECT id FROM equipements WHERE nom='PC-DEMO';")" ]; then
      echo "!! PC-DEMO n'existe pas : lance d'abord 'bash demo_alerte.sh down'."
      exit 1
    fi
    echo ">> Retablissement de PC-DEMO (adresse joignable 127.0.0.1)..."
    DB "UPDATE equipements SET adresse_ip='127.0.0.1' WHERE nom='PC-DEMO';"
    echo ">> Cycle de supervision..."
    $PY supervisor.py
    echo ">> Une notification de RETABLISSEMENT a du partir sur Telegram."
    ;;
  nettoyer|clean)
    echo ">> Suppression de l'equipement de demonstration PC-DEMO..."
    DB "DELETE FROM equipements WHERE nom='PC-DEMO' OR adresse_ip IN ('192.0.2.99','127.0.0.1');"
    echo ">> PC-DEMO retire."
    ;;
  *)
    echo "Usage : bash demo_alerte.sh down   (provoque une panne)"
    echo "        bash demo_alerte.sh up     (retablit l'equipement)"
    echo "        bash demo_alerte.sh clean  (retire le PC-DEMO apres la demo)"
    ;;
esac
