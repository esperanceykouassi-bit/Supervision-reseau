# PRÉSENTATION DE LA STRUCTURE D'ACCUEIL : OPEN MOISE

> *Les informations entre crochets `[...]` sont à compléter avec les données
> officielles de l'entreprise (registre du commerce, organigramme, plaquette).*

## 1. Présentation générale

**OPEN MOISE** est une **Entreprise de Services du Numérique (ESN)** de droit
ivoirien, implantée à **[ville]** depuis **[année]**. Elle accompagne les
organisations — PME, administrations, établissements et commerces — dans la
**conception, le déploiement et l'exploitation** de leurs infrastructures
informatiques et réseau.

| Élément | Information |
|---------|-------------|
| Raison sociale | OPEN MOISE |
| Forme juridique | [SARL / SAS / …] |
| Année de création | [année] |
| Siège social | [adresse, ville — Côte d'Ivoire] |
| Secteur d'activité | Services numériques (ESN / infogérance) |
| Effectif | [nombre] collaborateurs |
| Dirigeant | [NOM Prénom] |

## 2. Mission et domaines d'activité

La mission d'OPEN MOISE est de **garantir à ses clients un système d'information
performant, disponible et sécurisé**. Ses principaux pôles d'activité sont :

- **Infogérance et supervision** : exploitation et surveillance des réseaux et
  systèmes des clients, dans le cadre de contrats de service (SLA) ;
- **Intégration réseau et systèmes** : installation d'équipements actifs
  (routeurs, commutateurs, pare-feu), de serveurs et de solutions de
  connectivité ;
- **Développement applicatif et conseil** : applications métier, automatisation
  des processus, accompagnement à la transformation numérique ;
- **Cybersécurité** : protection, sauvegarde et continuité d'activité.

## 3. Organisation

OPEN MOISE est structurée autour de plusieurs pôles — **[Direction technique,
Pôle Infrastructures & Supervision, Pôle Développement, Support client]**. Le
présent projet a été conduit au sein du **[Pôle Infrastructures &
Supervision]**, sous la responsabilité de **[NOM Prénom — fonction]**.

## 4. Justification du projet au sein d'OPEN MOISE

En tant qu'ESN assurant l'**infogérance** des infrastructures de ses clients,
OPEN MOISE est directement exposée à la problématique traitée dans ce mémoire :
**détecter au plus tôt les pannes** des parcs qu'elle exploite et **réduire le
temps d'intervention** de ses équipes d'astreinte. La solution développée
constitue un **outil interne à forte valeur ajoutée** : elle permet
d'**industrialiser** la supervision, d'**améliorer la qualité de service**
(respect des SLA), de **renforcer la traçabilité** des incidents et de
**maîtriser les coûts** grâce à l'usage exclusif de technologies open-source.
Elle ouvre en outre la voie à une **nouvelle offre commerciale** : la
**supervision managée** facturée aux clients.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# INTRODUCTION GÉNÉRALE

À l'ère de la transformation numérique, le réseau informatique constitue le
**système nerveux** de toute organisation. La messagerie, la téléphonie sur IP,
les applications métier, l'accès à Internet, les services bancaires en ligne ou
encore les systèmes de paiement mobile — omniprésents en Côte d'Ivoire et dans
la sous-région — reposent intégralement sur la disponibilité et la fiabilité de
l'infrastructure réseau. Une interruption de service, même brève, se traduit
par une perte de productivité, un manque à gagner, une dégradation de l'image
et, dans les secteurs critiques, par des conséquences plus lourdes encore.

Cette exigence de **continuité de service** est particulièrement aiguë pour les
**entreprises de services du numérique (ESN)** telles qu'**OPEN MOISE**, qui
exploitent les réseaux de leurs clients dans le cadre de contrats assortis
d'**engagements de niveau de service (SLA)**. Pour ces prestataires, la
capacité à **détecter rapidement les pannes** et à **intervenir avant que le
client ne s'en aperçoive** est un facteur déterminant de compétitivité et de
fidélisation.

Or, le constat dressé au sein d'OPEN MOISE — et largement partagé dans les
structures de taille comparable — est celui d'une supervision encore **manuelle
et réactive** : des contrôles ponctuels (commandes `ping`, connexions aux
équipements), une détection des incidents reposant le plus souvent sur le
**signalement du client**, et une **absence de traçabilité** exploitable. Ce
mode de fonctionnement allonge mécaniquement le **temps de détection** et le
**temps d'intervention**, fragilise le respect des SLA et mobilise inutilement
les ressources humaines.

Des solutions de supervision existent pourtant — propriétaires (PRTG,
SolarWinds) ou open-source (Nagios, Zabbix, Centreon). Mais les premières sont
**coûteuses** et les secondes, bien que puissantes, sont souvent jugées
**lourdes et complexes** à déployer et à maintenir pour une structure aux moyens
mesurés. Il existe donc un **espace** pour une solution **légère, économique,
sur mesure et entièrement maîtrisée**, bâtie à partir de briques open-source.

C'est l'objet de ce mémoire-projet : **concevoir, réaliser et déployer chez OPEN
MOISE un système d'automatisation de la supervision et de la détection des
pannes réseau**, fondé exclusivement sur des outils open-source, et **le penser
comme un véritable produit** — depuis le besoin du terrain jusqu'au modèle
économique. Conformément au canevas mémoire-projet, le document s'organise
ainsi : après l'identification du **problème** (chap. 1), nous précisons les
**objectifs** (chap. 2) et la **démarche méthodologique** (chap. 3), puis nous
réalisons l'**état des lieux** des solutions et présentons la **solution
proposée** (chap. 4) et son **axe de différenciation** (chap. 5). Suivent
l'**étude de faisabilité et la conception** (chap. 6), le **fonctionnement
technique** (chap. 7) et la **démonstration** illustrée par les écrans de
l'application (chap. 8). Enfin, nous abordons le volet **marketing et
concurrence** (chap. 9), les **prévisions financières** en francs CFA (chap.
10), puis les **limites et perspectives** (chap. 11), avant de conclure.

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

Parallèlement, les attentes en matière de **disponibilité** se sont élevées :
les organisations visent désormais des objectifs de l'ordre de **99,9 %**, soit
moins de neuf heures d'indisponibilité cumulée par an. Atteindre et **prouver**
de tels niveaux suppose une surveillance **continue, outillée et tracée** — ce
que la supervision manuelle ne permet pas.

### 1.1.1 Le contexte numérique ivoirien

La Côte d'Ivoire connaît une transformation numérique soutenue : extension de la
couverture en fibre optique, essor du **commerce électronique**, dématérialisation
des services publics et, surtout, prééminence du **paiement mobile (mobile
money)**, devenu un instrument quotidien pour des millions d'usagers et de
commerçants. Cette dépendance accrue au numérique élève le **coût de
l'indisponibilité** : une interruption réseau peut bloquer des transactions, des
encaissements et des services entiers. Pour les prestataires informatiques
locaux comme OPEN MOISE, la **qualité et la continuité de service** deviennent
ainsi des facteurs déterminants de différenciation, dans un marché où la maîtrise
des **coûts** reste néanmoins primordiale. Ce double impératif — fiabilité
*et* économie — oriente directement les choix de ce projet vers l'**open-source**.

## 1.2 Contexte spécifique : la supervision chez OPEN MOISE

En tant qu'ESN, OPEN MOISE exploite pour le compte de ses clients des parcs
hétérogènes : routeurs, commutateurs, pare-feu, serveurs (web, base de données,
fichiers), points d'accès Wi-Fi et imprimantes réseau. Chaque client est lié à
OPEN MOISE par un **contrat de service** précisant des engagements de
disponibilité et des délais d'intervention.

L'observation des pratiques au sein du pôle d'accueil révèle que la surveillance
de ces parcs s'effectue essentiellement **à la demande** : un technicien lance
des commandes `ping` ou se connecte aux équipements lorsqu'un dysfonctionnement
est suspecté ou signalé. Aucun dispositif n'assure une **veille permanente et
automatique** de l'ensemble des équipements.

## 1.3 Constat et formulation du problème

De cette situation découlent plusieurs **dysfonctionnements** :

1. **Détection tardive** : la panne est le plus souvent révélée par le **client
   lui-même**, c'est-à-dire *après* que le service a été dégradé. Le temps moyen
   de détection (MTTD) se compte en **dizaines de minutes**, voire en heures.
2. **Réaction différée** : l'équipe d'astreinte n'étant pas alertée
   automatiquement, le **temps moyen de réaction** (MTTR) s'allonge d'autant.
3. **Absence de traçabilité** : faute d'historisation, il est difficile de
   **prouver le respect des SLA**, d'analyser les pannes récurrentes ou de
   produire des rapports clients.
4. **Charge humaine et risque d'erreur** : la surveillance manuelle est
   **chronophage**, non extensible au-delà de quelques équipements, et sujette à
   la fatigue.
5. **Risque commercial** : la détection tardive met en péril les engagements
   contractuels et, à terme, la **relation de confiance** avec le client.

Le problème central se formule ainsi : **l'absence d'un dispositif automatisé,
accessible et économique de supervision empêche OPEN MOISE de détecter
précocement les pannes des réseaux qu'elle exploite et allonge le temps
d'intervention de ses équipes, au détriment de la qualité de service et de la
maîtrise des coûts.**

## 1.4 Questions de recherche

### Question principale

> **Comment OPEN MOISE peut-elle détecter en temps réel les pannes des réseaux
> qu'elle supervise et réduire le temps d'intervention de ses équipes, à l'aide
> d'une solution automatisée, fiable et économiquement accessible, fondée sur
> des outils open-source ?**

### Questions secondaires

1. Quels concepts et technologies fondent la supervision et l'automatisation
   réseau, et quelles solutions existent déjà sur le marché ?
2. Quelle architecture logicielle et matérielle, à base d'outils open-source,
   répond aux besoins d'OPEN MOISE ?
3. Comment notifier l'astreinte de manière instantanée et fiable, où qu'elle se
   trouve ?
4. Dans quelle mesure l'automatisation améliore-t-elle concrètement le temps de
   détection, le temps de réaction et le taux de disponibilité, et à quel coût ?

## 1.5 Justification et intérêt du sujet

L'intérêt de ce sujet est triple. Sur le plan **professionnel**, il répond à un
besoin réel et immédiat d'OPEN MOISE et améliore sa compétitivité. Sur le plan
**économique**, il démontre qu'une solution efficace peut être bâtie sans
licence coûteuse — argument décisif dans le contexte ivoirien. Sur le plan
**scientifique et pédagogique**, il mobilise l'ensemble des compétences du
Master RIT (réseaux, programmation, bases de données, systèmes Linux,
cybersécurité, DevOps) et s'inscrit dans les pratiques d'**ingénierie
contemporaines** (automatisation, observabilité, AIOps).

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
