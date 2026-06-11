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


# AUTOBIOGRAPHIE


#### Introduction

La rédaction d'une autobiographie, dans le cadre d'un mémoire de fin de cycle, représente bien plus qu'un simple exercice académique. Elle constitue une démarche réflexive et introspective, qui invite à revisiter l'ensemble des étapes d'une vie, à en mesurer les apports, les défis et les transformations. C'est dans cet esprit que je me prête à cet exercice, avec sincérité et engagement.

Je me nomme Kouassi Yoo Nyong Kra Espérance. J'ai 24 ans. Née et élevée à Yopougon, dans le quartier Camp Militaire, à Abidjan, en Côte d'Ivoire, j'ai grandi dans un environnement familial et communautaire qui m'a profondément façonnée. Titulaire d'un Baccalauréat série D et d'une Licence en Informatique, je poursuis aujourd'hui un Master 2 en Réseaux et Informatique/Télécommunications (RIT) à CERCO.

Mon parcours est marqué par la résilience, la persévérance et une ambition claire : me hisser au rang des professionnels compétents dans le domaine des technologies de l'information et de la communication, contribuer activement au développement du secteur numérique ivoirien, et incarner les valeurs de travail et d'excellence que m'ont inculquées ma famille et mes expériences de vie.

La présente autobiographie retrace les grandes étapes de ce parcours : mes origines familiales et sociales, mon cursus scolaire et universitaire, mes expériences professionnelles et associatives, mes compétences, mon projet de carrière ainsi que les motivations profondes qui sous-tendent le thème de mon mémoire. Chaque section constitue un fragment d'une histoire en construction, celle d'une femme déterminée à réussir malgré les obstacles, et à contribuer, à sa mesure, à l'édification d'une Côte d'Ivoire numérique.


#### I. Origines et cadre familial

Toute destinée humaine prend racine dans son histoire familiale. La mienne ne déroge pas à cette règle. Je suis la fille unique de ma mère, et cette singularité revêt une signification particulièrement forte dans mon histoire personnelle.

Ma mère, après plusieurs grossesses douloureusement interrompues par des fausses couches successives, s'était vue annoncer par des médecins qu'elle ne pourrait plus donner la vie. Cette sentence médicale, lourde à porter pour toute femme, ne l'a pourtant pas brisée. Elle a continué d'espérer, de prier, de croire. Et c'est dans ce contexte empreint de douleur mais aussi d'une foi inébranlable, que je suis née. C'est précisément pour cette raison que l'on m'a prénommée Espérance : je suis, pour ma famille et particulièrement pour ma mère, le symbole vivant que l'espoir ne meurt jamais, et que la persévérance finit toujours par porter ses fruits.

Je suis également le septième enfant de mon père, ce qui fait de moi un membre d'une famille recomposée. Grandir dans cette configuration familiale m'a permis de développer très tôt une aptitude à l'adaptation, à la coexistence avec des personnalités diverses et à la gestion des relations humaines complexes. La cellule familiale élargie, avec ses frères et sœurs issus de différentes unions, m'a offert un espace d'apprentissage informel riche en enseignements sur la solidarité, le respect mutuel et la gestion des conflits.

C'est dans le quartier Camp Militaire de Yopougon que j'ai grandi. Yopougon, commune populaire et vibrante d'Abidjan, est connue pour son effervescence culturelle, son dynamisme social et la diversité de sa population. Grandir dans ce quartier, c'est apprendre à naviguer entre des réalités sociales contrastées, à faire preuve de débrouillardise et à cultiver un esprit de solidarité communautaire. Ces valeurs, ancrées dès mon enfance, ont fortement influencé ma vision du monde et ma façon d'aborder les défis de la vie.

Mon cadre familial, bien que modeste sur le plan matériel, m'a offert des richesses inestimables : l'amour inconditionnel de mes parents, l'enseignement de la résilience face aux épreuves, le sens des responsabilités et la conviction que l'éducation est la clé du progrès individuel et collectif. Ces fondements ont guidé chacune de mes décisions et continuent d'orienter mon parcours académique et professionnel.


#### II. Parcours scolaire

**1. L'enseignement primaire et les premières années de collège**

Mes premières années scolaires ont posé les bases d'un rapport au savoir que je qualifierais de curieux et engagé. Dès le primaire, j'ai manifesté un intérêt particulier pour les matières scientifiques, notamment les mathématiques et les sciences naturelles, qui stimulaient mon goût pour la logique et l'analyse.

C'est au collège Phalène 1 que j'ai effectué l'essentiel de mon enseignement secondaire du premier cycle, de la classe de sixième jusqu'en troisième. Ces années au collège ont été pour moi une période de construction intellectuelle et personnelle intense. J'ai appris à m'organiser, à travailler de manière régulière et à m'investir dans les activités parascolaires qui permettent de développer des compétences complémentaires à celles acquises en classe.

À l'issue de ce premier cycle d'enseignement secondaire, j'ai obtenu le Brevet d'Études du Premier Cycle (BEPC), consacrant ainsi une première étape importante dans mon parcours académique.

**2. Le lycée et l'obtention du Baccalauréat**

Après le BEPC, j'ai intégré le lycée des jeunes de Yopougon pour la poursuite de mes études secondaires. C'est là que j'ai opéré un choix déterminant : celui de la série D, filière scientifique orientée vers les sciences de la vie et de la terre, combinées aux mathématiques et à la physique-chimie.

Ce choix ne s'est pas fait au hasard. Il reflétait ma conviction profonde que les sciences constituent un socle indispensable pour appréhender le monde dans sa complexité et pour contribuer à son évolution. La série D m'a permis de développer un esprit d'analyse et de synthèse, une rigueur méthodologique et une capacité à résoudre des problèmes complexes, autant de qualités qui se sont révélées précieuses dans la suite de mon parcours en informatique et en réseaux.

Les années lycée n'ont pas été sans difficultés. Comme tout élève, j'ai traversé des périodes de doute, des moments où la pression des examens et les exigences du programme semblaient insurmontables. Mais à chaque fois, c'est ma détermination et le soutien de ma famille qui m'ont permis de surmonter ces obstacles. J'ai également trouvé dans mes professeurs des modèles d'engagement et de rigueur intellectuelle qui ont renforcé ma passion pour les sciences.

En 2020, au terme de ces années de travail acharné, j'ai obtenu mon Baccalauréat série D. Cette réussite a été vécue comme une véritable victoire, non seulement personnelle, mais aussi familiale. Elle ouvrait la voie à l'enseignement supérieur et à la réalisation de mon projet de vie.


#### III. Parcours universitaire

**1. La formation en Licence à l'UNISAT**

Fort de mon baccalauréat en poche, j'ai été orientée à l'UNISAT (Université des Sciences Appliquées et de Technologies), où j'ai entamé une formation en informatique. Ce choix de filière a été la concrétisation d'une inclination naturelle pour les technologies numériques, perceptible dès mes années de lycée.

La formation en Licence à l'UNISAT m'a offert un socle théorique et pratique solide dans plusieurs domaines fondamentaux de l'informatique. J'y ai acquis des compétences en réseaux informatiques, notamment la conception, la configuration et l'administration de réseaux locaux et étendus. J'ai également été formée aux systèmes d'exploitation, avec une maîtrise progressive des environnements Linux et Windows, essentiels dans le monde professionnel de l'informatique.

La programmation a constitué un autre pilier de ma formation. J'ai appris les bases des langages de programmation et développé une logique algorithmique qui me permet d'aborder les problèmes informatiques avec méthode. Enfin, les bases de données ont été au cœur d'une partie importante de ma formation, avec l'apprentissage de la conception de systèmes de gestion de bases de données relationnelles et l'utilisation du langage SQL.

Ces trois années de Licence ont également été l'occasion de réaliser des projets en groupe, expériences qui m'ont appris à collaborer, à partager les responsabilités et à mener un projet à son terme dans le respect des délais et des contraintes fixées. Ces compétences transversales sont aujourd'hui au cœur de mon approche professionnelle.

En 2023, j'ai obtenu ma Licence en Informatique, couronnant trois années d'efforts et d'apprentissage. Cette réussite a confirmé ma vocation pour l'informatique et les télécommunications, et renforcé ma motivation à poursuivre vers des études de Master.

**2. L'interruption et la reprise des études**

Le chemin vers la réussite est rarement linéaire. Le mien ne fait pas exception. Après l'obtention de ma Licence, j'ai été contrainte d'interrompre mes études pendant une année entière, en raison de difficultés financières que ma famille n'était pas en mesure de surmonter immédiatement.

Cette période d'interruption aurait pu être vécue comme un échec ou une capitulation. Mais j'ai choisi de la transformer en opportunité de croissance personnelle. Loin de rester passive, j'ai mis à profit ce temps pour apporter mon aide à mes parents dans diverses activités génératrices de revenus, contribuant ainsi à rassembler progressivement les ressources nécessaires pour financer la suite de mes études.

Cette expérience m'a confrontée à la réalité économique du quotidien, aux contraintes financières que doivent affronter de nombreux étudiants ivoiriens et à la nécessité de faire preuve d'ingéniosité et de persévérance face à l'adversité. Elle a renforcé mon sens des responsabilités et ma conviction que les obstacles ne sont que des étapes vers la réussite.

En 2024, avec une détermination renouvelée, je me suis inscrite à CERCO pour entamer un Master 2 en Réseaux et Informatique/Télécommunications. Cette reprise a été marquée par un engagement encore plus fort, une maturité accrue et une vision plus claire de mon projet professionnel.


#### IV. Expérience pratique en administration réseau

L'une des expériences les plus formatrices de mon parcours a sans conteste été ma participation à une mission d'administration réseau au sein de l'Institut Universitaire de Grand-Bassam (IUGB). Cette expérience pratique sur le terrain m'a permis de confronter les connaissances théoriques acquises en cours à la complexité et à l'imprévisibilité des environnements réseau réels.

**1. Le contexte et l'infrastructure**

L'IUGB dispose d'une infrastructure réseau de campus de grande envergure, conçue pour répondre aux besoins d'une institution universitaire moderne. Cette infrastructure comprenait notamment un routeur Huawei AR6140, pièce maîtresse de l'architecture réseau, assurant le routage inter-VLAN et la connexion à Internet. Des commutateurs CloudEngine et S5735, également de la marque Huawei, assuraient la commutation au niveau des accès et de la distribution. Un contrôleur Omada centralisait la gestion des points d'accès sans fil, au nombre de 86 unités de la marque TP-Link, répartis sur l'ensemble des bâtiments du campus et organisés en plusieurs VLANs distincts.

Cette architecture, bien que robuste dans sa conception, présentait un certain nombre de dysfonctionnements et de points de fragilité qui nécessitaient une intervention méthodique et rigoureuse.

**2. Les problématiques rencontrées**

Au cours de cette mission, j'ai été confrontée à des problématiques techniques réelles et variées, qui m'ont permis de développer une approche diagnostic approfondie :

La saturation de la bande passante, phénomène courant dans les environnements universitaires à forte densité d'utilisateurs, qui entraînait des ralentissements importants et une dégradation significative de la qualité de service.

Des erreurs de routage par défaut, qui provoquaient des pertes de connectivité intermittentes et des anomalies dans le transit des paquets entre les différents segments réseau.

Des conflits ARP (Address Resolution Protocol), source de perturbations dans la communication entre les équipements du réseau local, pouvant aller jusqu'à des interruptions de service.

Un portail captif défaillant, élément critique de la gestion des accès au réseau sans fil, dont les dysfonctionnements empêchaient les utilisateurs de s'authentifier et d'accéder aux ressources réseau.

**3. Ma contribution et les apprentissages**

Face à ces défis, j'ai contribué activement au diagnostic et à la résolution des incidents. Ma démarche a été fondée sur une approche méthodique : identification précise des symptômes, analyse des journaux système, tests de connectivité, et recherche de solutions documentées, avant la mise en œuvre des corrections retenues.

Cette expérience m'a appris que l'administration réseau ne se limite pas à la configuration initiale des équipements, mais implique une surveillance constante, une capacité à anticiper les problèmes et une réactivité face aux incidents. Elle m'a également démontré l'importance d'une documentation rigoureuse et d'une communication efficace au sein des équipes techniques.

Sur le plan humain, cette mission m'a confortée dans ma vocation pour les métiers des réseaux et m'a donné une première expérience concrète du terrain, indispensable pour tout professionnel de l'informatique souhaitant avoir un impact réel sur les organisations.


#### V. Expérience en gestion de la clientèle

En parallèle de mon parcours académique et technique, j'ai eu l'opportunité d'acquérir une expérience professionnelle dans le domaine de la gestion de la clientèle, au sein de l'entreprise OPEN. Cette expérience, bien que différente dans sa nature de mes activités liées aux réseaux informatiques, s'est révélée d'une richesse considérable pour mon développement personnel et professionnel.

Travailler au contact direct des clients m'a permis de développer et d'affiner plusieurs compétences essentielles dans le monde professionnel d'aujourd'hui. La communication, d'abord : savoir écouter activement, reformuler les attentes du client, expliquer clairement des concepts parfois techniques et adapter son discours en fonction de son interlocuteur sont des aptitudes que j'ai considérablement renforcées au cours de cette expérience.

L'écoute active a été particulièrement mise en avant dans ce rôle. Comprendre les besoins réels d'un client, souvent exprimés de manière imprécise ou partielle, et être capable d'y apporter une réponse adaptée et satisfaisante, constitue un véritable art qui s'apprend par la pratique et la répétition.

La gestion des relations professionnelles, dans ses dimensions à la fois relationnelles et organisationnelles, a également été au cœur de mon quotidien dans ce poste. Gérer des clients aux profils variés, parfois exigeants ou insatisfaits, en maintenant en toutes circonstances un niveau élevé de professionnalisme et de courtoisie, m'a dotée d'une solide maîtrise de moi-même et d'une grande capacité à gérer les situations de tension.

Sur un plan plus profond, cette expérience m'a permis de mieux comprendre l'importance de l'utilisateur final dans la conception et la gestion des systèmes informatiques. Trop souvent, les professionnels des technologies de l'information ont tendance à raisonner en termes de performance technique, en oubliant que le véritable objectif de tout système informatique est de répondre aux besoins concrets des utilisateurs. Mon expérience en gestion de la clientèle m'a définitivement ancrée dans cette conviction : la dimension humaine doit être au centre de toute démarche technologique.


#### VI. Engagement associatif et bénévolat

Au-delà de mes activités académiques et professionnelles, je me suis engagée dans plusieurs organisations bénévoles, convaincue que la responsabilité sociale est indissociable d'un parcours de vie accompli. Cet engagement associatif constitue une dimension importante de mon identité et de mes valeurs.

Au sein de ces organisations, j'ai eu l'opportunité de piloter et de participer à différents projets à vocation sociale, culturelle ou éducative. Ces expériences m'ont placée dans des situations qui développent des compétences rarement enseignées dans le cadre académique traditionnel.

Le leadership, d'abord. Piloter un projet bénévole, c'est apprendre à mobiliser des équipes sans avoir recours à l'autorité hiérarchique, à fédérer autour d'une vision commune, à motiver et à inspirer des personnes aux profils et aux motivations diverses. Cette forme de leadership dit « partagé » est aujourd'hui considérée comme l'une des plus efficaces dans les organisations modernes, et je l'ai pratiquée et éprouvée sur le terrain.

Le travail en équipe a également été une dimension centrale de mon engagement associatif. Collaborer avec des bénévoles issus d'horizons différents, gérer les divergences d'opinion et construire des consensus, sont des aptitudes que j'ai fortement développées au fil de mes expériences associatives.

La gestion de projets, dans sa dimension opérationnelle — planification, organisation des ressources, suivi des activités, évaluation des résultats — a également fait partie de mes responsabilités dans le cadre associatif. Ces compétences se révèlent aujourd'hui directement transférables dans le monde professionnel, notamment dans la gestion de projets informatiques.

Enfin, cet engagement bénévole reflète une conviction fondamentale : la réussite individuelle n'a de véritable sens que si elle contribue au bien-être collectif. Il est de la responsabilité de chacun, à son niveau et avec ses moyens, de contribuer positivement à la société. C'est dans cet esprit que j'envisage également mon futur rôle professionnel, comme une contribution au développement numérique de la Côte d'Ivoire.


#### VII. Compétences acquises

**1. Compétences techniques**

Mon parcours académique et professionnel m'a permis de constituer un portefeuille de compétences techniques solide, en constante évolution :

Administration réseau : configuration et gestion d'équipements réseau (routeurs Huawei, commutateurs CloudEngine/S5735, points d'accès TP-Link), maîtrise des protocoles TCP/IP, VLAN, routage inter-VLAN, et notions de gestion du trafic réseau.

Systèmes d'exploitation Linux : administration de serveurs sous Linux, gestion des utilisateurs et des permissions, utilisation de la ligne de commande, notions de scripting Bash.

Supervision réseau : initiation aux outils de surveillance et de monitoring des infrastructures réseau, compréhension des enjeux de la gestion proactive des incidents.

Bases de données : conception et manipulation de bases de données relationnelles, maîtrise du langage SQL.

Programmation : notions en langages de programmation, développement d'une logique algorithmique appliquée à la résolution de problèmes informatiques.

**2. Compétences transversales**

En parallèle de ces compétences techniques, j'ai développé un ensemble de soft skills essentiels à l'exercice des métiers de l'informatique dans un environnement professionnel exigeant :

Organisation et gestion du temps : capacité à gérer simultanément plusieurs projets, à établir des priorités et à respecter les délais.

Leadership et management d'équipe : aptitude à mobiliser et à coordonner des équipes pluridisciplinaires, développée dans le cadre de mes engagements associatifs.

Communication professionnelle : aisance à communiquer aussi bien avec des profils techniques qu'avec des interlocuteurs non techniques, compétence renforcée par mon expérience en gestion de la clientèle.

Résilience et adaptabilité : capacité éprouvée à faire face aux situations difficiles et à rebondir positivement, forgée par les épreuves personnelles traversées.

Sens des responsabilités : engagement constant à assumer pleinement ses missions et à en rendre compte avec honnêteté et transparence.


#### VIII. Choix du thème de mémoire

Le choix du thème de mon mémoire de fin de cycle n'est pas le fruit du hasard. Il s'inscrit dans la continuité naturelle de mon parcours académique, de mes expériences pratiques et de ma réflexion sur les enjeux actuels du secteur des technologies de l'information.

Mon thème porte sur l'automatisation de la supervision réseau. Ce sujet m'a été inspiré directement par mon expérience à l'IUGB, où j'ai pu mesurer de manière concrète les limites d'une gestion réseau réactive, fondée sur le traitement des incidents après leur survenue. Face à des infrastructures de plus en plus complexes, comprenant des dizaines d'équipements hétérogènes et des centaines d'utilisateurs simultanés, les approches traditionnelles de supervision montrent rapidement leurs limites.

L'automatisation de la supervision réseau répond à un besoin réel et croissant des organisations : détecter les anomalies de manière proactive, avant qu'elles ne se transforment en incidents majeurs ; réduire les temps de réponse face aux dysfonctionnements ; optimiser l'utilisation des ressources réseau ; et libérer les équipes techniques des tâches répétitives à faible valeur ajoutée, pour les concentrer sur des activités à plus fort impact stratégique.

Ce thème est également en phase avec les grandes tendances technologiques actuelles, notamment l'adoption croissante des pratiques DevOps et AIOps dans la gestion des infrastructures informatiques, l'essor des outils open-source de monitoring comme Zabbix, Nagios ou Prometheus, et l'intégration progressive de l'intelligence artificielle dans les processus de gestion des réseaux.

En choisissant ce thème, j'ambitionne de produire un travail qui soit non seulement académiquement rigoureux, mais aussi pratiquement utile pour les organisations ivoiriennes et africaines désireuses de moderniser leurs pratiques de gestion réseau.


#### IX. Projet professionnel

À l'issue de ma formation en Master 2, mon projet professionnel est clairement défini, articulé autour de deux axes principaux : l'expertise technique dans les domaines des réseaux et de la cybersécurité, et la contribution au développement du secteur numérique en Côte d'Ivoire.

Sur le plan technique, je souhaite exercer en tant qu'ingénieure en administration réseau et cybersécurité. Les infrastructures réseaux constituent l'épine dorsale de toute organisation moderne, et leur sécurisation est devenue un enjeu stratégique majeur à l'heure où les cybermenaces se multiplient et se sophistiquent. Je veux être au cœur de cette dynamique, contribuer à la conception d'architectures réseau robustes et sécurisées, et participer activement à la protection des systèmes d'information des organisations.

À plus court terme, mon objectif est de rejoindre une organisation — entreprise privée, institution publique ou opérateur de télécommunications — où je pourrai mettre en pratique les compétences acquises au cours de ma formation et les approfondir au contact de professionnels expérimentés. Je souhaite évoluer dans un environnement stimulant, qui valorise l'initiative, la créativité et la formation continue.

À moyen terme, j'envisage de me spécialiser davantage dans le domaine de la cybersécurité, en passant des certifications reconnues internationalement — telles que le CCNA (Cisco Certified Network Associate), le CompTIA Security+ ou le Certified Ethical Hacker (CEH) — qui viendront renforcer mon employabilité et ma crédibilité professionnelle.

À long terme, mon ambition est de contribuer activement au développement du secteur numérique en Côte d'Ivoire. Ce pays, engagé dans une dynamique de transformation digitale ambitieuse, a besoin de professionnels compétents et engagés pour accompagner cette transition. Je veux être l'une de ces professionnelles, et pourquoi pas, à terme, créer ma propre structure spécialisée dans la sécurité des systèmes d'information et le conseil en infrastructure réseau.


#### X. Centres d'intérêt et personnalité

La personne que l'on est ne saurait se réduire à son seul parcours académique et professionnel. C'est pourquoi cette autobiographie serait incomplète sans un regard sur mes centres d'intérêt et les traits de personnalité qui me définissent.

Je suis avant tout une femme curieuse, animée par un désir permanent de comprendre, d'explorer et de découvrir. Cette curiosité, qui a nourri mon attrait pour les sciences et la technologie, se manifeste également dans ma passion pour les voyages.

Voyager, pour moi, c'est bien plus que déplacer son corps d'un lieu à un autre. C'est une démarche d'ouverture au monde, une invitation à dépasser ses certitudes et ses habitudes, à s'enrichir au contact d'autres cultures, d'autres modes de vie, d'autres façons de penser. Chaque voyage est une leçon d'humilité et d'émerveillement. Chaque rencontre avec d'autres peuples et d'autres traditions nourrit ma compréhension de la diversité humaine et renforce mon sens de l'empathie.

Cette passion pour les voyages est profondément liée à mon rapport au monde professionnel. Les professionnels qui ont une expérience internationale, qui ont été confrontés à des contextes culturels différents, sont généralement plus créatifs, plus adaptables et plus capables de travailler en équipes multiculturelles. Je nourris l'ambition de développer cette dimension internationale tout au long de ma carrière.

Sur le plan de la personnalité, je me définirais comme quelqu'un de déterminé, persévérant et empathique. Ma détermination s'est forgée dans les épreuves traversées — les difficultés financières, l'interruption des études — et s'exprime aujourd'hui dans mon engagement sans faille dans mes projets académiques et professionnels. Ma persévérance est le moteur qui m'a permis de ne jamais abandonner, même dans les moments les plus difficiles. Mon empathie, enfin, est ce qui me permet de comprendre les besoins des autres, qu'il s'agisse de clients, de collaborateurs ou d'utilisateurs, et de proposer des solutions adaptées à leurs réalités.


#### Conclusion

Au terme de cette autobiographie, je mesure le chemin parcouru depuis mes premières années scolaires à Yopougon jusqu'à la rédaction de ce mémoire de Master 2. Un chemin marqué par des étapes significatives, des défis parfois intenses, mais aussi par des réussites qui ont jalonné et enrichi mon parcours.

Chaque expérience — qu'il s'agisse des années de lycée qui ont forgé ma rigueur intellectuelle, de la formation en Licence qui a posé les fondements de mes compétences techniques, de l'interruption difficile qui a renforcé ma résilience, de la mission à l'IUGB qui m'a confrontée à la réalité du terrain, ou encore de mon engagement associatif qui a développé mon sens des responsabilités — a contribué à construire la professionnelle et la personne que je suis aujourd'hui.

Je suis convaincue que la réussite dans le domaine des technologies de l'information ne repose pas seulement sur des compétences techniques. Elle requiert également des qualités humaines — la curiosité intellectuelle, la persévérance, l'empathie, le sens de l'éthique — qui permettent de mettre la technologie au service du bien commun.

C'est dans cet esprit que j'aborde la rédaction de mon mémoire sur l'automatisation de la supervision réseau, et plus largement, la construction de mon projet professionnel. Il ne s'agit pas simplement d'acquérir des diplômes ou des certifications, mais de devenir une professionnelle compétente, engagée et responsable, capable de contribuer activement au développement numérique de la Côte d'Ivoire et de l'Afrique.

L'histoire que j'ai commencé à écrire est encore loin d'être terminée. Les pages qui s'ouvrent devant moi sont pleines de promesses et de défis à relever. Et je les aborde avec la même détermination, la même curiosité et la même foi en l'avenir qui ont toujours guidé mes pas. Car c'est bien là le sens profond de mon prénom : Espérance.

Kouassi Yoo Nyong Kra Espérance

Abidjan, 2025

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# INTRODUCTION GÉNÉRALE

À l'ère de la transformation numérique, le réseau informatique constitue le
**système nerveux** de toute organisation. La messagerie, la téléphonie sur IP,
les applications métier, l'accès à Internet, les services bancaires en ligne ou
encore les systèmes de **paiement mobile** — omniprésents en Côte d'Ivoire et
dans la sous-région — reposent intégralement sur la disponibilité et la fiabilité
de l'infrastructure réseau. Une interruption de service, même brève, se traduit
par une perte de productivité, un manque à gagner, une dégradation de l'image
et, dans les secteurs critiques, par des conséquences plus lourdes encore.

Cette exigence de **continuité de service** est d'autant plus forte que les
infrastructures se densifient : multiplication des équipements (routeurs,
commutateurs, pare-feu, serveurs), virtualisation, cloud, mobilité et objets
connectés. Les organisations visent désormais des objectifs de disponibilité de
l'ordre de **99,9 %**, soit moins de neuf heures d'indisponibilité cumulée par
an. Atteindre et **prouver** de tels niveaux suppose une surveillance
**continue, outillée et tracée** — ce que la supervision manuelle ne permet pas.

Or, le constat dressé dans de nombreuses structures — en particulier les
**petites et moyennes entreprises (PME)** — est celui d'une supervision encore
**manuelle et réactive** : des contrôles ponctuels (commandes `ping`, connexions
aux équipements), une détection des incidents reposant le plus souvent sur le
**signalement des utilisateurs**, et une **absence de traçabilité** exploitable.
Ce mode de fonctionnement allonge mécaniquement le **temps de détection** et le
**temps d'intervention**, fragilise le respect des engagements de service et
mobilise inutilement les ressources humaines.

Des solutions de supervision existent pourtant — propriétaires (PRTG,
SolarWinds) ou open-source (Nagios, Zabbix, Centreon). Mais les premières sont
**coûteuses** et les secondes, bien que puissantes, sont souvent jugées
**lourdes et complexes** à déployer et à maintenir pour une structure aux moyens
mesurés. Il existe donc un **espace** pour une solution **légère, économique,
sur mesure et entièrement maîtrisée**, bâtie à partir de briques open-source.

C'est l'objet de ce mémoire-projet : **concevoir, réaliser et déployer un
système d'automatisation de la supervision et de la détection des pannes
réseau**, fondé exclusivement sur des outils open-source, et **le penser comme un
véritable produit** — depuis le besoin du terrain jusqu'au modèle économique.
Conformément au plan d'un mémoire-projet, le document s'organise ainsi : après
l'identification du **problème** (chap. 1), nous précisons les **objectifs**
(chap. 2) et la **démarche méthodologique** (chap. 3), puis nous réalisons
l'**état des lieux** des solutions et présentons la **solution proposée** (chap.
4) et son **axe de différenciation** (chap. 5). Suivent l'**étude de faisabilité
et la conception** (chap. 6), le **fonctionnement technique** (chap. 7) et la
**démonstration** illustrée par les écrans de l'application (chap. 8). Enfin,
nous abordons le volet **marketing et concurrence** (chap. 9), les **prévisions
financières** en francs CFA (chap. 10), puis les **limites et perspectives**
(chap. 11), avant de conclure.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CHAPITRE 1 — CONTEXTE ET IDENTIFICATION DU PROBLÈME

## 1.1 Contexte général

La dernière décennie a vu une **densification** sans précédent des
infrastructures réseau : multiplication des équipements actifs, virtualisation
des serveurs, adoption du cloud, mobilité des utilisateurs et explosion des
objets connectés. En Côte d'Ivoire, la généralisation de la fibre optique, la
croissance du commerce électronique et la prééminence du **paiement mobile**
ont fait du réseau une ressource **critique** pour l'activité économique.

Cette dépendance accrue au numérique élève le **coût de l'indisponibilité** :
une interruption réseau peut bloquer des transactions, des encaissements et des
services entiers. Pour les organisations comme pour les prestataires
informatiques, la **qualité et la continuité de service** deviennent ainsi des
facteurs déterminants de différenciation, dans un marché où la maîtrise des
**coûts** reste néanmoins primordiale. Ce double impératif — fiabilité *et*
économie — oriente directement les choix de ce projet vers l'**open-source**.

## 1.2 La supervision réseau aujourd'hui

La supervision consiste à surveiller en continu l'état et la performance des
composants d'un réseau afin de **détecter, diagnostiquer et signaler** les
anomalies. Dans la pratique, on observe deux grandes approches :

- une supervision **manuelle**, fondée sur des commandes ponctuelles et la
  vigilance humaine, encore très répandue dans les petites structures ;
- une supervision **automatisée**, assurée par un système logiciel fonctionnant
  en permanence, qui apporte réactivité, traçabilité et alerte proactive.

L'observation du terrain montre que de nombreuses structures en sont encore à la
première approche : la surveillance des parcs s'effectue essentiellement **à la
demande**, lorsqu'un dysfonctionnement est suspecté ou signalé. Aucun dispositif
n'assure une **veille permanente et automatique** de l'ensemble des équipements.

## 1.3 Constat et formulation du problème

De cette situation découlent plusieurs **dysfonctionnements** :

1. **Détection tardive** : la panne est le plus souvent révélée par
   l'**utilisateur final lui-même**, c'est-à-dire *après* que le service a été
   dégradé. Le temps moyen de détection (MTTD) se compte en **dizaines de
   minutes**, voire en heures.
2. **Réaction différée** : les équipes techniques n'étant pas alertées
   automatiquement, le **temps moyen de réaction** (MTTR) s'allonge d'autant.
3. **Absence de traçabilité** : faute d'historisation, il est difficile de
   **prouver le respect des engagements de service**, d'analyser les pannes
   récurrentes ou de produire des rapports.
4. **Charge humaine et risque d'erreur** : la surveillance manuelle est
   **chronophage**, non extensible au-delà de quelques équipements, et sujette à
   la fatigue.
5. **Risque pour l'activité** : la détection tardive met en péril la continuité
   de service et, à terme, la **relation de confiance** avec les utilisateurs.

Le problème central se formule ainsi : **l'absence d'un dispositif automatisé,
accessible et économique de supervision empêche la détection précoce des pannes
réseau et allonge le temps d'intervention des équipes, au détriment de la qualité
de service et de la maîtrise des coûts.**

## 1.4 Questions de recherche

### Question principale

> **Comment automatiser la supervision d'une infrastructure réseau afin de
> détecter — voire d'anticiper — les pannes en temps réel, tout en réduisant
> significativement le temps moyen d'intervention et la charge des équipes
> techniques, à l'aide d'une solution fiable et économiquement accessible fondée
> sur des outils open-source ?**

### Questions secondaires

1. Quels concepts et technologies fondent la supervision et l'automatisation
   réseau, et quelles solutions existent déjà sur le marché ?
2. Quelle architecture logicielle et matérielle, à base d'outils open-source,
   répond aux besoins identifiés ?
3. Comment notifier les équipes de manière instantanée et fiable, où qu'elles se
   trouvent ?
4. Dans quelle mesure l'automatisation améliore-t-elle concrètement le temps de
   détection, le temps de réaction et le taux de disponibilité, et à quel coût ?

## 1.5 Justification et intérêt du sujet

L'intérêt de ce sujet est triple. Sur le plan **professionnel**, il répond à un
besoin réel et récurrent de l'administration des réseaux et améliore la
compétitivité des structures qui l'adoptent. Sur le plan **économique**, il
démontre qu'une solution efficace peut être bâtie sans licence coûteuse —
argument décisif dans le contexte ivoirien. Sur le plan **scientifique et
pédagogique**, il mobilise l'ensemble des compétences du Master Réseaux
Informatique et Télécommunication (réseaux, programmation, bases de données,
systèmes Linux, cybersécurité, DevOps) et s'inscrit dans les pratiques
d'**ingénierie contemporaines** (automatisation, observabilité, AIOps).

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# CHAPITRE 2 — OBJECTIFS ET RÉSULTATS ATTENDUS

## 2.1 Objectif général

Concevoir, réaliser et déployer dans une organisation un **système automatisé de
supervision et de détection des pannes réseau**, fondé exclusivement sur des
scripts et des outils open-source, capable de **détecter les pannes en temps
réel**, d'**alerter instantanément** les équipes et de **réduire le temps
d'intervention**, tout en assurant la **traçabilité** des incidents.

## 2.2 Objectifs spécifiques

1. **Analyser** l'existant et comparer les principales solutions de supervision
   afin de positionner la solution proposée.
2. **Concevoir** une architecture modulaire et extensible reposant sur des
   briques open-source (Linux, Python, Cron, MySQL, Flask, Telegram), formalisée
   en **UML** et **MERISE**.
3. **Développer** les modules de **découverte** des équipements, de
   **surveillance** de la disponibilité (sondes ICMP et TCP) et de
   **journalisation**.
4. **Mettre en place** un système d'**alertes multi-canal** en temps réel
   (e-mail et Telegram), robuste aux faux positifs et au « spam » d'alertes.
5. **Réaliser** un **tableau de bord web** de visualisation, de gestion et de
   reporting.
6. **Évaluer** les performances et **mesurer** l'apport de l'automatisation par
   rapport à la supervision manuelle.

## 2.3 Hypothèses de recherche

| Code | Hypothèse |
|------|-----------|
| **H1** | L'automatisation réduit le **temps moyen de détection (MTTD)** par rapport à la supervision manuelle. |
| **H2** | Les alertes temps réel (e-mail + Telegram) réduisent le **temps moyen de réaction (MTTR)** des équipes. |
| **H3** | L'usage exclusif d'outils open-source atteint un niveau de service comparable aux solutions propriétaires pour un **coût quasi nul**. |
| **H4** | La journalisation systématique améliore la **traçabilité** et le **taux de disponibilité** du parc supervisé. |

## 2.4 Résultats attendus (indicateurs)

Les objectifs sont assortis d'**indicateurs mesurables** servant à valider les
hypothèses :

| Résultat attendu | Indicateur cible |
|------------------|------------------|
| Détection en temps réel | **MTTD < 2 minutes** (vs ~30–60 min) |
| Réaction rapide de l'astreinte | **MTTR < 5 minutes** (vs ~45 min) |
| Surveillance autonome | **0 intervention humaine** sur la collecte |
| Traçabilité complète | **100 %** des vérifications journalisées |
| Disponibilité améliorée | **≈ 97,5 % → ≈ 99,5 %** |
| Coût de licence | **0 FCFA** (open-source) |

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CHAPITRE 3 — DÉMARCHE MÉTHODOLOGIQUE

## 3.1 Type de recherche

Ce travail relève d'une **recherche appliquée** à caractère **expérimental**.
Il ne se limite pas à analyser un phénomène : il vise à **produire un artefact**
— le système de supervision — et à en **évaluer l'efficacité** par la mesure. Il
s'inscrit dans le paradigme de la **recherche-conception** (*Design Science
Research*), particulièrement adapté aux sciences de l'ingénieur, où la
connaissance se construit à travers la conception, la réalisation et
l'évaluation d'un système répondant à un problème concret.

## 3.2 Approche méthodologique

L'approche combine une dimension **qualitative** (analyse de l'existant, étude
comparative des solutions, observation des pratiques de terrain) et une
dimension **quantitative** (mesure de métriques : temps de détection, temps de
réaction, taux de disponibilité, latence). Le **cycle de développement** est
**itératif et incrémental**, inspiré de la philosophie **DevOps** :

> Analyse → Conception (UML / MERISE) → Développement → Test → Intégration →
> Mesure → *itération*

Chaque module a été développé, testé puis intégré avant de passer au suivant,
ce qui a permis une montée en charge progressive et un contrôle continu de la
qualité.

## 3.3 Techniques et outils de collecte des données

- **Recherche documentaire** : ouvrages, articles, documentations techniques et
  standards (RFC) relatifs à la supervision réseau ;
- **Observation participante** : analyse, sur le terrain, des
  pratiques de supervision manuelle et des incidents traités ;
- **Expérimentation** : déploiement d'un prototype dans un **environnement de
  test** (réseau local et machines virtuelles reproduisant un parc client) et
  **collecte automatisée des métriques** via les journaux du système ;
- **Entretiens informels** avec les techniciens d'astreinte pour
  recueillir les temps de détection/réaction de référence.

## 3.4 Méthode d'analyse

L'analyse procède par **comparaison « avant / après »** (supervision manuelle
*versus* supervision automatisée), à l'aide d'**indicateurs de performance
(KPI)** : MTTD, MTTR, taux de disponibilité et latence moyenne. Les résultats
sont présentés sous forme de **tableaux** et de **graphiques** afin de
**valider ou réfuter les hypothèses**. La conception est formalisée avec la
notation **UML** (sept diagrammes) et la méthode **MERISE** pour la base de
données.

## 3.5 Outils techniques mobilisés

| Catégorie | Outil retenu | Rôle |
|-----------|--------------|------|
| Système d'exploitation | Ubuntu Server 22.04 LTS | Hôte du serveur de supervision |
| Langage | Python 3 | Moteur de collecte et logique métier |
| Ordonnancement | Cron | Exécution périodique automatique |
| Base de données | MySQL 8 | Stockage (équipements, journaux, alertes) |
| Framework web | Flask | Tableau de bord et API REST |
| Interface | Bootstrap 5, Chart.js | Présentation responsive et graphiques |
| Notifications | SMTP, API Bot Telegram | Alertes e-mail et push mobile |
| Modélisation | UML (PlantUML), MERISE | Conception |
| Tests | unittest / pytest | Validation logicielle |

## 3.6 Planning de réalisation du projet

Le projet a été conduit sur une période d'environ quatre mois, selon un
découpage en phases successives mais partiellement recouvrantes (approche
itérative).

| Phase | Activités principales | Durée indicative |
|-------|------------------------|------------------|
| 1. Cadrage | Observation du terrain, recueil du besoin, problématique | 2 semaines |
| 2. État de l'art | Recherche documentaire, comparaison des solutions | 2 semaines |
| 3. Conception | Architecture, UML, MERISE, choix technologiques | 3 semaines |
| 4. Développement | Moteur, sondes, alertes, base de données, tableau de bord | 5 semaines |
| 5. Tests | Tests unitaires, fonctionnels et de performance | 2 semaines |
| 6. Évaluation | Mesures comparatives, analyse des résultats | 2 semaines |
| 7. Rédaction | Rédaction du mémoire et préparation de la soutenance | en continu |

## 3.7 Délimitation du champ de l'étude

L'étude porte sur la **supervision active de disponibilité** (sondes ICMP et
TCP) et la **détection de pannes** au niveau des couches réseau (3) et
transport/application (4–7). La supervision fine des **métriques internes** des
équipements (CPU, mémoire, trafic) par **SNMP**, ainsi que les aspects
contractuels détaillés des SLA, sont identifiés comme **perspectives** et
n'entrent pas dans le périmètre du prototype.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


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


# CHAPITRE 5 — L'AXE DE DIFFÉRENCIATION (INNOVATION TECHNOLOGIQUE)

## 5.1 Une innovation par l'assemblage

L'innovation de la solution ne réside pas dans l'invention d'un protocole
nouveau, mais dans un **assemblage différenciant** de briques éprouvées,
positionné exactement sur le besoin des organisations et de leurs utilisateurs. Là où chaque
solution concurrente impose un compromis — gratuité *contre* complexité, ou
simplicité *contre* coût —, la solution proposée **réunit** simplicité,
gratuité, légèreté, notification mobile native et ouverture vers l'IA.

## 5.2 Les facteurs de différenciation

| Différenciateur | Bénéfice pour l'organisation |
|-----------------|--------------------------|
| **Alerte Telegram native** | Astreinte alertée partout, sans coût de notification |
| **Ultra-légèreté** | 1 VM par client ou mutualisée : coûts d'exploitation réduits |
| **Code 100 % ouvert et maîtrisé** | Adaptation à chaque client, **zéro vendor lock-in** |
| **« Plug & supervise »** | Découverte automatique : onboarding d'un client en < 30 min |
| **Traçabilité orientée SLA** | Journaux exploitables comme **preuve de service** au client |
| **Prêt pour l'IA** | Historique structuré → futur service de **maintenance prédictive** |

## 5.3 Le marqueur : la notification mobile instantanée

Le principal marqueur d'innovation est l'intégration **native** d'un canal de
notification **push mobile gratuit** via **Telegram**. Sur ce point, les
solutions concurrentes imposent un plugin, une application payante ou une
passerelle SMS facturée. Pour une ESN dont la réactivité de l'astreinte est le
cœur de métier, recevoir l'alerte **instantanément sur smartphone**, où que l'on
soit, constitue un **avantage opérationnel et concurrentiel** direct.

## 5.4 Un socle évolutif

L'architecture **modulaire** et le stockage **structuré** de l'historique
préparent des évolutions à forte valeur : intégration de **SNMP**, détection
d'anomalies par **apprentissage automatique**, **maintenance prédictive** et
**auto-remédiation** (AIOps). La différenciation est donc aussi **temporelle** :
la solution constitue une **base de croissance** pour une offre de service.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CHAPITRE 6 — ÉTUDE DE FAISABILITÉ ET CONCEPTION DE LA SOLUTION

## 6.1 Étude de faisabilité

### 6.1.1 Faisabilité technique

Toutes les briques retenues sont **matures, documentées et éprouvées** (Linux,
Python, MySQL, Flask). Les compétences nécessaires sont **déjà présentes** au
sein de l'organisation. La preuve de faisabilité est apportée par un **prototype
réalisé, testé et fonctionnel** (chapitres 7 et 8).

### 6.1.2 Faisabilité économique

Le coût de **licence est nul** (open-source) ; le matériel se réduit à un
**serveur léger** (machine virtuelle ou mini-serveur), éventuellement
**mutualisé** entre plusieurs clients. L'investissement initial est de l'ordre
de **130 000 FCFA** (détail au chapitre 10).

### 6.1.3 Faisabilité organisationnelle

La solution s'**intègre au processus d'astreinte** existant : les
alertes alimentent directement les canaux déjà utilisés par les équipes
(messagerie, Telegram). Le déploiement et la prise en main sont **rapides**.

> **Conclusion :** le projet est faisable sur les plans technique, économique et
> organisationnel.

## 6.2 Spécification des besoins

### 6.2.1 Besoins fonctionnels

- **BF1** — gérer l'inventaire des équipements (ajout, modification,
  suppression) ;
- **BF2** — découvrir automatiquement les équipements d'un sous-réseau ;
- **BF3** — surveiller périodiquement la disponibilité (ICMP) et les services
  (TCP) ;
- **BF4** — journaliser chaque vérification ;
- **BF5** — détecter les pannes selon un seuil d'échecs (anti-faux positif) ;
- **BF6** — émettre des alertes temps réel par e-mail et Telegram ;
- **BF7** — afficher un tableau de bord temps réel et des rapports ;
- **BF8** — permettre l'acquittement des alertes ;
- **BF9** — authentifier les utilisateurs du tableau de bord.

### 6.2.2 Besoins non fonctionnels

- **BNF1 — Performance** : un cycle sur une centaine d'équipements doit
  s'exécuter en quelques secondes (sondes parallélisées) ;
- **BNF2 — Fiabilité** : le moteur ne doit jamais s'interrompre sur l'échec
  d'une sonde ;
- **BNF3 — Sécurité** : secrets hors du code, mots de passe hachés, requêtes SQL
  paramétrées, communications chiffrées ;
- **BNF4 — Portabilité** : déploiement sur tout serveur Linux standard ;
- **BNF5 — Maintenabilité** : architecture modulaire, code commenté ;
- **BNF6 — Ergonomie** : interface web responsive et intuitive.

## 6.3 Architecture technique en cinq couches

L'architecture s'organise en **cinq couches** faiblement couplées, du système
d'exploitation jusqu'à la présentation (figure 1).

![Figure 1 — Architecture en cinq couches du système de supervision](../architecture/architecture-5couches.png)

Le **choix d'ingénierie majeur** est le **découplage** entre le **moteur de
collecte** (script Python lancé par Cron) et l'**interface web** (Flask) : ils
communiquent uniquement par la **base de données**. La surveillance se poursuit
donc même si le tableau de bord est arrêté, ce qui renforce la robustesse.

### 6.3.1 Justification des choix technologiques

| Brique | Technologie | Justification |
|--------|-------------|---------------|
| OS | Ubuntu Server 22.04 LTS | Gratuit, stable (LTS), léger, outils réseau natifs |
| Langage | Python 3 | Lisibilité, écosystème réseau, productivité |
| Ordonnancement | Cron | Natif, fiable, sans dépendance ; découple collecte/interface |
| SGBD | MySQL 8 | Robuste, transactionnel (InnoDB), accès concurrents |
| Web | Flask | Micro-framework léger, courbe d'apprentissage faible |
| Front-end | Bootstrap 5, Chart.js | Interface responsive et graphiques dynamiques |
| E-mail | SMTP (smtplib) | Standard universel, traçabilité écrite |
| Mobile | Bot Telegram | Notification push gratuite, instantanée → réactivité |

## 6.4 Conception UML

La conception est formalisée par **sept diagrammes UML**, du niveau le plus
abstrait (contexte) au plus concret (déploiement).

### 6.4.1 Diagramme de contexte

Il présente le système comme une entité unique et ses quatre acteurs :
l'**administrateur** (technicien réseau), les **équipements** supervisés, le
**serveur SMTP** et le **service Telegram** (figure 2).

![Figure 2 — Diagramme de contexte](../architecture/diagrammes/diagramme-contexte.png)

### 6.4.2 Diagramme de cas d'utilisation

Il formalise les interactions : l'administrateur gère les équipements, consulte
le tableau de bord, acquitte les alertes ; le système (Cron) déclenche la
supervision, qui *inclut* la journalisation et la détection, et *étend* le
déclenchement des alertes (figure 3).

![Figure 3 — Diagramme de cas d'utilisation](../architecture/diagrammes/cas-utilisation.png)

### 6.4.3 Diagramme de séquence

Il décrit chronologiquement le scénario de **détection et d'alerte** : Cron
déclenche le moteur, qui charge les équipements, lance les sondes, met à jour la
base et, en cas de panne confirmée, fait diffuser l'alerte par e-mail et
Telegram après contrôle anti-spam (figure 4).

![Figure 4 — Diagramme de séquence](../architecture/diagrammes/diagramme-sequence.png)

### 6.4.4 Diagramme d'activité

Il modélise le flux de contrôle d'un cycle : test ICMP puis éventuellement TCP,
mise à jour du statut, journalisation, puis branche décisionnelle (panne
confirmée → alerte ; retour en ligne → rétablissement), figure 5.

![Figure 5 — Diagramme d'activité](../architecture/diagrammes/diagramme-activite.png)

### 6.4.5 Diagramme de classes

Il présente le modèle du domaine : classes `Equipement`, `Journal`, `Alerte`,
`Utilisateur`, `Statistique`, et classes de service `SondeICMP`,
`SondeService`, `GestionnaireAlertes`, `CanalEmail`, `CanalTelegram` (figure 6).
Les associations expriment qu'un équipement *génère* des journaux et *déclenche*
des alertes, qu'un **utilisateur** *supervise* plusieurs équipements (relation
plusieurs-à-plusieurs) et *acquitte* plusieurs alertes (relation 1..n).

![Figure 6 — Diagramme de classes](../architecture/diagrammes/diagramme-classes.png)

### 6.4.6 Diagramme de composants

Il montre l'organisation logicielle en paquets : interface (Flask + API REST),
moteur (Cron, orchestrateur, sondes, découverte), alertes (gestionnaire +
canaux) et couche d'accès aux données reliée à MySQL (figure 7).

![Figure 7 — Diagramme de composants](../architecture/diagrammes/diagramme-composants.png)

### 6.4.7 Diagramme de déploiement

Il décrit la répartition physique des artefacts : serveur Ubuntu (moteur, Flask,
Cron, MySQL), équipements supervisés, poste administrateur, smartphone et
services externes (SMTP, Telegram), figure 8.

![Figure 8 — Diagramme de déploiement](../architecture/diagrammes/diagramme-deploiement.png)

## 6.5 Conception de la base de données (méthode MERISE)

La base est conçue selon la méthode **MERISE** : du **Modèle Conceptuel de
Données (MCD)** vers le **Modèle Logique (MLD)**, puis le modèle physique
(script SQL).

### 6.5.1 Modèle Conceptuel de Données (MCD)

Le MCD décrit les entités et leurs associations (figure 9) : un **équipement**
*génère* plusieurs **journaux** et *déclenche* plusieurs **alertes** ; un
**utilisateur** *supervise* plusieurs équipements — relation
**plusieurs-à-plusieurs** (0,n)–(1,n) — et *acquitte* plusieurs **alertes** —
relation (1,n). La **statistique** complète le modèle.

![Figure 9 — Modèle Conceptuel de Données (MCD)](../database/mcd.png)

### 6.5.2 Modèle Logique de Données (MLD)

Le MLD traduit le MCD en tables relationnelles avec clés primaires (PK) et
étrangères (FK) — figure 10. La relation plusieurs-à-plusieurs « supervise » est,
conformément aux règles de transformation MERISE, **résolue par une table
associative** `responsabilite` (clé primaire composite). On obtient ainsi
**six tables** : `utilisateurs`, `equipements`, `journaux`, `alertes`,
`responsabilite` et `statistiques`. La relation « acquitte » se matérialise par
la clé étrangère `acquittee_par` dans la table `alertes`.

![Figure 10 — Modèle Logique de Données (MLD)](../database/mld.png)

### 6.5.3 Choix physiques

Moteur **InnoDB** (transactions + intégrité référentielle), jeu de caractères
**utf8mb4**, **index** sur les colonnes filtrées (`statut`, `acquittee`,
`equipement_id`), suppression en **cascade** des journaux/alertes à la
suppression d'un équipement, et contrainte d'**unicité** sur l'adresse IP.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


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


# CHAPITRE 8 — DÉMONSTRATION : LES ÉCRANS DE LA SOLUTION

Ce chapitre présente la solution **réalisée et fonctionnelle** à travers ses
principaux écrans, illustrés sur un **parc client d'exemple** supervisé par OPEN
MOISE (huit équipements, dont deux en panne). Les captures correspondent au
rendu réel de l'application (Flask + Bootstrap).

## 8.1 L'accès sécurisé (page de connexion)

L'accès au tableau de bord est protégé par une **authentification** (figure 11).
Les identifiants sont vérifiés contre la table `utilisateurs`, où les mots de
passe sont stockés **hachés** (jamais en clair). Toute tentative d'accès non
authentifiée est redirigée vers cette page.

![Figure 11 — Page de connexion sécurisée](../soutenance/captures/capture-login.png)

## 8.2 Le tableau de bord

Le tableau de bord (figure 12) offre, en un coup d'œil, une **vue d'ensemble**
de l'état du parc : quatre **indicateurs clés (KPI)** — nombre d'équipements
supervisés, en ligne, hors ligne et alertes actives —, un **anneau de
disponibilité** (ici **75 %**), la liste des **alertes actives** et l'**état
détaillé** de chaque équipement avec son statut, sa latence et l'horodatage de
la dernière vérification. Les équipements en panne (Serveur-BDD, Imprimante-RH)
apparaissent en **rouge (DOWN)**.

![Figure 12 — Tableau de bord temps réel](../soutenance/captures/capture-dashboard.png)

Le rafraîchissement automatique (AJAX, toutes les 30 secondes) maintient
l'affichage à jour sans rechargement de page, offrant aux techniciens d'OPEN
MOISE une **vision permanente et synthétique** de tous les parcs supervisés.

## 8.3 La détection d'une panne et l'alerte instantanée

Lorsqu'un équipement cesse de répondre, le moteur confirme la panne (seuil
d'échecs) puis déclenche une **alerte multi-canal**. La figure 13 montre la
**notification Telegram** telle que la reçoit l'équipe d'astreinte sur son
smartphone : équipement concerné, adresse IP, type et sévérité de l'alerte, et
message détaillé. Au retour en ligne, une seconde notification annonce le
**rétablissement**.

![Figure 13 — Notification Telegram reçue par l'astreinte (smartphone)](../soutenance/captures/capture-telegram.png)

C'est l'élément le plus déterminant de la solution : l'alerte parvient à
l'équipe **en moins de deux minutes**, **où qu'elle se trouve**, ce qui réduit
drastiquement le temps de réaction.

## 8.4 L'historique des alertes

La page « Alertes » (figure 14) conserve l'**historique complet** des
événements, avec leur **sévérité** (CRITIQUE, AVERTISSEMENT, INFO) et leur
**état** (en attente / acquittée). L'**acquittement** permet au technicien de
marquer une alerte comme prise en charge. Cet historique constitue une
**preuve de respect des SLA** opposable au client.

![Figure 14 — Historique des alertes](../soutenance/captures/capture-alertes.png)

## 8.5 La gestion des équipements

La page « Équipements » (figure 15) présente l'**inventaire** du parc client :
nom, adresse IP, type, emplacement, service supervisé et statut. L'inventaire
est **alimenté automatiquement** par la découverte réseau ; le technicien peut
également **ajouter ou retirer** un équipement en quelques clics.

![Figure 15 — Gestion des équipements](../soutenance/captures/capture-equipements.png)

## 8.6 Les rapports et statistiques

La page « Rapports » (figure 16) synthétise les **indicateurs de performance** :
taux de disponibilité, latence moyenne et nombre d'alertes actives, ainsi qu'un
**graphique** de la latence par équipement. Ces rapports, **exportables** (impression
/ PDF), permettent de **rendre compte** périodiquement aux clients ou à la direction
de la qualité de service délivrée.

![Figure 16 — Rapports et statistiques](../soutenance/captures/capture-rapports.png)

## 8.7 Synthèse de la démonstration

| Écran | Ce qu'il prouve |
|-------|--------------------------------|
| Connexion | Accès **sécurisé** et authentifié |
| Tableau de bord | Supervision temps réel, KPI, anneau de disponibilité |
| Notification Telegram | Astreinte alertée sur smartphone en **< 2 min** |
| Historique des alertes | Traçabilité + acquittement (**preuve de SLA**) |
| Gestion des équipements | Inventaire + **découverte automatique** des parcs |
| Rapports | Statistiques et rapports de disponibilité **exportables** |

La démonstration établit que la solution **fonctionne de bout en bout** : de
l'accès sécurisé à la détection automatique d'une panne, jusqu'à l'alerte
instantanée de l'astreinte et au reporting exploitable au profit du client.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# CHAPITRE 9 — MARKETING, VENTE ET CONCURRENCE

## 9.1 Une double valeur

La solution présente une **double valeur** pour toute organisation — ou pour un prestataire de services :

1. **Outil interne** : elle industrialise la supervision des parcs déjà gérés,
   fiabilise le respect des **SLA**, réduit la charge d'astreinte et renforce la
   relation de confiance avec les clients existants ;
2. **Nouvelle offre commerciale** : elle devient un **service de supervision
   managée** facturable, que l'entreprise peut proposer à l'ensemble de son
   portefeuille et à de nouveaux prospects.

## 9.2 Segmentation et cible

Le marché visé est celui des organisations ne disposant pas d'une équipe
informatique étoffée, mais dépendantes de leur réseau :

- **PME et commerces** (agences, cabinets, distribution) ;
- **Établissements** (écoles, cliniques, hôtels) ;
- **Administrations et collectivités** ;
- **Hébergeurs, cybercafés et autres ESN** partenaires.

## 9.3 Proposition de valeur

> *« Nous surveillons votre réseau 24h/24 et intervient avant que vous ne
> constatiez la panne — sans licence, sans matériel coûteux. »*

Cette proposition transforme un **centre de coût** (la maintenance réactive) en
un **service à valeur ajoutée**, proactif et contractualisé.

## 9.4 Modèle économique (open-core et service managé)

| Composante | Description | Mode de revenu |
|------------|-------------|----------------|
| Cœur open-source | Le moteur et le tableau de bord, gratuits | Adoption / confiance |
| Mise en service | Installation, paramétrage, formation chez le client | Forfait unique |
| Supervision managée | Surveillance continue + astreinte | **Abonnement mensuel** |
| Option « Pro » | SNMP, multi-sites, IA prédictive, rapports SLA avancés | Supplément |

## 9.5 Positionnement concurrentiel

| Critère | Nagios/Zabbix | PRTG/SolarWinds | **Solution proposée** |
|---------|:-------------:|:---------------:|:--------------------:|
| Prix | Gratuit mais coûteux à exploiter | Très coûteux | **Gratuit + services** |
| Simplicité | Faible | Élevée | **Élevée** |
| Légèreté | Moyenne / faible | Faible | **Très élevée** |
| Alerte mobile native | Plugin | Application | **Telegram natif** |
| Sur-mesure / ouvert | Limité | Non | **Total** |

**Stratégie « océan bleu » :** plutôt que d'affronter les géants sur le segment
des grandes infrastructures, la solution se **différencie auprès des PME** avec
une offre **simple, sans licence et au prix du marché local**, là où les
solutions internationales sont trop chères ou trop lourdes.

## 9.6 Plan d'action commercial

1. **Déployer** la solution en interne et l'**éprouver** sur les clients
   existants (preuve par l'usage) ;
2. **Packager** l'offre de supervision managée (niveaux de service et tarifs) ;
3. **Communiquer** : démonstrations, témoignages clients, présence en ligne ;
4. **Convertir** progressivement le portefeuille existant à l'abonnement ;
5. **Prospecter** de nouveaux clients sur la base des résultats mesurés.

## 9.7 Analyse SWOT de l'offre

| Forces (Strengths) | Faiblesses (Weaknesses) |
|--------------------|--------------------------|
| Coût nul de licence, marge élevée | Dépend des compétences internes (clé de l'humain) |
| Notification mobile native (Telegram) | Pas encore de métriques SNMP / IA |
| Solution maîtrisée et personnalisable | Notoriété de l'offre à construire |
| Déploiement rapide (« plug & supervise ») | Serveur de supervision à sécuriser/redonder |

| Opportunités (Opportunities) | Menaces (Threats) |
|------------------------------|--------------------|
| Forte demande PME (digitalisation, mobile money) | Concurrence des grands éditeurs |
| Évolution vers la maintenance prédictive (IA) | Solutions cloud SaaS low-cost |
| Élargissement du portefeuille existant | Exigence croissante des SLA clients |
| Partenariats avec d'autres ESN locales | Dépendance à la connectivité Internet |

Cette analyse confirme que les **forces** et les **opportunités** l'emportent :
l'offre s'appuie sur un avantage de coût structurel et répond à une demande
croissante, tandis que les faiblesses identifiées correspondent précisément aux
**perspectives** d'évolution (chapitre 11).

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CHAPITRE 10 — PRÉVISIONS FINANCIÈRES

> *Montants exprimés en francs CFA (XOF). Parité fixe de référence : 1 € =
> 655,957 FCFA. Les hypothèses sont indicatives et à ajuster aux prix réellement
> pratiqués sur le marché ivoirien.*

## 10.1 Investissement initial

| Poste | Coût (FCFA) |
|-------|-------------|
| Licences logicielles | **0** (100 % open-source) |
| Serveur / VM (mutualisable) | 100 000 – 200 000 |
| Développement et déploiement | Interne (déjà réalisé) |
| **Total d'entrée** | **≈ 130 000 FCFA** |

L'investissement est **quasi nul** : absence de licence, matériel léger et
mutualisable, développement réalisé en interne dans le cadre de ce projet.

## 10.2 Revenus et gains prévisionnels (année 1)

| Source | Hypothèse | Montant (FCFA) |
|--------|-----------|----------------|
| Supervision managée | 10 clients × 25 000 FCFA/mois | 3 000 000 |
| Mise en service | 10 × 200 000 FCFA | 2 000 000 |
| Option « Pro » (SNMP/IA) | 3 × 325 000 FCFA | 975 000 |
| Pénalités SLA évitées | estimation | gain additionnel |
| **Total année 1** | | **≈ 6 000 000 FCFA** |

## 10.3 Analyse de rentabilité et seuil critique

Le **seuil de rentabilité** est atteint extrêmement tôt : l'investissement
d'entrée (**≈ 130 000 FCFA**) est couvert dès le **premier mois** d'abonnement
d'un seul client (25 000 FCFA/mois) cumulé à sa mise en service (200 000 FCFA).
Autrement dit, **un seul client** suffit à rentabiliser le projet.

Au-delà, chaque client supplémentaire en supervision managée génère un **revenu
récurrent** de l'ordre de **300 000 FCFA par an** (25 000 × 12), pour un coût
marginal d'exploitation très faible (le serveur étant mutualisé). La marge est
donc **élevée et croissante** avec le nombre de clients.

## 10.4 Gains internes (économies)

Outre les revenus, la solution génère des **économies
internes** :

- **Réduction du temps d'astreinte** consacré à la détection manuelle ;
- **Diminution des pénalités SLA** grâce à une détection et une intervention
  plus rapides ;
- **Préservation de l'image** et **fidélisation** des clients, donc réduction du
  coût de renouvellement du portefeuille.

## 10.5 Synthèse financière

| Indicateur | Valeur |
|------------|--------|
| Investissement initial | ≈ 130 000 FCFA |
| Revenus prévisionnels année 1 | ≈ 6 000 000 FCFA |
| Coût de licence | 0 FCFA |
| Seuil de rentabilité | **≈ 1 client** |

Le projet présente ainsi un **rapport bénéfice/coût très favorable** : un
investissement marginal pour des revenus récurrents et des économies internes
substantielles.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# CHAPITRE 11 — LIMITES DU PROJET ET PERSPECTIVES

## 11.1 Limites du projet

Le travail réalisé, bien que fonctionnel et probant, présente des **limites**
assumées :

1. **Supervision active uniquement** : la solution mesure la disponibilité
   (ICMP/TCP) mais ne collecte pas encore les **métriques internes** des
   équipements (CPU, mémoire, trafic), qui nécessiteraient le protocole
   **SNMP** ;
2. **Réactivité bornée** : l'intervalle de cycle (2 minutes) constitue une
   borne minimale du temps de détection ;
3. **Dépendance à la connectivité sortante** : l'acheminement des alertes
   (SMTP, Telegram) suppose un accès Internet fonctionnel sur le site supervisé ;
4. **« Qui surveille le surveillant ? »** : le serveur de supervision est
   lui-même un point de défaillance, d'où la nécessité d'une **redondance** pour
   les environnements critiques ;
5. **Périmètre fonctionnel** : la gestion fine des contrats SLA, la facturation
   et le portail multi-clients restent à développer pour une exploitation
   commerciale à grande échelle.

## 11.2 Recommandations opérationnelles

Pour un déploiement en production, nous recommandons de :

- placer le serveur de supervision sur un **VLAN d'administration** dédié et lui
  attribuer une **adresse IP fixe** ;
- l'adosser à un **onduleur (UPS)** : il doit survivre aux coupures qu'il
  surveille ;
- **sauvegarder régulièrement** la base de données (historique et configuration) ;
- **changer les identifiants par défaut** et appliquer une politique de mots de
  passe robustes ;
- prévoir une **redondance** (second serveur en veille) pour les clients
  critiques.

## 11.3 Perspectives d'évolution

La solution constitue une **base extensible**. Les perspectives, qui dessinent
aussi une feuille de route d'évolution, sont :

- **Intégration de SNMP** : supervision des performances internes (CPU,
  mémoire, bande passante), pour une offre plus complète ;
- **Seuils de performance** : alerte préventive lorsque la latence ou la charge
  dépasse un seuil ;
- **Intelligence artificielle** : détection d'**anomalies** par apprentissage
  automatique sur l'historique multi-clients, repérant des comportements
  anormaux **avant** la panne franche ;
- **Maintenance prédictive** : anticipation des défaillances à partir des
  tendances, valorisable comme **offre premium** ;
- **Auto-remédiation (AIOps)** : déclenchement automatique d'actions
  correctives sûres (redémarrage d'un service, bascule sur un lien de secours) ;
- **Portail multi-clients** et **conteneurisation** (Docker/Kubernetes) pour
  industrialiser le déploiement et la facturation ;
- **Canaux additionnels** : SMS, Slack, Microsoft Teams.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CONCLUSION GÉNÉRALE

Ce mémoire-projet s'est attaché à répondre à un besoin concret et stratégique de
les organisations : **détecter en temps réel les pannes des réseaux
qu'elle supervise et réduire le temps d'intervention de ses équipes**, à un coût
maîtrisé. Partant du constat des limites de la supervision **manuelle et
réactive** — détection tardive, absence de traçabilité, risque sur les SLA — et
de l'inadéquation, pour une structure de cette taille, des solutions du marché
(trop complexes ou trop coûteuses), nous avons **conçu, réalisé et déployé un
système d'automatisation de la supervision et de la détection des pannes
réseau**, fondé **exclusivement sur des outils open-source**.

La démarche a suivi un cheminement rigoureux, conforme au canevas
mémoire-projet : identification du **problème**, définition des **objectifs** et
de la **méthodologie**, **état des lieux** des solutions et conception d'une
**solution différenciante**, **étude de faisabilité** et **conception** (UML,
MERISE, architecture en cinq couches), **réalisation technique**, puis
**démonstration** sur les écrans réels de l'application. Le volet
entrepreneurial — **marketing, concurrence et prévisions financières en francs
CFA** — a montré que la solution dépasse le simple outil interne pour devenir une
**offre commerciale** viable.

Les évaluations menées **confirment les quatre hypothèses** : l'automatisation
fait chuter le temps de détection d'environ une heure à **moins de deux
minutes**, réduit le temps de réaction grâce aux **notifications instantanées**,
améliore le **taux de disponibilité** et assure une **traçabilité complète**, le
tout pour un **coût de licence nul**. Sur le plan économique, l'investissement
(**≈ 130 000 FCFA**) est rentabilisé dès le **premier client**, pour des revenus
récurrents et des économies internes significatives.

Au-delà de l'artefact produit, ce travail démontre qu'une **maîtrise des briques
open-source** permet à une ESN ivoirienne de bâtir des solutions **sur mesure,
efficaces et économiques**, et d'en faire un **avantage concurrentiel**. Les
perspectives ouvertes — **SNMP**, **intelligence artificielle**, **maintenance
prédictive** et **auto-remédiation** — tracent la voie d'une supervision
**proactive et intelligente**, qui ne se contente plus de constater les pannes
mais cherche à les **anticiper**. C'est dans cette direction que pourront se
prolonger les travaux futurs, au service de la compétitivité des organisations et de
la qualité de service rendue à ses clients.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# BIBLIOGRAPHIE

**Ouvrages**

1. Tanenbaum, A. S., & Wetherall, D. J. (2021). *Computer Networks* (6ᵉ éd.). Pearson.
2. Kurose, J. F., & Ross, K. W. (2020). *Computer Networking: A Top-Down Approach* (8ᵉ éd.). Pearson.
3. Mauro, D., & Schmidt, K. (2005). *Essential SNMP* (2ᵉ éd.). O'Reilly Media.
4. Kim, G., Humble, J., Debois, P., & Willis, J. (2016). *The DevOps Handbook*. IT Revolution Press.
5. Edelman, J., Lowe, S. S., & Oswalt, M. (2018). *Network Programmability and Automation*. O'Reilly Media.
6. Raymond, E. S. (1999). *The Cathedral and the Bazaar*. O'Reilly Media.
7. Sridharan, C. (2018). *Distributed Systems Observability*. O'Reilly Media.
8. Grinberg, M. (2018). *Flask Web Development* (2ᵉ éd.). O'Reilly Media.

**Articles et standards**

9. ISO/IEC. (1989). *ISO/IEC 7498-4 — OSI Management framework* (modèle FCAPS).
10. Postel, J. (1981). *RFC 792 — Internet Control Message Protocol (ICMP)*. IETF.
11. Case, J., et al. (1990). *RFC 1157 — Simple Network Management Protocol (SNMP)*. IETF.
12. Klensin, J. (2008). *RFC 5321 — Simple Mail Transfer Protocol (SMTP)*. IETF.

**Ressources en ligne**

13. Nagios Enterprises. (2024). *Nagios Core Documentation*. https://www.nagios.org
14. Zabbix LLC. (2024). *Zabbix Documentation*. https://www.zabbix.com/documentation
15. Python Software Foundation. (2024). *Python 3 Documentation*. https://docs.python.org
16. Pallets Projects. (2024). *Flask Documentation*. https://flask.palletsprojects.com
17. Oracle. (2024). *MySQL 8.0 Reference Manual*. https://dev.mysql.com/doc
18. Telegram. (2024). *Telegram Bot API*. https://core.telegram.org/bots/api

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# ANNEXES

**Annexe A — Procédure d'installation et de déploiement.** Préparation du
serveur Ubuntu, installation de MySQL et exécution du script `schema.sql`,
création de l'environnement virtuel Python, installation des dépendances,
configuration du fichier `.env`, mise en place du `cron` et lancement du tableau
de bord (Gunicorn). *(Voir `docs/INSTALLATION.md` du dépôt.)*

**Annexe B — Code source.** L'intégralité du code commenté figure dans le
dossier `src/` : moteur `supervisor.py`, application `app.py`, modules (sondes,
découverte, journalisation, alertes), templates et fichiers statiques.

**Annexe C — Script de création de la base de données.** Script SQL complet
(`database/schema.sql`) : création de la base, des six tables (dont la table
associative `responsabilite`), des contraintes,
de l'utilisateur applicatif et des données d'amorçage.

**Annexe D — Diagrammes UML et MERISE.** Sources PlantUML des sept diagrammes
UML et des modèles MCD/MLD (`architecture/diagrammes/`, `database/`).

**Annexe E — Configuration du bot Telegram.** Création d'un bot via @BotFather,
obtention du jeton (`TELEGRAM_BOT_TOKEN`) et de l'identifiant de discussion
(`TELEGRAM_CHAT_ID`), renseignés dans le fichier `.env`.

<div align="center">

*— FIN DU MÉMOIRE —*

</div>


