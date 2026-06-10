# CHAPITRE 7 — FONCTIONNEMENT DE LA SOLUTION : POINT DE VUE TECHNIQUE

Ce chapitre décrit la réalisation concrète du système. Le code source complet et
commenté est organisé dans l'arborescence du projet ; les extraits clés sont
présentés ci-dessous.

## 7.1 Arborescence du projet

```
Supervision-reseau/
├── architecture/        # Conception : UML, schémas, justification technique
├── database/            # MCD/MLD + script SQL complet (schema.sql)
├── src/                 # CODE SOURCE
│   ├── app.py           # Application web Flask (tableau de bord + API REST)
│   ├── supervisor.py    # Moteur de supervision (lancé par Cron)
│   ├── config.py        # Configuration centralisée (variables d'environnement)
│   ├── requirements.txt # Dépendances Python
│   ├── cron/            # Planification Cron
│   ├── modules/         # Logique métier
│   │   ├── database.py       # Couche d'accès aux données (DAL)
│   │   ├── logger.py         # Journalisation avec rotation
│   │   ├── ping_monitor.py   # Sonde ICMP
│   │   ├── service_monitor.py# Sonde de services TCP
│   │   ├── detection.py      # Découverte automatique du réseau
│   │   └── alertes/          # Alertes multi-canal (e-mail + Telegram)
│   ├── templates/       # Vues HTML (Jinja2 + Bootstrap)
│   └── static/          # CSS + JavaScript (Chart.js)
└── tests/               # Tests unitaires et fonctionnels
```

## 7.2 Le moteur de supervision (cycle automatisé)

Le **moteur** (`supervisor.py`) est exécuté périodiquement par **Cron**. À
chaque cycle, il : (1) charge les équipements actifs depuis MySQL ; (2) lance la
sonde ICMP, puis éventuellement la sonde de service ; (3) met à jour le statut et
journalise ; (4) applique le **seuil d'échecs consécutifs** ; (5) déclenche les
alertes en cas de panne confirmée ; (6) notifie le **rétablissement** au retour
en ligne.

```python
def superviser_equipement(equipement):
    """Supervise un équipement : ping + éventuelle sonde de service."""
    nom, ip = equipement["nom"], equipement["adresse_ip"]
    ancien_statut = equipement.get("statut")

    statut, latence = ping(ip)                 # sonde ICMP (couche 3)
    service = equipement.get("service_supervise")
    message = ""
    if statut == "UP" and service:             # sonde de service (couche 4-7)
        ouvert, _ = verifier_service(ip, service)
        if not ouvert:
            statut = "DOWN"
            message = f"Hôte joignable mais service {service} indisponible."

    database.update_statut_equipement(equipement["id"], statut, latence)
    database.add_journal(equipement["id"], statut, latence, message or "OK")

    if statut == "DOWN":
        echecs = _compter_echecs_consecutifs(equipement["id"])
        if echecs >= config.FAILURE_THRESHOLD:        # anti-faux positif
            alertes.declencher_alerte(equipement, "PANNE_RESEAU", "CRITIQUE",
                                      message or f"{nom} ({ip}) ne répond plus.")
    elif statut == "UP" and ancien_statut == "DOWN":  # transition DOWN -> UP
        alertes.alerte_retablissement(equipement, f"{nom} est de nouveau en ligne.")
    return statut, latence
```

La planification Cron exécute un cycle **toutes les deux minutes** et une
**découverte réseau quotidienne** :

```
*/2 * * * * cd /opt/supervision/src && python supervisor.py
0 3 * * *   cd /opt/supervision/src && python supervisor.py --decouvrir 192.168.1.0/24
```

## 7.3 La découverte automatique des équipements

Le module `detection.py` balaie un sous-réseau (notation **CIDR**) en
**parallélisant** les pings via un *pool* de threads — un balayage séquentiel
d'un `/24` (254 hôtes) prendrait plusieurs minutes contre quelques secondes en
parallèle. Chaque hôte actif fait l'objet d'une résolution DNS inverse, puis est
enregistré s'il n'existe pas déjà.

```python
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = {executor.submit(_scanner_hote, ip): ip for ip in hotes}
    for future in as_completed(futures):
        resultat = future.result()
        if resultat:
            actifs.append(resultat)
```

## 7.4 Les sondes de disponibilité

### 7.4.1 Sonde ICMP (ping)

La sonde ICMP teste la joignabilité en couche réseau via la commande système
`ping` (portable Windows/Linux), avec un *timeout* de sécurité, et extrait la
**latence moyenne (RTT)** par expression régulière.

```python
def ping(adresse_ip):
    commande = ["ping", param_count, str(config.PING_COUNT),
                param_timeout, str(config.PING_TIMEOUT), adresse_ip]
    resultat = subprocess.run(commande, capture_output=True, text=True,
                              timeout=config.PING_TIMEOUT * config.PING_COUNT + 5)
    if resultat.returncode == 0:
        return "UP", _extraire_latence(resultat.stdout)
    return "DOWN", None
```

### 7.4.2 Sonde de service (TCP)

La sonde de service teste l'ouverture d'un port **TCP** (HTTP, SSH, MySQL…) par
une tentative de connexion (*3-way handshake*). Elle détecte le cas où un hôte
répond au ping tout en ayant son service applicatif hors d'usage.

## 7.5 La gestion des alertes multi-canal

Le **gestionnaire d'alertes** orchestre la diffusion sur tous les canaux et
applique une logique **anti-spam** : une seule alerte est émise par panne tant
qu'elle n'est pas résolue ou acquittée.

```python
def declencher_alerte(equipement, type_alerte, severite, message):
    if database.derniere_alerte_active(equipement["id"], type_alerte):
        return False                    # anti-spam : alerte déjà active
    database.add_alerte(equipement["id"], type_alerte, severite, message,
                        canal="EMAIL+TELEGRAM")
    envoyer_alerte_email(equipement, type_alerte, severite, message)
    envoyer_alerte_telegram(equipement, type_alerte, severite, message)
    return True
```

- **Canal e-mail (SMTP, STARTTLS)** : message HTML formaté, traçabilité écrite ;
- **Canal Telegram (API Bot, HTTPS)** : notification *push* mobile quasi
  instantanée, levier central de la réduction du temps de réaction.

## 7.6 Le tableau de bord web (Flask)

L'application `app.py` fournit l'interface : **authentification**, **tableau de
bord** temps réel (KPI, graphiques), **gestion des équipements** (CRUD),
**historique des alertes** (avec acquittement), **journaux**, **rapports**, et
une **API REST JSON** consommée par le front pour le rafraîchissement AJAX.
Flask se contente de **lire** la base, ce qui garde l'interface légère et
réactive.

## 7.7 Sécurité « by design »

La sécurité a été intégrée dès la conception, conformément aux bonnes pratiques
(OWASP) :

| Risque | Parade implémentée |
|--------|--------------------|
| Secrets dans le code | Variables d'environnement (fichier `.env` non versionné) |
| Vol de mots de passe | **Hachage** `pbkdf2:sha256` (jamais en clair) |
| Injection SQL | **Requêtes paramétrées** systématiques |
| Écoute des notifications | **SMTP STARTTLS** + Telegram **HTTPS** |
| Accès base trop large | Compte applicatif au **moindre privilège** |
| Accès non autorisé | **Authentification** du tableau de bord (sessions Flask) |

## 7.8 Tests et validation

La validation s'appuie sur trois niveaux : **tests unitaires** (9 cas, 100 % de
réussite — analyse de la latence, sonde TCP, logique de seuil), **tests
fonctionnels** (détection, anti-spam, rétablissement, service indisponible,
découverte, authentification) et **tests de performance**.

| Nombre d'équipements | Cycle séquentiel | Cycle parallélisé |
|:--------------------:|:----------------:|:-----------------:|
| 50 | ~30 s | **~4 s** |
| 100 | ~60 s | **~7 s** |
| 254 (`/24`) | ~150 s | **~12 s** |

La **parallélisation** réduit le temps de balayage d'un facteur 10 à 15,
validant le besoin de performance (BNF1).

## 7.9 La configuration centralisée et la gestion des secrets

L'ensemble des paramètres est centralisé dans `config.py` et chargé depuis des
**variables d'environnement** (fichier `.env` non versionné). Ce choix répond à
deux exigences : la **sécurité** (aucun secret en clair dans le code) et la
**portabilité** (un même code s'exécute en développement, en test et en
production, en changeant seulement le fichier d'environnement). Les paramètres
incluent les accès à la base, les identifiants SMTP, le jeton du bot Telegram,
ainsi que les réglages de sonde (nombre de paquets, *timeout*, seuil d'échecs).

## 7.10 La couche d'accès aux données (DAL)

Toutes les interactions avec MySQL sont encapsulées dans un unique module
`database.py` (*Data Access Layer*). Cette centralisation présente trois
avantages : elle **isole** la logique SQL, **facilite la maintenance** et
**réduit la surface d'attaque** par injection, toutes les requêtes étant
**paramétrées**. Un **pool de connexions** est utilisé pour de meilleures
performances sous charge, et un gestionnaire de contexte (`with`) garantit la
fermeture systématique des connexions, même en cas d'exception.

## 7.11 Description des tables de la base de données

La base `supervision` comporte **six tables** :

- **`utilisateurs`** : comptes d'accès au tableau de bord. Le mot de passe est
  stocké uniquement sous forme de **hachage** ; un champ `role` distingue
  administrateur, opérateur et lecteur.
- **`equipements`** : inventaire et **état courant** de chaque équipement (nom,
  adresse IP unique, type, emplacement, service supervisé, statut, latence, date
  de dernière vérification).
- **`journaux`** : historique de **chaque vérification** (statut, latence,
  message, horodatage). C'est la table qui alimente les statistiques de
  disponibilité et constitue la **preuve de SLA**.
- **`alertes`** : alertes émises, avec type, sévérité, canal de diffusion, état
  d'**acquittement** et dates. Elle porte la logique anti-spam (recherche d'une
  alerte active du même type) et trace, via `acquittee_par`, l'**utilisateur**
  qui a pris en charge l'alerte.
- **`responsabilite`** : table associative reliant `utilisateurs` et
  `equipements`. Elle matérialise la relation **« supervise »**
  (plusieurs-à-plusieurs) : un technicien est responsable de plusieurs
  équipements, et un équipement peut être suivi par plusieurs techniciens. Sa
  clé primaire est **composite** (`utilisateur_id`, `equipement_id`).
- **`statistiques`** : agrégats journaliers (instantanés) pour les rapports de
  tendance.

Les contraintes d'**intégrité référentielle** (clés étrangères avec suppression
en **cascade**) garantissent la cohérence : la suppression d'un équipement purge
automatiquement ses journaux et alertes.

## 7.12 La journalisation applicative

Indépendamment des journaux métier stockés en base, le système tient un
**journal applicatif** (`logger.py`) écrit à la fois dans un **fichier tournant**
(rotation automatique pour éviter la saturation du disque — point critique sur un
serveur de supervision) et dans la console (exploitable via `journalctl`). Cette
double sortie facilite l'exploitation et le diagnostic en production.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
