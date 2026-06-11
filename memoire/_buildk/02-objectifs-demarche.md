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
