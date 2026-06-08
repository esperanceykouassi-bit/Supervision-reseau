# Guide d'installation et de déploiement

Ce guide décrit l'installation complète du système de supervision sur un serveur
**Ubuntu Server 22.04 LTS**. Comptez environ 30 minutes.

## 1. Prérequis

- Serveur Ubuntu 22.04 LTS (physique, VM ou conteneur)
- Accès `sudo`
- Adresse IP fixe recommandée
- Accès Internet sortant (SMTP 587, HTTPS 443 pour Telegram)

## 2. Installation des paquets système

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip mysql-server git iputils-ping
```

## 3. Récupération du projet

```bash
sudo mkdir -p /opt/supervision
sudo chown $USER:$USER /opt/supervision
git clone <URL_DU_DEPOT> /opt/supervision
cd /opt/supervision
```

## 4. Configuration de la base de données

```bash
# Sécuriser MySQL (facultatif mais recommandé)
sudo mysql_secure_installation

# Créer la base, les tables et les données d'amorçage
sudo mysql < database/schema.sql
```

> Le script crée la base `supervision`, l'utilisateur applicatif `supervisor`
> et un compte administrateur par défaut (**admin / admin123** — à changer !).

## 5. Environnement Python

```bash
cd /opt/supervision
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r src/requirements.txt
```

## 6. Configuration des secrets (.env)

```bash
cd src
cp .env.example .env
nano .env          # renseigner BDD, SMTP, Telegram, SECRET_KEY
```

Générer une clé secrète Flask solide :

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 7. Premier test manuel

```bash
cd /opt/supervision/src
source ../venv/bin/activate

# Découverte du réseau local (adapter le CIDR)
python supervisor.py --decouvrir 192.168.1.0/24

# Un cycle de supervision
python supervisor.py
```

## 8. Lancement du tableau de bord

### En développement
```bash
python app.py        # http://<ip-serveur>:5000
```

### En production (Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 --workers 3 app:app
```

## 9. Planification avec Cron

```bash
# Adapter les chemins dans le fichier puis l'installer
sudo cp cron/supervision.cron /etc/cron.d/supervision
sudo systemctl restart cron
```

Vérifier l'exécution :

```bash
tail -f /opt/supervision/src/logs/cron.log
```

## 10. (Option) Service systemd pour le tableau de bord

Créer `/etc/systemd/system/supervision-web.service` :

```ini
[Unit]
Description=Tableau de bord Supervision Reseau
After=network.target mysql.service

[Service]
User=www-data
WorkingDirectory=/opt/supervision/src
ExecStart=/opt/supervision/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 3 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now supervision-web
```

## 11. Vérifications finales

- [ ] Le tableau de bord est accessible et la connexion fonctionne.
- [ ] `python supervisor.py` met à jour les statuts en base.
- [ ] Une panne simulée déclenche bien une alerte e-mail **et** Telegram.
- [ ] Les identifiants par défaut ont été **changés**.
- [ ] Les journaux tournent correctement dans `src/logs/`.

## Dépannage

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| `Access denied` MySQL | Mauvais identifiants `.env` | Vérifier `DB_USER`/`DB_PASSWORD` |
| Pas d'alerte e-mail | SMTP mal configuré | Vérifier hôte/port/mot de passe applicatif |
| Pas d'alerte Telegram | Token/chat_id absent | Voir Annexe F du mémoire |
| Ping échoue toujours | Pare-feu bloque ICMP | Autoriser ICMP ou utiliser la sonde TCP |
