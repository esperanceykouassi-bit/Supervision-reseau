# Tableau de bord de supervision réseau — Awali

Code source **autonome** du tableau de bord web (Flask) du système de
supervision et de détection des pannes réseau, déployé chez OPEN MOISE.

## Contenu
```
dashboard/
├── app.py                 # Application Flask : routes, authentification, API REST JSON
├── config.py              # Configuration centralisée (lue depuis .env)
├── requirements.txt       # Dépendances Python
├── .env.example           # Modèle de configuration (à copier en .env)
├── templates/             # Pages HTML (Jinja2 + Bootstrap 5)
│   ├── base.html          #   gabarit commun (navigation, pied de page)
│   ├── login.html         #   page de connexion sécurisée
│   ├── dashboard.html     #   tableau de bord (KPI, disponibilité, alertes)
│   ├── equipements.html   #   gestion des équipements
│   ├── alertes.html       #   historique des alertes
│   ├── journaux.html      #   journaux de supervision
│   └── rapports.html      #   rapports & statistiques
├── static/
│   ├── css/style.css      # Style personnalisé
│   └── js/dashboard.js    # Graphiques (Chart.js) + rafraîchissement AJAX
└── modules/
    ├── database.py        # Couche d'accès aux données (requêtes paramétrées)
    └── logger.py          # Journalisation applicative
```

## Lancement
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # puis renseigner la base MySQL et SECRET_KEY
python app.py               # → http://<ip>:5000   (admin / admin123)
```

> Le tableau de bord **lit et affiche** les données. La base MySQL doit être
> créée au préalable (`database/schema.sql`) et le moteur `supervisor.py` doit
> avoir tourné au moins une fois pour peupler les équipements et les alertes.
