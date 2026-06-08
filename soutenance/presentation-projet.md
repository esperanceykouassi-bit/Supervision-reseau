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

### Une solution open-source pour une infrastructure toujours disponible

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
5. Axe de différenciation (innovation)
6. Étude de faisabilité & conception
7. Fonctionnement technique
8. **Démonstration**
9. Marketing, vente & concurrence
10. Prévisions financières
11. Limites & perspectives

**Conclusion**

<!-- Mon exposé suit le fil d'un projet d'entreprise : je pars du problème
du marché, je présente la solution et sa technique, je la démontre, puis
j'aborde son modèle économique avant de conclure sur les perspectives. -->

---

## Introduction — L'annonce du sujet

**Le sujet :** concevoir, réaliser et valoriser un système qui **surveille un
réseau en continu**, **détecte automatiquement les pannes** et **alerte
instantanément** les administrateurs — entièrement avec des outils open-source.

**Pourquoi ce thème ?**
- 🌐 Le réseau est devenu le **système nerveux** de toute organisation
- ⏱️ Une **minute** d'indisponibilité peut coûter très cher
- 🧑‍💻 Vécu de terrain : pannes découvertes **trop tard**, par les utilisateurs
- 💡 Conviction : l'**open-source** rend la supervision accessible à **tous**

> Allier une **expertise réseau** à une **démarche entrepreneuriale**.

<!-- J'ai choisi ce thème car il croise une réalité technique que j'ai observée
en stage - les pannes détectées trop tard - et une conviction : on peut
résoudre ce problème sans budget colossal grâce à l'open-source. C'est à la
fois un défi d'ingénieur et une opportunité de marché. -->

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

**Contexte :** densification des réseaux (cloud, virtualisation, IoT) face à des
exigences de disponibilité de plus en plus fortes (objectif « 99,9 % »).

**Constat de terrain (PME / administrations) :**
- Supervision **manuelle** et **épisodique** (`ping` à la main)
- Pannes signalées par les **utilisateurs** → réaction **tardive**
- **Aucune traçabilité** des incidents, pas d'historique exploitable
- Solutions pro jugées **trop chères** ou **trop complexes**

<!-- Le contexte est celui de réseaux toujours plus complexes et critiques.
Pourtant, sur le terrain, beaucoup de structures surveillent encore à la main.
Résultat : on apprend la panne par les plaintes, on ne garde aucune trace, et
les outils du marché paraissent inaccessibles. -->

---

## 1. La problématique — formulation claire

<!-- _class: lead -->

> ### « Comment **détecter en temps réel** les pannes d'un réseau et **réduire le temps d'intervention** des administrateurs, à l'aide d'une solution **automatisée, fiable et économiquement accessible** ? »

**Sous-questions :**
- Comment automatiser une surveillance **continue** et **fiable** (sans fausses alertes) ?
- Comment **notifier** l'administrateur **où qu'il soit**, instantanément ?
- Comment offrir cette valeur à un **coût quasi nul** ?

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

## 6. Étude de faisabilité & conception

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

## 7. Fonctionnement technique — le cycle automatisé

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

**Cible :** PME, écoles, administrations, cybercafés, hébergeurs, **MSP** (infogérants).

**Proposition de valeur :** *« Supervisez votre réseau et soyez alerté sur votre
téléphone en cas de panne — sans licence, sans complexité. »*

**Modèle économique (open-core) :**
- 🆓 **Cœur open-source gratuit** (adoption & confiance)
- 💼 **Services** : installation, formation, support (abonnement)
- ⭐ **Édition Pro** : SNMP, multi-sites, IA prédictive, rapports avancés

**Canaux :** GitHub/communauté · réseau d'infogérants · bouche-à-oreille · démo.

<!-- Côté business, je vise les structures sans gros budget IT et les
infogérants. Mon modèle est l'open-core : le cœur est gratuit pour créer
l'adoption, et je monétise les services - installation, formation, support - et
une édition Pro avec SNMP et IA. -->

---

## 9. Positionnement concurrentiel

| Critère | Nagios/Zabbix | PRTG/SolarWinds | **Notre solution** |
|---------|:-------------:|:---------------:|:------------------:|
| Prix | Gratuit mais coûteux à exploiter | **€€€** | **Gratuit + services** |
| Simplicité | Faible | Élevée | **Élevée** |
| Légèreté | Moyenne/Faible | Faible | **Très élevée** |
| Alerte mobile native | Plugin | Appli | **Telegram natif** |
| Sur-mesure / ouvert | Limité | Non | **Total** |

> **Stratégie :** ne pas affronter les géants sur le haut de gamme, mais
> **dominer le segment délaissé** des petites structures (stratégie « océan bleu »).

<!-- Je ne prétends pas battre Zabbix sur les très grandes infrastructures. Ma
stratégie est celle de l'océan bleu : occuper le segment que les géants
négligent - les petites structures - avec un produit simple, léger et gratuit. -->

---

## 10. Prévisions financières

**Coûts de mise en place (estimation) :**

| Poste | Coût |
|-------|------|
| Licences logicielles | **0 €** (100 % open-source) |
| Serveur (VM / mini-PC) | ~150–300 € (ou mutualisé) |
| Déploiement (temps) | Interne / ~1 j de prestation |
| **Total entrée** | **≈ 200 € (matériel)** |

**Modèle de revenus (scénario prestataire, an 1) :**

| Source | Hypothèse | Revenu annuel |
|--------|-----------|---------------|
| Installation+formation | 10 clients × 300 € | 3 000 € |
| Support (abonnement) | 10 clients × 40 €/mois | 4 800 € |
| Édition Pro | 3 clients × 500 € | 1 500 € |
| **Total an 1** | | **≈ 9 300 €** |

<!-- Financièrement, l'entrée est quasi nulle : pas de licence, juste un petit
serveur. Côté revenus, même avec des hypothèses prudentes - une dizaine de
clients en services - on dépasse 9 000 € la première année. Le ROI pour le
client, lui, vient de la réduction des coûts d'indisponibilité. -->

---

## 10. Retour sur investissement (côté client)

**1 heure d'indisponibilité évitée** peut représenter **des centaines à des
milliers d'euros** (perte de productivité, de chiffre d'affaires, d'image).

```
Coût solution (≈ 200 €)  ≪  Coût d'UNE panne prolongée évitée
```

> En faisant passer la détection de **~1 h à < 2 min**, la solution
> **s'autofinance dès le premier incident majeur évité**.

<!-- L'argument financier décisif pour le client : la solution coûte environ
200 €, alors qu'une seule heure de panne en coûte bien plus. En réduisant le
temps de détection d'une heure à deux minutes, elle est rentabilisée dès le
premier incident évité. -->

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

✅ Un **produit fonctionnel**, testé, **100 % open-source**
✅ Détection **temps réel** (**< 2 min**) & temps d'intervention **réduit**
✅ Un **modèle économique** viable (open-core) sur un **segment délaissé**
✅ Une **base extensible** vers l'IA et la maintenance prédictive

> ### De la supervision **réactive** vers une supervision **proactive, accessible et intelligente.**

**L'automatisation transforme la disponibilité réseau en avantage à la portée
de toutes les organisations.**

<!-- En conclusion, ce projet livre un produit réel et performant, doublé d'un
modèle économique crédible, et ouvert vers l'avenir de la supervision : le
prédictif. J'ai montré qu'on pouvait rendre la haute disponibilité accessible à
tous. -->

---

<!-- _class: lead -->

# Merci de votre attention

### Je me tiens à votre disposition pour vos questions

**[NOM Prénom]** — Master 2 RIT — 2026

<!-- Je vous remercie de votre attention et je suis prêt à répondre à toutes vos
questions, qu'elles soient techniques ou sur le volet économique du projet. -->
