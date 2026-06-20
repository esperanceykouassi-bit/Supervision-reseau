#!/usr/bin/env bash
# ====================================================================== #
#  demo_live.sh — Démonstration EN DIRECT, guidée et rythmée.            #
#  ----------------------------------------------------------------------#
#  Lance ce script pendant la soutenance : il déroule la démo étape par  #
#  étape, en s'arrêtant à chaque pause (touche Entrée) pour te laisser   #
#  commenter et montrer le téléphone / le tableau de bord.               #
#                                                                         #
#  Pré-requis : le dashboard tourne (http://<ip>:5000) et le .env        #
#  contient les identifiants Telegram + e-mail.                          #
#  Usage : bash demo_live.sh                                             #
# ====================================================================== #
cd "$(dirname "$0")"
pause(){ echo; read -p "      ▶  Appuyez sur [Entrée] pour continuer..."; echo; }

clear
cat <<'BANNER'
  ==================================================================
     DÉMONSTRATION EN DIRECT  —  SupervisionNet
     Supervision et détection des pannes réseau en temps réel
  ==================================================================
BANNER
echo
echo "  Le tableau de bord est ouvert dans le navigateur :"
echo "        http://192.168.1.50:5000   (admin / admin123)"
echo "  Montrez l'état du parc : équipements supervisés, taux de disponibilité."
pause

echo "  >>> ÉTAPE 1 — Écran propre (on acquitte les alertes précédentes)"
mysql -u supervisor -psupervision_pass supervision -e "UPDATE alertes SET acquittee=1;" 2>/dev/null
echo "      ✓ Rechargez le dashboard : le compteur « Alertes actives » est à 0."
pause

echo "  >>> ÉTAPE 2 — On PROVOQUE une panne réseau sur un équipement (PC-DEMO)"
echo "      Le moteur va le sonder : après 2 échecs, l'alerte se déclenche."
echo "  ------------------------------------------------------------------"
bash demo_alerte.sh down
echo "  ------------------------------------------------------------------"
echo "      📲  TÉLÉPHONE : une alerte 🔴 PANNE_RESEAU arrive sur Telegram."
echo "      📧  E-MAIL   : la même alerte arrive dans la boîte Gmail."
echo "      🖥️   DASHBOARD : rechargez → PC-DEMO apparaît en ROUGE (DOWN)."
pause

echo "  >>> ÉTAPE 3 — On RÉTABLIT l'équipement (retour à la normale)"
echo "  ------------------------------------------------------------------"
bash demo_alerte.sh up
echo "  ------------------------------------------------------------------"
echo "      📲  TÉLÉPHONE : notification 🟠 de RÉTABLISSEMENT."
echo "      🖥️   DASHBOARD : rechargez → PC-DEMO repasse en VERT (UP)."
pause

echo "  >>> ÉTAPE 4 — Nettoyage de fin de démonstration"
bash demo_alerte.sh clean
echo
cat <<'END'
  ==================================================================
     FIN DE LA DÉMONSTRATION
     De la supervision réactive vers une supervision proactive.
     Détection < 2 min  •  Alerte multi-canal  •  Coût de licence : 0 FCFA
  ==================================================================
END
