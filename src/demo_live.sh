#!/usr/bin/env bash
cd "$(dirname "$0")"

# Acquitte les alertes précédentes
mysql -u supervisor -psupervision_pass supervision -e "UPDATE alertes SET acquittee=1;" 2>/dev/null

# Provoque la panne réseau immédiatement
bash demo_alerte.sh down
