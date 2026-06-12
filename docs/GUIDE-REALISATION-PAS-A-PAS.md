# Guide pas à pas — Réalisation du projet

> **Automatisation de la supervision et de la détection des pannes réseau**
> Solution open-source : Ubuntu · Python · Cron · MySQL · Flask · Telegram.
> Ce guide décrit, étape par étape, comment **refaire le projet** depuis zéro,
> de l'environnement jusqu'au déploiement et aux livrables.

---

## PHASE 0 — Préparation

### Étape 0.1 — Matériel / environnement
- Un **serveur ou PC sous Linux** (Ubuntu Server 22.04 LTS recommandé), physique,
  machine virtuelle (VirtualBox/VMware) ou conteneur.
- Une **adresse IP fixe** pour ce serveur (service permanent).
- Un **accès Internet sortant** (pour les alertes e-mail et Telegram).
- Quelques **équipements à superviser** sur le réseau local (routeur, switch,
  serveur, imprimante…) — réels ou simulés par des machines virtuelles.

### Étape 0.2 — Mettre à jour le système
```bash
sudo apt update && sudo apt upgrade -y
```

### Étape 0.3 — Installer les paquets de base
```bash
sudo apt install -y python3 python3-venv python3-pip mysql-server git iputils-ping
```

---

## PHASE 1 — Conception (avant de coder)

### Étape 1.1 — Analyser le besoin
Lister les **besoins fonctionnels** (découverte, sondes, alertes, tableau de bord)
et **non fonctionnels** (performance, sécurité, fiabilité). *(Voir mémoire, chap. 6.)*

### Étape 1.2 — Concevoir l'architecture (5 couches)
Système (Ubuntu) → Données (MySQL) → Traitement (Python + Cron) →
Notification (SMTP + Telegram) → Présentation (Flask + Bootstrap).

### Étape 1.3 — Modéliser
- **UML** (7 diagrammes : contexte, cas d'utilisation, séquence, activité,
  classes, composants, déploiement) avec PlantUML.
- **MERISE** : MCD → MLD → script SQL (6 tables).

---

## PHASE 2 — Base de données

### Étape 2.1 — Sécuriser MySQL (recommandé)
```bash
sudo mysql_secure_installation
```

### Étape 2.2 — Créer la base et les tables
Le script `database/schema.sql` crée la base `supervision`, l'utilisateur
applicatif `supervisor`, les **6 tables** (utilisateurs, equipements, journaux,
alertes, responsabilite, statistiques) et un compte admin par défaut.
```bash
sudo mysql < database/schema.sql
```
> Compte par défaut : **admin / admin123** (à changer impérativement).

---

## PHASE 3 — Code et environnement Python

### Étape 3.1 — Récupérer le projet
```bash
sudo mkdir -p /opt/supervision && sudo chown $USER:$USER /opt/supervision
git clone <URL_DU_DEPOT> /opt/supervision
cd /opt/supervision
```

### Étape 3.2 — Créer l'environnement virtuel et installer les dépendances
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r src/requirements.txt
```

### Étape 3.3 — Comprendre les modules développés (dossier `src/`)
- `config.py` — configuration centralisée (lue depuis `.env`).
- `modules/database.py` — couche d'accès aux données (requêtes paramétrées).
- `modules/ping_monitor.py` — **sonde ICMP** (ping + latence).
- `modules/service_monitor.py` — **sonde de service TCP** (HTTP, SSH, MySQL…).
- `modules/detection.py` — **découverte automatique** (scan CIDR parallélisé).
- `modules/logger.py` — journalisation avec rotation.
- `modules/alertes/` — alertes **e-mail (SMTP)** et **Telegram**, avec anti-spam.
- `supervisor.py` — **moteur** (exécuté par Cron).
- `app.py` — **tableau de bord Flask** + API REST.

---

## PHASE 4 — Configuration (secrets)

### Étape 4.1 — Créer le fichier `.env`
```bash
cd src
cp .env.example .env
nano .env
```
Renseigner : base de données, SMTP, Telegram, `SECRET_KEY`.

### Étape 4.2 — Générer une clé secrète Flask
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Étape 4.3 — Créer le bot Telegram
1. Sur Telegram, contacter **@BotFather** → `/newbot` → récupérer le **token**.
2. Démarrer une conversation avec le bot.
3. Récupérer le **chat_id** :
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Renseigner `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID` dans `.env`.

### Étape 4.4 — Configurer le SMTP (e-mail)
Renseigner `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
(pour Gmail : créer un **mot de passe d'application**).

---

## PHASE 5 — Mise en service et tests

### Étape 5.1 — Découvrir le réseau (auto-inventaire)
```bash
cd /opt/supervision/src
source ../venv/bin/activate
python supervisor.py --decouvrir 192.168.1.0/24   # adapter au sous-réseau
```

### Étape 5.2 — Lancer un cycle de supervision manuel
```bash
python supervisor.py
```
Vérifier dans la base que les statuts (UP/DOWN) et journaux se mettent à jour.

### Étape 5.3 — Tester la chaîne d'alerte
Éteindre/débrancher un équipement, relancer le cycle deux fois :
→ une **alerte e-mail + Telegram** doit arriver après le seuil d'échecs.
Le rallumer → notification de **rétablissement**.

### Étape 5.4 — Exécuter les tests automatisés
```bash
cd /opt/supervision/src
python -m pytest ../tests -v        # ou : python -m unittest discover -s ../tests
```
→ 9 tests unitaires doivent passer (100 %).

---

## PHASE 6 — Automatisation (Cron)

### Étape 6.1 — Planifier le moteur
```bash
sudo cp src/cron/supervision.cron /etc/cron.d/supervision
sudo systemctl restart cron
```
Par défaut : un **cycle toutes les 2 minutes** + une **découverte quotidienne** à 3 h.

### Étape 6.2 — Vérifier l'exécution périodique
```bash
tail -f /opt/supervision/src/logs/cron.log
```

---

## PHASE 7 — Tableau de bord (interface web)

### Étape 7.1 — Lancer en développement
```bash
cd /opt/supervision/src
python app.py            # http://<ip-serveur>:5000   (admin / admin123)
```

### Étape 7.2 — Déployer en production (Gunicorn + systemd)
```bash
gunicorn --bind 0.0.0.0:5000 --workers 3 app:app
```
Créer un service systemd (voir `docs/INSTALLATION.md`) pour un démarrage
automatique au boot.

---

## PHASE 8 — Évaluation des résultats

### Étape 8.1 — Mesurer les indicateurs
Comparer **avant/après** (manuel vs automatisé) : MTTD, MTTR, taux de
disponibilité, latence moyenne (données issues des journaux et des rapports).

### Étape 8.2 — Produire les tableaux et graphiques
Page **Rapports** du tableau de bord (export PDF/impression).

---

## PHASE 9 — Sécurité et bonnes pratiques

- **Changer** les identifiants par défaut (admin/admin123).
- Garder les **secrets hors du code** (fichier `.env` non versionné).
- Placer le serveur sur un **VLAN d'administration** + **IP fixe**.
- L'adosser à un **onduleur (UPS)**.
- **Sauvegarder** régulièrement la base de données.
- Prévoir une **redondance** pour les environnements critiques.

---

## PHASE 10 — Livrables (documentation et soutenance)

> *Outils utilisés pour produire les livrables (reproductibles) :*

| Livrable | Commande |
|----------|----------|
| Diagrammes UML + MERISE (PNG) | `java -jar plantuml.jar architecture/diagrammes/*.puml database/*.puml` |
| Schéma d'architecture 5 couches | `python architecture/generer_architecture_5couches.py` |
| Captures de la maquette (tableau de bord…) | `python soutenance/generer_captures.py` |
| Support de soutenance (PowerPoint) | `python soutenance/generer_pptx.py` |
| Mémoire (Word) | `cd memoire && bash build.sh` (pandoc) |
| Vidéo de démonstration | `python soutenance/generer_video_demo.py` (ffmpeg) |

---

## Récapitulatif express (mémo)

```
0. Préparer Ubuntu + paquets (python, mysql, git)
1. Concevoir (UML, MERISE, architecture 5 couches)
2. Créer la base :        sudo mysql < database/schema.sql
3. Installer le code :    python3 -m venv venv ; pip install -r src/requirements.txt
4. Configurer :           cp .env.example .env  (BDD, SMTP, Telegram, SECRET_KEY)
5. Découvrir + tester :   python supervisor.py --decouvrir 192.168.1.0/24 ; python supervisor.py
6. Automatiser :          cron (cycle 2 min)
7. Lancer l'interface :   python app.py  ->  http://<ip>:5000
8. Mesurer / sécuriser / sauvegarder
9. Produire les livrables (diagrammes, PPTX, mémoire, vidéo)
```
