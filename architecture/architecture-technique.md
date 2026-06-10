# Architecture technique

Ce document décrit la **pile technologique** retenue et **justifie chaque
choix** au regard des objectifs du mémoire (automatisation, temps réel,
réduction du temps d'intervention, exclusivité de l'open-source).

## 1. Vue en couches

![Architecture en 5 couches](architecture-5couches.png)

```
┌──────────────────────────────────────────────────────────────────┐
│  COUCHE PRÉSENTATION                                               │
│  Tableau de bord Web (Flask + Jinja2 + Bootstrap 5 + Chart.js)     │
│  → Visualisation temps réel, gestion des équipements, rapports     │
├──────────────────────────────────────────────────────────────────┤
│  COUCHE TRAITEMENT / MÉTIER                                        │
│  Moteur Python (supervisor.py) + modules :                         │
│    detection · ping_monitor · service_monitor · alertes            │
│  Ordonnancement : Cron (exécution périodique)                      │
├──────────────────────────────────────────────────────────────────┤
│  COUCHE NOTIFICATION                                               │
│  SMTP (e-mail) · API Bot Telegram (push mobile)                    │
├──────────────────────────────────────────────────────────────────┤
│  COUCHE DONNÉES                                                    │
│  Base de données MySQL (équipements, journaux, alertes, users…)    │
├──────────────────────────────────────────────────────────────────┤
│  COUCHE SYSTÈME                                                    │
│  Serveur Linux Ubuntu Server 22.04 LTS                             │
└──────────────────────────────────────────────────────────────────┘
```

## 2. Justification des choix technologiques

| Brique | Technologie | Justification |
|--------|-------------|---------------|
| **Système d'exploitation** | Ubuntu Server 22.04 LTS | Distribution Linux gratuite, stable (support LTS jusqu'en 2027), large communauté, légère (fonctionne sur peu de ressources), outils réseau natifs (`ping`, `cron`). |
| **Langage** | Python 3 | Lisibilité, productivité, riche écosystème réseau (sockets, subprocess), idéal pour le scripting d'automatisation. |
| **Ordonnancement** | Cron | Présent nativement sous Linux, fiable, éprouvé, sans dépendance externe. Découple la collecte de l'interface web. |
| **Base de données** | MySQL 8 | SGBD relationnel open-source robuste, transactionnel (InnoDB), performant en lecture pour le tableau de bord. |
| **Framework web** | Flask | Micro-framework léger, courbe d'apprentissage faible, parfait pour une application de taille moyenne. Évite la lourdeur de Django. |
| **Front-end** | Bootstrap 5 + Chart.js | Interface responsive professionnelle sans expertise design ; graphiques dynamiques côté navigateur. |
| **Alerte e-mail** | SMTP (smtplib) | Standard universel, traçabilité écrite, intégration aux outils de ticketing. |
| **Alerte instantanée** | Bot Telegram | Notification *push* gratuite et quasi instantanée sur smartphone → **réduction directe du temps de réaction**. |

## 3. Flux de données (résumé)

1. **Cron** déclenche `supervisor.py` toutes les 2 minutes.
2. Le moteur lit la liste des **équipements** depuis **MySQL**.
3. Pour chacun, il lance une **sonde ICMP** (et éventuellement une **sonde de service TCP**).
4. Le résultat est **journalisé** et le **statut** mis à jour en base.
5. En cas de panne confirmée (seuil d'échecs), le **gestionnaire d'alertes** émet
   une notification **e-mail + Telegram** et enregistre l'alerte.
6. Le **tableau de bord Flask** lit en continu la base pour afficher l'état
   temps réel et permettre l'**acquittement** des alertes.

## 4. Sécurité (principes appliqués)

- **Secrets hors du code** : identifiants et jetons dans des variables
  d'environnement (`.env` non versionné).
- **Requêtes SQL paramétrées** : protection contre l'injection SQL.
- **Hachage des mots de passe** : `pbkdf2:sha256` via Werkzeug (jamais en clair).
- **Moindre privilège** : compte MySQL applicatif limité au strict nécessaire.
- **Chiffrement des notifications** : SMTP STARTTLS, API Telegram en HTTPS.
- **Authentification** de l'accès au tableau de bord (sessions Flask).
