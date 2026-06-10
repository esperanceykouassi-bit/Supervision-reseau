<div align="center">

**RÉPUBLIQUE DE CÔTE D'IVOIRE**
*Union — Discipline — Travail*

**MINISTÈRE DE L'ENSEIGNEMENT SUPÉRIEUR ET DE LA RECHERCHE SCIENTIFIQUE**

**[NOM DE L'UNIVERSITÉ / GRANDE ÉCOLE]**

**DÉPARTEMENT RÉSEAUX ET INFORMATIQUE / TÉLÉCOMMUNICATIONS (RIT)**

---
---

*MÉMOIRE DE FIN DE CYCLE*
*En vue de l'obtention du diplôme de*
**MASTER 2 — RÉSEAUX ET INFORMATIQUE / TÉLÉCOMMUNICATIONS (RIT)**

---

# AUTOMATISATION DE LA SUPERVISION ET DE LA DÉTECTION DES PANNES RÉSEAU

### Conception et déploiement d'une solution open-source au sein de l'entreprise OPEN MOISE

---
---

**Présenté et soutenu publiquement par :**
**[NOM Prénom de l'étudiant]**

| | |
|---|---|
| **Directeur de mémoire :** | **Maître de stage (OPEN MOISE) :** |
| [Grade — NOM Prénom] | [NOM Prénom — Fonction] |

**Structure d'accueil : OPEN MOISE** *(Entreprise de Services du Numérique)*

---

**Année académique 2025 – 2026**

</div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# DÉDICACE

<div align="center">

*Je dédie ce travail :*

*À mes chers parents,*
*pour leur amour, leurs sacrifices et leur soutien indéfectible ;*

*À toute ma famille et à mes proches,*
*pour leurs encouragements constants ;*

*À mes enseignants du département RIT,*
*qui ont éclairé mon parcours ;*

*À l'ensemble du personnel d'OPEN MOISE,*
*pour son accueil et son partage d'expérience ;*

*À mes camarades de promotion.*

</div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# REMERCIEMENTS

La réalisation de ce mémoire n'aurait pas été possible sans le concours de
nombreuses personnes à qui je tiens à exprimer ma sincère reconnaissance.

Je remercie tout d'abord mon **directeur de mémoire, [Grade — NOM Prénom]**,
pour la qualité de son encadrement, sa disponibilité, ses orientations
méthodologiques et sa rigueur scientifique tout au long de ce travail.

Je remercie l'ensemble du **corps professoral du département RIT** pour la
formation solide dispensée durant ces années d'études.

Mes remerciements vont également à la **direction de l'entreprise OPEN MOISE**
pour m'avoir accueilli en stage, ainsi qu'à mon **maître de stage [NOM Prénom]**
et à toute l'équipe technique, pour leur disponibilité, leur partage
d'expérience et l'accès au terrain qui ont nourri ce travail.

J'adresse enfin ma gratitude aux **membres du jury** pour l'honneur qu'ils me
font d'évaluer ce mémoire, ainsi qu'à ma **famille** et à mes **amis** pour
leur soutien moral.

À toutes et à tous, **merci**.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# RÉSUMÉ

La disponibilité des infrastructures réseau est devenue un enjeu stratégique
pour les organisations et, plus encore, pour les **entreprises de services du
numérique (ESN)** qui en assurent l'exploitation pour le compte de leurs
clients. C'est le cas d'**OPEN MOISE**, structure d'accueil de ce projet, qui
supervise les réseaux de plusieurs clients sous engagements de niveau de
service (SLA). Or, cette supervision reposait largement sur des contrôles
**manuels et réactifs** : les pannes étaient souvent découvertes tardivement,
fréquemment signalées par le client lui-même, sans traçabilité exploitable.

Ce mémoire propose la **conception, la réalisation et le déploiement** d'un
système d'**automatisation de la supervision et de la détection des pannes
réseau**, fondé **exclusivement sur des outils open-source** : serveur Linux
Ubuntu, moteur de collecte en **Python** ordonnancé par **Cron**, base de
données **MySQL**, et **tableau de bord web** développé avec **Flask** et
**Bootstrap**. Le système réalise la **découverte automatique** des équipements,
la **surveillance** de leur disponibilité (sondes ICMP et TCP), la
**journalisation** des événements, et la **génération d'alertes en temps réel**
par **courrier électronique (SMTP)** et par **notification instantanée
Telegram**.

Les évaluations menées montrent que l'automatisation fait chuter le **temps
moyen de détection** d'environ une heure à moins de **deux minutes**, réduit le
**temps de réaction** des équipes et améliore le **taux de disponibilité** du
parc supervisé, le tout pour un **coût de licence nul**. Au-delà de l'outil
interne, la solution ouvre pour OPEN MOISE une **nouvelle offre de supervision
managée** à destination de ses clients, et prépare l'évolution vers une
supervision **prédictive** assistée par l'intelligence artificielle.

**Mots-clés :** supervision réseau, automatisation, détection de pannes,
open-source, Python, Flask, MySQL, Telegram, DevOps, SLA, OPEN MOISE.

# ABSTRACT

The availability of network infrastructures has become a strategic concern for
organizations and, even more, for **Managed Service Providers (MSP/ESN)** that
operate them on behalf of their clients. This is the case of **OPEN MOISE**,
the host company of this project, which monitors several client networks under
**Service Level Agreements (SLA)**. However, this monitoring relied largely on
**manual and reactive** checks: failures were often discovered late, frequently
reported by the client itself, with no usable traceability.

This thesis proposes the **design, implementation and deployment** of an
**automated network monitoring and fault-detection system**, based
**exclusively on open-source tools**: a Linux Ubuntu server, a collection
engine written in **Python** and scheduled by **Cron**, a **MySQL** database,
and a **web dashboard** built with **Flask** and **Bootstrap**. The system
performs **automatic device discovery**, availability **monitoring** (ICMP and
TCP probes), event **logging**, and **real-time alerting** through **e-mail
(SMTP)** and **instant Telegram notifications**.

The evaluations show that automation reduces the **mean time to detect** from
about one hour to less than **two minutes**, shortens the teams' **reaction
time**, and improves the **availability rate** of the monitored network, all at
**zero licensing cost**. Beyond the internal tool, the solution opens for OPEN
MOISE a **new managed-monitoring service offering** for its clients, and paves
the way toward **predictive** monitoring supported by artificial intelligence.

**Keywords:** network monitoring, automation, fault detection, open-source,
Python, Flask, MySQL, Telegram, DevOps, SLA, OPEN MOISE.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# LISTE DES ABRÉVIATIONS ET ACRONYMES

| Sigle | Signification |
|-------|---------------|
| **AIOps** | Artificial Intelligence for IT Operations |
| **API** | Application Programming Interface |
| **CIDR** | Classless Inter-Domain Routing |
| **CRUD** | Create, Read, Update, Delete |
| **DAL** | Data Access Layer (couche d'accès aux données) |
| **DevOps** | Development and Operations |
| **DNS** | Domain Name System |
| **ESN** | Entreprise de Services du Numérique |
| **FCFA** | Franc de la Communauté Financière Africaine (XOF) |
| **HTTP(S)** | HyperText Transfer Protocol (Secure) |
| **ICMP** | Internet Control Message Protocol |
| **IP** | Internet Protocol |
| **KPI** | Key Performance Indicator (indicateur clé de performance) |
| **LAN** | Local Area Network |
| **MCD / MLD / MPD** | Modèle Conceptuel / Logique / Physique de Données |
| **MTTD** | Mean Time To Detect (temps moyen de détection) |
| **MTTR** | Mean Time To Repair/Respond (temps moyen de réaction) |
| **MSP** | Managed Service Provider |
| **PME** | Petite et Moyenne Entreprise |
| **RTT** | Round Trip Time (temps d'aller-retour) |
| **SGBD** | Système de Gestion de Base de Données |
| **SLA** | Service Level Agreement (engagement de niveau de service) |
| **SMTP** | Simple Mail Transfer Protocol |
| **SNMP** | Simple Network Management Protocol |
| **SQL** | Structured Query Language |
| **SSH** | Secure Shell |
| **TCP** | Transmission Control Protocol |
| **UML** | Unified Modeling Language |
| **VLAN** | Virtual Local Area Network |
| **WSGI** | Web Server Gateway Interface |
| **XOF** | Code ISO du franc CFA (Afrique de l'Ouest) |

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# LISTE DES FIGURES

| N° | Figure |
|----|--------|
| Figure 1 | Architecture en cinq couches du système de supervision |
| Figure 2 | Diagramme de contexte |
| Figure 3 | Diagramme de cas d'utilisation |
| Figure 4 | Diagramme de séquence |
| Figure 5 | Diagramme d'activité |
| Figure 6 | Diagramme de classes |
| Figure 7 | Diagramme de composants |
| Figure 8 | Diagramme de déploiement |
| Figure 9 | Modèle Conceptuel de Données (MCD) |
| Figure 10 | Modèle Logique de Données (MLD) |
| Figure 11 | Page de connexion sécurisée |
| Figure 12 | Tableau de bord temps réel |
| Figure 13 | Notification Telegram reçue par l'astreinte |
| Figure 14 | Historique des alertes |
| Figure 15 | Gestion des équipements |
| Figure 16 | Rapports et statistiques |

# LISTE DES TABLEAUX

| N° | Tableau |
|----|---------|
| Tableau 1 | Hypothèses de recherche |
| Tableau 2 | Résultats attendus et indicateurs cibles |
| Tableau 3 | Outils techniques mobilisés |
| Tableau 4 | Comparatif des solutions de supervision |
| Tableau 5 | Facteurs de différenciation |
| Tableau 6 | Justification des choix technologiques |
| Tableau 7 | Sécurité « by design » |
| Tableau 8 | Tests de performance |
| Tableau 9 | Modèle économique |
| Tableau 10 | Investissement et revenus prévisionnels (FCFA) |

> *La table des matières détaillée est générée automatiquement ci-après.*

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
