# CHAPITRE 4 — ÉTAT DES LIEUX DES SOLUTIONS EXISTANTES ET SOLUTION PROPOSÉE

## 4.1 Cadre conceptuel et définitions

Avant de comparer les solutions, il convient de préciser les concepts mobilisés.

- **Réseau informatique** : ensemble d'équipements interconnectés échangeant des
  données via des protocoles normalisés, principalement la suite **TCP/IP**. La
  communication est structurée en couches (modèles OSI et TCP/IP).
- **Administration réseau** : ensemble des activités assurant le fonctionnement,
  la performance et la sécurité d'un réseau. Le modèle de référence **FCAPS**
  (ISO/UIT-T) la décompose en gestion des **pannes**, de la **configuration**,
  de la **comptabilité**, des **performances** et de la **sécurité**. La
  supervision relève surtout des volets *Fault* et *Performance*.
- **Supervision réseau** : processus continu de surveillance de l'état et de la
  performance des composants, visant à **détecter, diagnostiquer et signaler**
  les anomalies. Elle s'appuie sur des **sondes** interrogeant périodiquement
  les équipements et sur des **seuils** déclenchant des alertes.
- **Monitoring / observabilité** : collecte et visualisation continue de
  **métriques** (disponibilité, latence, charge), enrichie aujourd'hui par les
  **logs** et les **traces**.
- **Protocoles de sonde** : l'**ICMP** (commande `ping`) teste la joignabilité
  en couche 3 ; une **sonde TCP** teste l'ouverture d'un port applicatif
  (couche 4–7) ; le **SNMP** interroge des variables internes des équipements.
- **Automatisation** : délégation à des programmes des tâches répétitives, pour
  gagner en rapidité, en fiabilité et en cohérence.
- **Open-source** : logiciel dont le code est librement accessible, modifiable
  et redistribuable (licences GPL, MIT, Apache). Avantages : gratuité,
  transparence, communauté, absence de dépendance à un éditeur (*vendor
  lock-in*).
- **DevOps** : culture rapprochant développement et exploitation autour de
  l'automatisation, de l'intégration continue et de la **surveillance
  continue** — dont la supervision est un pilier.
- **SLA (Service Level Agreement)** : engagement contractuel de niveau de
  service (ex. taux de disponibilité garanti, délai d'intervention).

## 4.2 La supervision manuelle

La supervision manuelle consiste à vérifier l'état du réseau au moyen de
commandes ponctuelles (`ping`, `traceroute`, `nslookup`, connexions SSH).

**Avantages :** simplicité, aucun investissement logiciel, contrôle direct.

**Inconvénients :** caractère **réactif** (on découvre la panne après coup),
**chronophage**, **non tracé**, **non extensible**, dépendant de la
disponibilité humaine et sujet à l'erreur. C'est précisément le mode de
fonctionnement initial observé sur le terrain, à l'origine du présent projet.

## 4.3 La supervision automatisée

La supervision automatisée délègue la surveillance à un système logiciel
fonctionnant en continu. Elle apporte la **réactivité** (détection quasi temps
réel), la **traçabilité** (historisation), l'**alerte proactive** et la
**scalabilité**. Plusieurs solutions matures existent, présentées ci-après.

### 4.3.1 Nagios

Solution open-source historique, reposant sur un cœur (*Nagios Core*) et un
système de **plugins**. Très **éprouvée** et extensible, mais de
**configuration complexe** (fichiers texte), à l'interface vieillissante et à la
courbe d'apprentissage élevée. *Nagios Core* est gratuit ; *Nagios XI* est
payant.

### 4.3.2 Zabbix

Plateforme open-source **complète et moderne** : SNMP, agents, découverte
automatique, interface web riche, historique en base. En contrepartie, elle est
**gourmande en ressources** et exige une configuration initiale conséquente,
disproportionnée pour de petits besoins. Logiciel gratuit, support payant.

### 4.3.3 PRTG Network Monitor

Solution **propriétaire** (Paessler) réputée pour sa **simplicité**, fondée sur
des « capteurs ». Installation aisée et interface intuitive, mais **serveur
Windows uniquement** et **tarification au nombre de capteurs**. Gratuite
jusqu'à 100 capteurs, puis **licence payante**.

### 4.3.4 Centreon

Solution française bâtie historiquement sur le moteur de Nagios, à l'interface
**modernisée** et dotée de fonctions de reporting. Édition open-source gratuite ;
modules avancés et éditions entreprise **payants**.

### 4.3.5 SolarWinds NPM

Solution **propriétaire** haut de gamme pour grandes infrastructures : très
complète (cartographie, analyses avancées), mais **coûteuse** et lourde, et
éditée par un acteur ayant connu un incident de sécurité majeur (chaîne
d'approvisionnement, 2020). **Licence élevée** (plusieurs millions de FCFA).

## 4.4 Tableau comparatif des solutions

| Critère | Nagios | Zabbix | PRTG | Centreon | SolarWinds | **Solution proposée** |
|---------|:------:|:------:|:----:|:--------:|:----------:|:-----------------------:|
| Licence | Open-source | Open-source | Propriétaire | Mixte | Propriétaire | **Open-source** |
| Coût | Gratuit / payant | Gratuit | Payant | Gratuit / payant | Élevé | **Nul** |
| OS serveur | Linux | Linux | Windows | Linux | Windows | **Linux** |
| Simplicité de déploiement | Faible | Moyenne | Élevée | Moyenne | Faible | **Élevée** |
| Ressources requises | Faibles | Élevées | Moyennes | Moyennes | Élevées | **Très faibles** |
| Interface web | Basique | Riche | Riche | Riche | Riche | **Moderne (Bootstrap)** |
| Découverte auto. | Plugin | Oui | Oui | Oui | Oui | **Oui (Python)** |
| Alerte e-mail | Oui | Oui | Oui | Oui | Oui | **Oui** |
| Alerte mobile native | Plugin | Plugin | Appli | Plugin | Appli | **Oui (Telegram natif)** |
| Personnalisation du code | Limitée | Limitée | Non | Limitée | Non | **Totale** |
| Adapté aux PME / ESN | Moyen | Moyen | Oui | Moyen | Non | **Oui** |

## 4.5 Synthèse : le « vide » à combler

Les solutions existantes sont soit **puissantes mais complexes et gourmandes**
(Nagios, Zabbix, Centreon), soit **simples mais propriétaires et coûteuses**
(PRTG, SolarWinds). Pour les PME et les structures de taille moyenne — qui recherchent une
solution **légère, gratuite, simple, sur mesure** et dotée d'une **notification
mobile native** —, il subsiste un **espace** qu'aucune solution ne comble
pleinement. Ce constat justifie le développement d'une **solution propre**
plutôt que l'adoption d'un outil existant.

## 4.6 La solution proposée

Nous proposons un **système de supervision automatisé, modulaire et 100 %
open-source**, conçu pour les organisations, qui :

- **découvre automatiquement** les équipements d'un sous-réseau client (scan
  CIDR parallélisé) ;
- **sonde en continu** la disponibilité (ICMP) et les services (TCP : HTTP, SSH,
  MySQL…) ;
- **confirme** la panne par un seuil d'échecs (anti-faux positif) et
  **journalise** chaque vérification (preuve de SLA) ;
- **alerte en temps réel** l'astreinte par **e-mail** et **Telegram**, avec
  logique **anti-spam** ;
- expose un **tableau de bord web** temps réel, la **gestion des équipements**,
  l'**historique des alertes** et des **rapports** exportables.

La pile technologique retenue est : **Ubuntu · Python · Cron · MySQL · Flask ·
Bootstrap · Bot Telegram**. Les justifications détaillées de ces choix et la
conception du système font l'objet du chapitre 6.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
