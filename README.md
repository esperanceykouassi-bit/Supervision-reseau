# Supervision Réseau — Système d'automatisation open-source

> **Mémoire de Master 2 RIT** — *Mise en place d'un système d'automatisation de
> la supervision réseau basé sur des scripts et outils open-source.*

Ce dépôt contient **l'intégralité du travail** : le mémoire rédigé, la conception
(UML, architecture), le **code source fonctionnel** d'un système de supervision
réseau automatisé, la base de données, l'interface web, les tests et le support
de soutenance.

---

## 🎯 Ce que fait le système

- 🔍 **Découverte automatique** des équipements d'un sous-réseau (scan CIDR)
- 📡 **Surveillance** de la disponibilité (sondes **ICMP** et **TCP/services**)
- 📝 **Journalisation** complète de chaque vérification
- 🚨 **Alertes en temps réel** par **e-mail (SMTP)** et **Telegram** (push mobile)
- 📊 **Tableau de bord web** temps réel (état, statistiques, rapports)
- ✅ **Anti-faux positif** (seuil d'échecs) et **anti-spam** (dé-duplication)

**Stack 100 % open-source :** Ubuntu · Python · Cron · MySQL · Flask · Bootstrap.

---

## 📂 Structure du dépôt

| Dossier | Contenu |
|---------|---------|
| [`memoire/`](memoire/) | **Le mémoire complet** (`memoire-complet.md`) : page de garde, problématique, chapitres 1 à 5, conclusion, bibliographie, annexes. |
| [`architecture/`](architecture/) | Architecture technique, schéma réseau et **7 diagrammes UML** (contexte, cas d'utilisation, séquence, activité, classes, composants, déploiement). |
| [`database/`](database/) | **MCD/MLD/MPD** (`mcd-mld.md`) et **script SQL complet** (`schema.sql`). |
| [`src/`](src/) | **Code source** : moteur (`supervisor.py`), application Flask (`app.py`), modules (sondes, alertes, BDD, logs), templates et statiques. |
| [`tests/`](tests/) | Tests unitaires et fonctionnels (`pytest`/`unittest`). |
| [`soutenance/`](soutenance/) | **Support de présentation** (Marp → PPTX), notes de l'orateur, questions/réponses du jury. |
| [`docs/`](docs/) | [Guide d'installation et de déploiement](docs/INSTALLATION.md). |

---

## 🚀 Démarrage rapide

```bash
# 1. Base de données
sudo mysql < database/schema.sql

# 2. Environnement Python
python3 -m venv venv && source venv/bin/activate
pip install -r src/requirements.txt

# 3. Configuration
cd src && cp .env.example .env   # éditer .env (BDD, SMTP, Telegram)

# 4. Découverte + premier cycle
python supervisor.py --decouvrir 192.168.1.0/24
python supervisor.py

# 5. Tableau de bord  ->  http://localhost:5000  (admin / admin123)
python app.py
```

➡️ Guide détaillé : [`docs/INSTALLATION.md`](docs/INSTALLATION.md).

---

## 🧪 Tests

```bash
cd src && python -m pytest ../tests -v      # ou : python -m unittest discover -s ../tests
```

> 9 tests unitaires — **100 % de réussite**.

---

## 📈 Résultats clés (manuel → automatisé)

| Indicateur | Manuel | **Automatisé** |
|------------|:------:|:--------------:|
| Temps de détection (MTTD) | ~30–60 min | **< 2 min** |
| Temps de réaction (MTTR) | ~45 min | **< 5 min** |
| Taux de disponibilité | ~97,5 % | **~99,5 %** |
| Coût de licence | — | **0 FCFA** |

---

## 🔐 Sécurité

Secrets hors du code (`.env`) · mots de passe **hachés** (pbkdf2) · requêtes SQL
**paramétrées** · SMTP **STARTTLS** · API Telegram **HTTPS** · principe du
**moindre privilège** pour le compte MySQL.

> ⚠️ **Changez les identifiants par défaut (`admin`/`admin123`) avant tout usage réel.**

---

## 📜 Licence

Projet académique réalisé dans le cadre d'un mémoire de Master 2 RIT (2025–2026).
Briques technologiques sous licences open-source respectives.
