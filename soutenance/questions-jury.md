# Questions probables du jury et réponses détaillées

Ce document anticipe les questions du jury et propose des réponses argumentées.
Il faut maîtriser ces points pour défendre sereinement le mémoire.

---

## A. Questions sur les choix techniques

**Q1. Pourquoi développer votre propre solution plutôt que d'utiliser Nagios ou Zabbix ?**

> Nagios et Zabbix sont excellents mais présentent deux freins pour une petite
> structure : une **complexité de déploiement et de configuration** élevée, et
> une **consommation de ressources** importante (surtout Zabbix). Mon objectif
> était de démontrer qu'une solution **légère, totalement maîtrisée et
> personnalisable** pouvait être bâtie avec des scripts. De plus, mon système
> intègre **nativement la notification Telegram**, souvent absente ou payante
> dans les solutions existantes. Enfin, développer la solution avait une forte
> **valeur pédagogique** : cela mobilise l'ensemble des compétences du Master.

**Q2. Pourquoi Python et pas Bash ou un autre langage ?**

> Python offre le meilleur compromis : **lisibilité**, **richesse de
> l'écosystème** (sockets, subprocess, requests), **portabilité** et **gestion
> des structures de données** bien supérieure à Bash. Il s'est imposé comme le
> standard de l'automatisation réseau. Bash aurait suffi pour de simples pings,
> mais pas pour la logique métier, la base de données et l'API web.

**Q3. Pourquoi Cron et pas un démon (service) qui tourne en continu ?**

> Cron est **natif, fiable et éprouvé** sous Linux, sans dépendance. Il garantit
> l'exécution périodique même après un redémarrage du serveur. Un démon
> permanent serait plus réactif (intervalle < 1 min) mais plus complexe à rendre
> robuste (gestion des plantages, supervision du superviseur). Cron à 2 minutes
> offre un excellent compromis réactivité/simplicité. Le code est d'ailleurs
> conçu pour fonctionner aussi en mode démon si besoin.

**Q4. Pourquoi MySQL et pas SQLite ou PostgreSQL ?**

> SQLite aurait suffi pour un prototype mono-utilisateur, mais MySQL gère mieux
> les **accès concurrents** (le moteur écrit pendant que l'interface lit) et la
> **montée en charge**. PostgreSQL aurait été un choix tout aussi valable ; j'ai
> retenu MySQL pour sa **simplicité de mise en œuvre** et sa très large diffusion.

---

## B. Questions sur le fonctionnement

**Q5. Comment évitez-vous les fausses alertes (faux positifs) ?**

> J'applique un **seuil d'échecs consécutifs** (paramétrable, 2 par défaut) :
> une alerte n'est déclenchée qu'après plusieurs cycles d'échec, ce qui filtre
> les pertes ponctuelles d'un seul paquet. J'ai aussi une logique **anti-spam** :
> une seule alerte est émise par panne tant qu'elle n'est pas résolue ou acquittée.

**Q6. Comment le système sait-il qu'un équipement est réparé ?**

> À chaque cycle, le statut est recalculé. Lors de la transition **DOWN → UP**,
> le système émet une **notification de rétablissement** et **acquitte
> automatiquement** les alertes de panne ouvertes pour cet équipement.

**Q7. Que se passe-t-il si le serveur de supervision lui-même tombe ?**

> C'est une limite connue (« qui surveille le surveillant ? »). Je recommande de
> l'adosser à un **onduleur**, et pour les environnements critiques, de déployer
> un **second serveur en veille** (redondance). On peut aussi mettre en place un
> **watchdog externe** (un service tiers qui pingue le superviseur).

**Q8. La différence entre une sonde ICMP et une sonde de service ?**

> La **sonde ICMP (ping)** teste la joignabilité au niveau **couche 3 (réseau)**.
> La **sonde de service (TCP)** teste l'ouverture d'un **port applicatif**
> (couche 4/7). Un serveur peut répondre au ping tout en ayant son service web
> planté : la sonde TCP détecte ce cas que le ping ne verrait pas.

---

## C. Questions sur la sécurité

**Q9. Comment sécurisez-vous les mots de passe et les secrets ?**

> Les **secrets** (mots de passe BDD, token Telegram, identifiants SMTP) sont
> stockés dans des **variables d'environnement** (fichier `.env` non versionné),
> jamais dans le code. Les **mots de passe utilisateurs** sont **hachés**
> (`pbkdf2:sha256` via Werkzeug), jamais en clair. Les requêtes SQL sont
> **paramétrées** (protection contre l'injection SQL). Les communications SMTP
> utilisent **STARTTLS** et l'API Telegram passe en **HTTPS**.

**Q10. Votre système est-il vulnérable aux injections SQL ?**

> Non. **Toutes** les requêtes utilisent des **requêtes préparées paramétrées**
> (placeholders `%s`), ce qui sépare le code SQL des données et neutralise les
> injections. Aucune concaténation de chaîne n'est utilisée pour bâtir des requêtes.

---

## D. Questions sur la méthodologie et les résultats

**Q11. Comment avez-vous mesuré la réduction du temps de détection ?**

> Par **comparaison avant/après**. En supervision manuelle, la détection dépend
> du signalement des utilisateurs (30 à 60 min en moyenne). En automatisé, elle
> est bornée par l'intervalle de cycle : **au plus 2 minutes**. Les journaux du
> système horodatent précisément chaque détection, ce qui rend la mesure objective.

**Q12. Vos chiffres de disponibilité (99,5 %) sont-ils réels ou estimés ?**

> Ce sont des **estimations** issues de l'environnement de test, à valeur
> **indicative**. La méthodologie de calcul (disponibilité = temps en service /
> temps total) est rigoureuse, mais une validation en production sur plusieurs
> mois serait nécessaire pour des chiffres définitifs. Je le mentionne
> honnêtement dans la section « Discussion ».

**Q13. Quelles sont les limites de votre travail ?**

> Trois principales : (1) la supervision active ne mesure pas les **métriques
> internes** (CPU, RAM) que fournirait SNMP ; (2) la réactivité est **bornée par
> l'intervalle** de 2 minutes ; (3) les alertes dépendent de la **connectivité
> Internet sortante**. Ces limites sont assumées et ouvrent mes perspectives.

---

## E. Questions d'ouverture

**Q14. Comment intégreriez-vous l'intelligence artificielle ?**

> En collectant l'historique de latence et de disponibilité (déjà stocké), on
> peut entraîner un modèle de **détection d'anomalies** (par ex. *Isolation
> Forest* ou un modèle de série temporelle) qui repère des comportements
> anormaux **avant** la panne franche. À plus long terme, des modèles de
> **régression** permettraient une **maintenance prédictive** : anticiper la
> défaillance d'un équipement à partir de ses tendances.

**Q15. Votre solution passe-t-elle à l'échelle pour 1000 équipements ?**

> Le moteur **parallélise** les sondes, donc le temps de cycle reste maîtrisé.
> Pour 1000 équipements, on **augmenterait le nombre de threads** et l'on
> **répartirait** éventuellement la collecte sur plusieurs sondes (architecture
> distribuée), en conservant une base centralisée. La couche de données
> resterait à optimiser (index, partitionnement de l'historique).

**Q16. Pourquoi Telegram et pas un SMS ?**

> Telegram est **gratuit**, **chiffré**, fiable et instantané, et son **API est
> simple**. Le SMS implique un coût et une passerelle tierce. Cela dit,
> l'architecture **modulaire** des canaux d'alerte permet d'ajouter facilement
> un canal SMS, Slack ou Teams sans toucher au reste du système.

---

## Conseils pour la soutenance

- **Maîtriser le vocabulaire** : ICMP, TCP, MTTD, MTTR, MERISE, UML, DevOps.
- **Faire une démonstration live** si possible (lancer un cycle, éteindre un
  équipement, montrer l'alerte Telegram arriver).
- **Rester honnête** sur les limites : un jury apprécie la lucidité.
- **Préparer une réponse courte ET une réponse longue** par question.
- **Ne pas réciter** : s'appuyer sur le support, regarder le jury.
