# Connexion rapide — de la VM au tableau de bord

Ce guide ne sert qu'à **se connecter** au système déjà installé (pas à
l'installer). Pour l'installation complète, voir `docs/INSTALLATION.md`.

## 1. Démarrer la machine virtuelle
Lance la VM depuis VirtualBox/VMware (ou ton hyperviseur). Attends qu'Ubuntu
ait fini de démarrer (invite de connexion affichée sur la console).

## 2. Se connecter à la VM
- **En local (console VM)** : identifiant/mot de passe Ubuntu de la VM.
- **À distance (recommandé)** depuis ton PC, par SSH :
  ```bash
  ssh <utilisateur>@192.168.1.50
  ```
  (remplace `192.168.1.50` par l'IP réelle de la VM — `ip addr` sur la VM pour la vérifier).

## 3. Vérifier que les services tournent

```bash
# MySQL doit être actif
sudo systemctl status mysql

# Si le tableau de bord tourne déjà en service systemd :
sudo systemctl status supervision-web
```

- Si `supervision-web` est **actif** → passe directement à l'étape 5.
- Sinon (lancement manuel, cas le plus fréquent en démo) → étape 4.

## 4. Lancer le tableau de bord manuellement

```bash
cd /opt/supervision/src        # adapter le chemin si différent
source ../venv/bin/activate
python app.py
```

Tu dois voir dans le terminal :
```
Démarrage du tableau de bord Flask sur 0.0.0.0:5000 (HTTP)
```
Laisse ce terminal ouvert (le serveur tourne tant qu'il n'est pas arrêté).

> Pour lancer aussi un cycle de supervision avant la démo :
> `python supervisor.py` (voir aussi `src/demo_live.sh` pour une démo guidée
> avec panne simulée).

## 5. Accéder au tableau de bord depuis le navigateur

Sur ton PC (même réseau que la VM), ouvre :

```
http://192.168.1.50:5000
```

(remplace par l'IP réelle de la VM trouvée à l'étape 2).

## 6. Se connecter

| Champ | Valeur par défaut |
|---|---|
| Identifiant | `admin` |
| Mot de passe | `admin123` |

⚠️ Ce sont les identifiants par défaut créés par `database/schema.sql` —
à changer avant tout usage réel (voir `docs/INSTALLATION.md`, étape 11).

## Dépannage rapide

| Symptôme | Cause probable | Solution |
|---|---|---|
| `ssh: connect to host ... port 22: Connection refused` | VM pas encore démarrée ou SSH non installé | Attendre le boot / `sudo apt install openssh-server` sur la VM |
| Page web inaccessible | Mauvaise IP ou pare-feu | Vérifier `ip addr` sur la VM, `sudo ufw allow 5000` si pare-feu actif |
| `python app.py` plante (MySQL) | MySQL non démarré | `sudo systemctl start mysql` |
| Identifiants refusés | Compte admin déjà modifié | Utiliser le nouveau mot de passe, ou réinitialiser via `database/schema.sql` |
