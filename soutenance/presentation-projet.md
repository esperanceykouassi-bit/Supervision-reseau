---
marp: true
theme: gaia
paginate: true
backgroundColor: #fff
color: #1a1a2e
header: 'Automatisation de la Supervision et de la Détection des Pannes Réseau'
footer: 'Soutenance Mémoire-Projet — Master 2 RIT — 2026'
style: |
  section { font-size: 26px; }
  h1 { color: #0d3b66; }
  h2 { color: #0d6efd; border-bottom: 3px solid #0d6efd; padding-bottom: 6px; }
  table { font-size: 22px; }
  strong { color: #d62828; }
  section.lead h1 { font-size: 46px; text-align: center; }
  section.lead { text-align: center; }
---

<!--
============================================================================
SUPPORT DE SOUTENANCE — FORMAT MÉMOIRE-PROJET (CANEVAS ENTREPRENEURIAL)
============================================================================
Format MARP -> conversion PowerPoint / PDF :
    npm install -g @marp-team/marp-cli
    marp presentation-projet.md -o presentation-projet.pptx
    marp presentation-projet.md -o presentation-projet.pdf

Les blocs <!-- ... --> sous chaque diapo = NOTES DE L'ORATEUR
(visibles en mode présentateur, masquées à l'écran).
Durée cible : 15-20 min d'exposé + questions.
============================================================================
-->

<!-- _class: lead -->

# Automatisation de la Supervision et de la Détection des Pannes Réseau

### Une solution open-source déployée au sein d'OPEN MOISE (ESN d'infogérance)

**[NOM Prénom]** — Master 2 RIT
Sous la direction de **[Directeur de mémoire]**
Structure d'accueil : **OPEN MOISE** — Année académique 2025–2026

<!-- Bonjour Mesdames et Messieurs les membres du jury. Je vous remercie de
votre présence. Je vais vous présenter mon mémoire-projet : une solution
d'automatisation de la supervision et de la détection des pannes réseau,
pensée comme un véritable produit, du besoin du marché jusqu'au modèle
économique. -->

---

<!-- _class: lead -->

## Plan de la présentation

**Introduction** — L'annonce du sujet

1. Contexte et identification du problème
2. Objectifs et résultats attendus
3. Démarche méthodologique
4. État des lieux & solution proposée
5. L'axe de différenciation (innovation technologique)
6. Étude de faisabilité & conception
7. Fonctionnement de la solution : point de vue technique
8. **Démonstration**
9. Marketing, vente et concurrence
10. Prévisions financières
11. Limites & perspectives

**Conclusion**

<!-- Mon exposé suit le fil d'un projet d'entreprise : je pars du problème
du marché, je présente la solution et sa technique, je la démontre, puis
j'aborde son modèle économique avant de conclure sur les perspectives. -->

---

## Introduction — L'annonce du sujet

**Le sujet :** concevoir, réaliser et déployer **chez OPEN MOISE** un système qui
**surveille en continu les réseaux supervisés**, **détecte automatiquement les
pannes** et **alerte instantanément** les équipes — entièrement open-source.

**Pourquoi ce thème ?**
- 🌐 Le réseau est le **système nerveux** des clients d'OPEN MOISE
- ⏱️ Une **minute** d'indisponibilité menace les engagements de service (**SLA**)
- 🧑‍💻 Vécu de terrain chez OPEN MOISE : pannes des parcs clients découvertes
  **trop tard**, souvent signalées par le client
- 💡 Conviction : l'**open-source** permet d'**industrialiser** la supervision sans licence

> Répondre à un besoin réel d'**OPEN MOISE** en alliant expertise réseau et
> démarche entrepreneuriale.

<!-- J'ai choisi ce thème car il croise une réalité observée chez OPEN MOISE -
les pannes des réseaux clients détectées trop tard - et une conviction : on peut
industrialiser la supervision sans budget colossal grâce à l'open-source. -->

---

## Présentation de la structure d'accueil — OPEN MOISE

**OPEN MOISE** — Entreprise de Services du Numérique (**ESN**)

- 🏢 Activités : **infogérance**, intégration réseau & systèmes, développement, cybersécurité
- 🎯 Mission : garantir aux clients un SI **performant, disponible et sécurisé**
- 👥 [Effectif] collaborateurs · implantée à [ville] · depuis [année]
- 🧩 Projet mené au sein du **[Pôle Infrastructures & Supervision]**

> En tant qu'ESN qui **supervise les réseaux de ses clients**, OPEN MOISE est
> directement concernée : ce projet est un **outil interne stratégique** pour
> tenir ses engagements de service (**SLA**) et maîtriser ses coûts.

<!-- Quelques mots sur mon entreprise d'accueil, OPEN MOISE. C'est une ESN qui
assure notamment l'infogérance et la supervision des réseaux de ses clients.
Mon projet répond donc à un besoin direct de l'entreprise : détecter plus vite
les pannes des parcs qu'elle exploite et respecter ses engagements de service. -->

---

## 1. Contexte et identification du problème

**Contexte :** OPEN MOISE, **ESN d'infogérance**, exploite et supervise les
réseaux de plusieurs clients sous **engagements contractuels** (SLA, « 99,9 % »).

**Constat de terrain chez OPEN MOISE :**
- Supervision largement **manuelle** et **épisodique** (`ping` à la main)
- Pannes des parcs clients signalées **par le client** → réaction **tardive**
- **Aucune traçabilité** des incidents → **SLA difficiles à prouver**
- Solutions du marché jugées **trop chères** ou **trop lourdes** à déployer

<!-- Le contexte est celui d'OPEN MOISE : une ESN qui supervise les réseaux de
ses clients sous engagement de service. Or cette supervision est encore largement
manuelle. Résultat : on apprend la panne par le client lui-même, sans trace
exploitable, ce qui met en péril le respect des SLA. -->

---

## 1. La problématique — formulation claire

<!-- _class: lead -->

> ### « Comment **OPEN MOISE** peut-elle **détecter en temps réel** les pannes des réseaux qu'elle supervise et **réduire le temps d'intervention** de ses équipes, à l'aide d'une solution **automatisée, fiable et économiquement accessible** ? »

**Sous-questions :**
- Comment automatiser une surveillance **continue** et **fiable** des parcs clients ?
- Comment **alerter les équipes d'astreinte** d'OPEN MOISE, **où qu'elles soient** ?
- Comment offrir cette valeur **sans alourdir les coûts** d'OPEN MOISE ?

<!-- Tout le projet répond à cette question centrale, que je formule clairement :
détecter en temps réel et réduire le temps d'intervention, avec une solution
automatisée, fiable ET accessible financièrement. Les trois sous-questions
guident ma conception. -->

---

## 2. Objectifs et résultats attendus

| Objectif | Résultat attendu (indicateur) |
|----------|-------------------------------|
| Détecter les pannes en temps réel | **MTTD < 2 min** (vs ~60 min) |
| Alerter instantanément | **MTTR < 5 min** (vs ~45 min) |
| Automatiser la surveillance | **0 intervention humaine** sur la collecte |
| Assurer la traçabilité | **100 %** des événements journalisés |
| Améliorer la disponibilité | **+2 pts** (≈97,5 % → ≈99,5 %) |
| Maîtriser le coût | **0 €** de licence (open-source) |

> **Objectif général :** livrer un produit fonctionnel, mesurablement plus
> performant que la supervision manuelle, pour un coût négligeable.

<!-- Mes objectifs sont chiffrés et donc vérifiables. Le cœur : faire chuter le
temps de détection de l'ordre de l'heure à moins de deux minutes, et le temps
de réaction à moins de cinq minutes, le tout sans coût de licence. -->

---

## 3. Démarche méthodologique

**Type :** recherche **appliquée / expérimentale** — paradigme *Design Science*
(on conçoit un artefact et on en **mesure** l'efficacité).

**Cycle de travail (itératif, inspiré DevOps) :**

```
Analyse → Conception (UML/MERISE) → Développement → Test → Intégration → Mesure
   ↑___________________________ itération ___________________________↓
```

**Outils & livrables :** recherche documentaire · observation terrain ·
prototypage · **collecte automatisée des métriques** (journaux) ·
comparaison **avant/après** (manuel vs automatisé).

<!-- Ma démarche est celle de l'ingénieur-chercheur : je conçois un système réel
et je prouve sa valeur par la mesure. J'ai travaillé en cycles itératifs, à la
DevOps, et j'évalue par comparaison avant/après sur des indicateurs objectifs. -->

---

## 4. État des lieux des solutions existantes

| Solution | Type | Atout | Frein majeur |
|----------|------|-------|--------------|
| **Nagios** | Open-source | Éprouvé, extensible | Config. complexe |
| **Zabbix** | Open-source | Très complet | Gourmand en ressources |
| **Centreon** | Mixte | Interface soignée | Modules avancés payants |
| **PRTG** | Propriétaire | Simple | Payant, Windows |
| **SolarWinds** | Propriétaire | Haut de gamme | **Très coûteux** |

**Le vide identifié :** rien de **léger + gratuit + simple + sur mesure** avec
**notification mobile native** pour les **petites structures**.

<!-- J'ai analysé les références du marché. Le constat : ce sont soit des usines
à gaz puissantes mais complexes, soit des produits simples mais propriétaires et
chers. Il existe un vide pour une solution légère, gratuite et sur mesure. -->

---

## 4. Solution proposée

Un système **automatisé**, **modulaire** et **100 % open-source** qui :

- 🔍 **découvre** automatiquement les équipements du réseau
- 📡 **sonde** en continu disponibilité (ICMP) et services (TCP)
- 🧠 **confirme** la panne (anti-faux positif) et **journalise** tout
- 🚨 **alerte** en temps réel par **e-mail** ET **Telegram** (push mobile)
- 📊 offre un **tableau de bord web** temps réel + rapports

**Stack :** Ubuntu · Python · Cron · MySQL · Flask · Bootstrap · Bot Telegram

<!-- Ma réponse à ce vide : une solution complète mais légère. Elle découvre,
surveille, confirme, journalise, alerte et affiche - le tout assemblé à partir
de briques open-source éprouvées. -->

---

## 5. Axe de différenciation (innovation technologique)

**Ce qui rend la solution unique :**

| Différenciateur | Bénéfice client |
|-----------------|-----------------|
| 📱 **Alerte Telegram native** | Notification *push* gratuite, l'admin alerté **partout** |
| 🪶 **Ultra-légère** | Tourne sur un mini-serveur / VM 1 vCPU |
| 🧩 **Code 100 % maîtrisé & ouvert** | Personnalisation **totale**, zéro *vendor lock-in* |
| ⚙️ **« Plug & supervise »** | Découverte auto. + déploiement en < 30 min |
| 🤖 **Prête pour l'IA** | Historique structuré → maintenance **prédictive** |

> **L'innovation n'est pas une brique isolée, mais l'ASSEMBLAGE** : simplicité +
> gratuité + notification mobile + extensibilité IA, là où les autres imposent
> un compromis.

<!-- Mon innovation ne réside pas dans l'invention d'un protocole, mais dans un
positionnement unique : combiner simplicité, gratuité, alerte mobile instantanée
et ouverture vers l'IA. Là où chaque concurrent impose un sacrifice, ma solution
réunit ces atouts. La notification Telegram native est mon vrai marqueur. -->

---

## 6. Étude de faisabilité et conception de la solution

**Faisabilité technique** ✅ — briques matures (Linux, Python, MySQL), compétences
maîtrisées, prototype **réalisé et testé**.
**Faisabilité économique** ✅ — coût de licence **nul**, matériel minimal.
**Faisabilité organisationnelle** ✅ — déploiement et prise en main rapides.

**Conception formalisée :**
- **UML** : 7 diagrammes (contexte, cas d'usage, séquence, activité, classes, composants, déploiement)
- **MERISE** : MCD → MLD → base MySQL (équipements, journaux, alertes, utilisateurs, statistiques)
- **Architecture en 5 couches** : Système → Données → Traitement → Notification → Présentation

<!-- Le projet est faisable sur les trois plans : technique - le prototype existe
et fonctionne -, économique - coût quasi nul - et organisationnel - déploiement
rapide. J'ai rigoureusement conçu le système en UML et MERISE, sur une
architecture claire en cinq couches. -->

---

## 6. Architecture de la solution

```
┌────────────────────────────────────────────────────────┐
│ PRÉSENTATION  Tableau de bord Flask + Bootstrap + Chart │
├────────────────────────────────────────────────────────┤
│ NOTIFICATION  E-mail (SMTP)  +  Telegram (push mobile)  │
├────────────────────────────────────────────────────────┤
│ TRAITEMENT    Moteur Python + Cron (sondes ICMP / TCP)  │
├────────────────────────────────────────────────────────┤
│ DONNÉES       Base MySQL (historique, alertes, config)  │
├────────────────────────────────────────────────────────┤
│ SYSTÈME       Serveur Linux Ubuntu                      │
└────────────────────────────────────────────────────────┘
```

**Choix clé :** **découplage** moteur de collecte (Cron) ↔ interface (Flask)
→ la surveillance continue même si le tableau de bord est arrêté.

<!-- Voici l'architecture en cinq couches. Le choix d'ingénierie le plus
important est le découplage entre la collecte et l'affichage : ils communiquent
uniquement par la base, ce qui rend le système robuste. -->

---

## 7. Fonctionnement de la solution : point de vue technique

```
  ┌──────────┐   toutes les 2 min   ┌──────────────┐
  │   CRON   │ ───────────────────► │  supervisor  │
  └──────────┘                      └──────┬───────┘
                          1. charge les équipements (MySQL)
                          2. sonde ICMP (ping) + TCP (service)
                          3. met à jour le statut + journalise
                          4. seuil d'échecs ? (anti-faux positif)
                                     │ oui
                          5. ┌───────▼─────── anti-spam ──────┐
                             │  ALERTE  e-mail  +  Telegram    │
                             └─────────────────────────────────┘
                          6. retour UP → notif. de rétablissement
```

**Robustesse :** seuil d'échecs (pas de fausse alerte), dé-duplication (pas de
spam), sondes parallélisées (scan d'un /24 en ~12 s), journaux à rotation.

<!-- Techniquement : toutes les deux minutes, Cron lance le moteur qui teste
chaque équipement. Une panne n'est confirmée qu'après plusieurs échecs - pour
éviter les fausses alertes - et une seule notification est envoyée par panne.
Tout est parallélisé pour rester rapide même sur un grand réseau. -->

---

## 7. Sécurité « by design »

| Risque | Parade implémentée |
|--------|--------------------|
| Secrets dans le code | Variables d'**environnement** (`.env` non versionné) |
| Vol de mots de passe | **Hachage** pbkdf2:sha256 (jamais en clair) |
| Injection SQL | Requêtes **paramétrées** systématiques |
| Écoute des notifications | **SMTP STARTTLS** + Telegram **HTTPS** |
| Accès BDD trop large | Compte applicatif au **moindre privilège** |
| Accès non autorisé | **Authentification** du tableau de bord |

<!-- La sécurité a été pensée dès la conception, pas ajoutée après : secrets
hors du code, mots de passe hachés, requêtes paramétrées contre l'injection SQL,
communications chiffrées et moindre privilège sur la base. -->

---

## 8. Démonstration — scénario en direct

**Déroulé proposé au jury (≈ 3 min) :**

1. 🖥️ **Tableau de bord** — vue temps réel : équipements **UP**, KPI, graphiques
2. 🔌 **Je débranche / éteins** un équipement supervisé
3. ⏱️ Au cycle suivant → statut bascule en **DOWN** (badge rouge)
4. 📧📱 **L'alerte arrive** : e-mail **+ notification Telegram** sur le téléphone
5. ✅ Je **rallume** → notification de **rétablissement** + acquittement auto
6. 📊 **Page Rapports** : historique, taux de disponibilité, latences

> *Plan B : captures d'écran + courte vidéo si la démo live est impossible.*

<!-- Pour la démonstration, je propose un scénario vivant : je montre le tableau
de bord, j'éteins un équipement devant vous, et vous verrez l'alerte Telegram
arriver sur mon téléphone en temps réel. Puis je le rallume pour montrer le
rétablissement automatique. J'ai un plan B en captures et vidéo. -->

---

## 8. Démonstration — captures clés

> *Insérer ici les captures réelles :*

| Écran | Ce qu'il prouve |
|-------|-----------------|
| 🔐 Connexion | Accès sécurisé |
| 📊 Tableau de bord | Supervision temps réel, KPI, anneau de disponibilité |
| 🖧 Équipements | Inventaire + découverte automatique |
| 🔔 Alertes | Historique + acquittement |
| 📱 Notification Telegram | Alerte push reçue sur smartphone |
| 📈 Rapports | Statistiques & graphiques exportables |

<!-- Ces captures matérialisent chaque fonctionnalité clé. La plus parlante est
la notification Telegram reçue sur le téléphone : c'est la preuve concrète de la
valeur ajoutée pour l'administrateur. -->

---

## 9. Marketing, vente et concurrence

**Double valeur pour OPEN MOISE :**
- 🛠️ **Outil interne** : industrialise la supervision, fiabilise les **SLA**, réduit l'astreinte
- 💼 **Nouvelle offre** : **« Supervision managée »** vendue aux clients d'OPEN MOISE

**Proposition de valeur d'OPEN MOISE à ses clients :** *« OPEN MOISE surveille
votre réseau 24/7 et intervient avant que vous ne constatiez la panne. »*

**Monétisation :**
- 📅 **Abonnement** mensuel de supervision managée (par site / par équipement)
- ⭐ **Option Pro** : SNMP, multi-sites, IA prédictive, rapports SLA avancés

<!-- Pour OPEN MOISE, la solution a une double valeur : en interne, elle
industrialise la supervision et fiabilise les SLA ; en externe, elle devient une
nouvelle offre de supervision managée facturée aux clients. C'est à la fois une
économie et une source de revenus récurrents. -->

---

## 9. Positionnement concurrentiel

| Critère | Nagios/Zabbix | PRTG/SolarWinds | **Solution OPEN MOISE** |
|---------|:-------------:|:---------------:|:------------------:|
| Prix | Gratuit mais coûteux à exploiter | **€€€** | **Gratuit + services** |
| Simplicité | Faible | Élevée | **Élevée** |
| Légèreté | Moyenne/Faible | Faible | **Très élevée** |
| Alerte mobile native | Plugin | Appli | **Telegram natif** |
| Sur-mesure / ouvert | Limité | Non | **Total** |

> **Stratégie d'OPEN MOISE :** ne pas affronter les géants sur le haut de gamme,
> mais **se différencier sur le segment des PME** avec une offre managée simple
> et sans licence (stratégie « océan bleu »).

<!-- Je ne prétends pas battre Zabbix sur les très grandes infrastructures. Ma
stratégie est celle de l'océan bleu : occuper le segment que les géants
négligent - les petites structures - avec un produit simple, léger et gratuit. -->

---

## 10. Prévisions financières (OPEN MOISE)

**Investissement d'OPEN MOISE :**

| Poste | Coût |
|-------|------|
| Licences logicielles | **0 €** (100 % open-source) |
| Serveur / VM (mutualisé) | ~150–300 € |
| Développement & déploiement | Interne (déjà réalisé) |
| **Total d'entrée** | **≈ 200 €** |

**Revenus & gains pour OPEN MOISE (an 1) :**

| Source | Hypothèse | Montant |
|--------|-----------|---------|
| Supervision managée | 10 clients × 40 €/mois | 4 800 € |
| Mise en service client | 10 × 300 € | 3 000 € |
| Option Pro (SNMP/IA) | 3 × 500 € | 1 500 € |
| Pénalités SLA évitées | estimation | + gains |
| **Total an 1** | | **≈ 9 300 €** |

<!-- Pour OPEN MOISE, l'investissement est quasi nul : pas de licence, un serveur
mutualisé, un développement déjà réalisé en interne. Le retour est double :
revenus récurrents via l'offre managée, et économies internes. -->

---

## 10. Double retour pour OPEN MOISE

**1 heure d'indisponibilité client évitée** = pénalités **SLA** évitées + image
préservée + fidélisation du client.

```
Investissement OPEN MOISE (≈ 200 €)  ≪  Revenus récurrents + pénalités SLA évitées
```

> Détection ramenée de **~1 h à < 2 min** → OPEN MOISE **tient ses SLA**,
> **réduit son astreinte** et **facture une nouvelle offre** : l'investissement
> est **amorti dès le premier client**.

<!-- L'argument décisif pour OPEN MOISE : un investissement d'environ 200 € qui
génère des revenus récurrents et évite des pénalités SLA. La solution est
rentabilisée dès le premier client de l'offre managée. -->

---

## 11. Limites du projet et perspectives

**Limites assumées :**
- Supervision active → pas de métriques internes (CPU/RAM) sans **SNMP**
- Réactivité **bornée** par l'intervalle de cycle (2 min)
- Alertes dépendantes de la **connectivité sortante**
- « Qui surveille le surveillant ? » → besoin de **redondance**

**Perspectives :**
- 📈 Intégration **SNMP** (performances détaillées)
- 🤖 **Machine Learning** : détection d'anomalies
- 🔮 **Maintenance prédictive** (anticiper la panne)
- ⚙️ **Auto-remédiation** (AIOps) · 🐳 Conteneurisation (Docker/K8s)
- 📲 Canaux additionnels (SMS, Slack, Teams)

<!-- Je reste lucide sur les limites : pas encore de SNMP, réactivité bornée à
deux minutes, et la question du superviseur lui-même. Mais ces limites tracent
ma feuille de route : SNMP, puis l'IA pour passer d'une supervision réactive à
une supervision prédictive qui anticipe les pannes. -->

---

## Conclusion

✅ Pour **OPEN MOISE** : un outil **fonctionnel**, testé, **100 % open-source**
✅ Détection **temps réel** (**< 2 min**) → **SLA clients** mieux respectés
✅ **Double valeur** : économies internes + nouvelle **offre managée**
✅ Une **base extensible** vers l'IA et la maintenance prédictive

> ### Pour OPEN MOISE, l'automatisation transforme la supervision en **avantage concurrentiel** : de la réaction subie vers un **service proactif, fiable et rentable**.

<!-- En conclusion, ce projet dote OPEN MOISE d'un outil réel et performant, qui
fiabilise ses engagements de service, génère des économies et ouvre une nouvelle
offre commerciale. Pour l'entreprise, c'est un avantage concurrentiel concret. -->

---

<!-- _class: lead -->

# Merci de votre attention

### Je me tiens à votre disposition pour vos questions

**[NOM Prénom]** — Master 2 RIT — 2026

<!-- Je vous remercie de votre attention et je suis prêt à répondre à toutes vos
questions, qu'elles soient techniques ou sur le volet économique du projet. -->
