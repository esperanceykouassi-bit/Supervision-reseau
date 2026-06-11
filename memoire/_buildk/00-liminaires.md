<div align="center">

**RÉPUBLIQUE DE CÔTE D'IVOIRE**
*Union — Discipline — Travail*

**MINISTÈRE DE L'ENSEIGNEMENT SUPÉRIEUR ET DE LA RECHERCHE SCIENTIFIQUE**

**[NOM DE L'UNIVERSITÉ / GRANDE ÉCOLE]**

**DÉPARTEMENT RÉSEAUX INFORMATIQUE ET TÉLÉCOMMUNICATION (RIT)**

---
---

*MÉMOIRE DE PROJET DE FIN D'ÉTUDES*
*En vue de l'obtention du diplôme de*
**MASTER 2 — RÉSEAUX INFORMATIQUE ET TÉLÉCOMMUNICATION (RIT)**

---

# AUTOMATISATION DE LA SUPERVISION ET DE LA DÉTECTION DES PANNES RÉSEAU

### Conception et déploiement d'une solution open-source

---
---

**Présenté et soutenu publiquement par :**
**KOUASSI Yoo Nyong Kra Espérance**

**Encadré par :**
**Dr Alain CAPO-CHICHI**
*Maître de Conférences des Universités du CAMES en Génie Informatique*

---

**Année académique 2025 – 2026**

</div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# DÉDICACE

<div align="center">

*À mon père, Kouassi Kouassi Alphonse,*
*dont la présence et l'amour ont guidé chacun de mes pas.*

*À ma mère, Mukandangamiye Félicité,*
*toi qui as espéré et cru, même quand tout semblait perdu.*

*À mes frères,*
*et tout particulièrement à mon frère Kouassi Christian,*
*pour votre affection indéfectible et votre foi en moi.*

*— Ce travail vous est humblement et affectueusement dédié —*

</div>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# REMERCIEMENTS

La réalisation de ce mémoire n'aurait pas été possible sans le concours de
nombreuses personnes à qui je tiens à exprimer ma sincère reconnaissance.

Je remercie tout d'abord mon encadreur, **Dr Alain CAPO-CHICHI**, Maître de
Conférences des Universités du CAMES en Génie Informatique, pour la qualité de
son encadrement, sa disponibilité, ses orientations méthodologiques et la
rigueur scientifique qu'il a su m'inculquer tout au long de ce travail.

Ma reconnaissance va également à **Monsieur Maxime LOKOSSOU**, assistant
directeur de mémoire, dont les contributions ont été déterminantes dans la
structuration de la démarche, ainsi qu'à **Monsieur MASSOLOKONON Tadagbe
Landry** pour son soutien constant et ses précieux conseils.

Une pensée fraternelle va à mes grands frères de cœur, **OUATTARA IVIDA Samuel**
et **ADOU JESUS KANGA Jonas BEUGRE**, ainsi qu'à ma sœur de cœur **Seungri
Adebayo**, pour leur soutien moral et leurs encouragements constants.

Je remercie sincèrement ma collègue **Nora YAPO**, qui m'a initiée et guidée
dans le domaine de la gestion de la clientèle, partageant avec générosité son
expérience et son expertise professionnelle.

Je remercie du fond du cœur ma **famille** — mon père, ma mère, mes sœurs et mon
frère — pour leur soutien moral indéfectible, leur patience et leurs
encouragements constants tout au long de ce parcours académique. Leur amour a
été ma plus grande force.

Un remerciement particulier va à toutes mes **camarades de promotion** avec
lesquelles j'ai partagé les joies et les difficultés de ces années d'études.

Enfin, je remercie toutes les personnes qui, de près ou de loin, ont contribué à
la réalisation de ce mémoire. Que chacun trouve ici l'expression de ma profonde
et sincère gratitude.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# RÉSUMÉ

La disponibilité des infrastructures réseau est devenue un enjeu stratégique
pour les organisations : entreprises, banques, opérateurs télécoms, hôpitaux et
administrations en dépendent en permanence. Pourtant, dans de nombreuses
structures — en particulier les petites et moyennes entreprises — la supervision
réseau demeure **manuelle et réactive** : on intervient une fois la panne
survenue, parfois signalée par l'utilisateur lui-même, sans traçabilité
exploitable.

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
parc supervisé, le tout pour un **coût de licence nul**. La solution, modulaire
et extensible, prépare l'évolution vers une supervision **prédictive** assistée
par l'intelligence artificielle.

**Mots-clés :** supervision réseau, automatisation, détection de pannes,
open-source, Python, Flask, MySQL, Telegram, DevOps, SLA.

# ABSTRACT

The availability of network infrastructures has become a strategic concern for
organizations: companies, banks, telecom operators, hospitals and public
administrations depend on it continuously. Yet, in many structures — especially
small and medium-sized enterprises — network supervision remains **manual and
reactive**: action is taken only after the failure occurs, sometimes reported by
the user, with no usable traceability.

This thesis proposes the **design, implementation and deployment** of an
**automated network monitoring and fault-detection system**, based
**exclusively on open-source tools**: a Linux Ubuntu server, a collection engine
written in **Python** and scheduled by **Cron**, a **MySQL** database, and a
**web dashboard** built with **Flask** and **Bootstrap**. The system performs
**automatic device discovery**, availability **monitoring** (ICMP and TCP
probes), event **logging**, and **real-time alerting** through **e-mail (SMTP)**
and **instant Telegram notifications**.

The evaluations show that automation reduces the **mean time to detect** from
about one hour to less than **two minutes**, shortens the teams' **reaction
time**, and improves the **availability rate** of the monitored network, all at
**zero licensing cost**. The modular and extensible solution paves the way
toward **predictive** monitoring supported by artificial intelligence.

**Keywords:** network monitoring, automation, fault detection, open-source,
Python, Flask, MySQL, Telegram, DevOps, SLA.

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
| **FCFA** | Franc de la Communauté Financière Africaine (XOF) |
| **HTTP(S)** | HyperText Transfer Protocol (Secure) |
| **ICMP** | Internet Control Message Protocol |
| **IP** | Internet Protocol |
| **KPI** | Key Performance Indicator (indicateur clé de performance) |
| **LAN** | Local Area Network |
| **MCD / MLD / MPD** | Modèle Conceptuel / Logique / Physique de Données |
| **MTTD** | Mean Time To Detect (temps moyen de détection) |
| **MTTR** | Mean Time To Repair/Respond (temps moyen de réaction) |
| **NOC** | Network Operations Center |
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
