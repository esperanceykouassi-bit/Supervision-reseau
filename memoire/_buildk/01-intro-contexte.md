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
