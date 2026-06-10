# CHAPITRE 5 — L'AXE DE DIFFÉRENCIATION (INNOVATION TECHNOLOGIQUE)

## 5.1 Une innovation par l'assemblage

L'innovation de la solution ne réside pas dans l'invention d'un protocole
nouveau, mais dans un **assemblage différenciant** de briques éprouvées,
positionné exactement sur le besoin d'OPEN MOISE et de ses clients. Là où chaque
solution concurrente impose un compromis — gratuité *contre* complexité, ou
simplicité *contre* coût —, la solution proposée **réunit** simplicité,
gratuité, légèreté, notification mobile native et ouverture vers l'IA.

## 5.2 Les facteurs de différenciation

| Différenciateur | Bénéfice pour OPEN MOISE |
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
la solution constitue une **base de croissance** pour l'offre d'OPEN MOISE.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CHAPITRE 6 — ÉTUDE DE FAISABILITÉ ET CONCEPTION DE LA SOLUTION

## 6.1 Étude de faisabilité

### 6.1.1 Faisabilité technique

Toutes les briques retenues sont **matures, documentées et éprouvées** (Linux,
Python, MySQL, Flask). Les compétences nécessaires sont **déjà présentes** au
sein d'OPEN MOISE. La preuve de faisabilité est apportée par un **prototype
réalisé, testé et fonctionnel** (chapitres 7 et 8).

### 6.1.2 Faisabilité économique

Le coût de **licence est nul** (open-source) ; le matériel se réduit à un
**serveur léger** (machine virtuelle ou mini-serveur), éventuellement
**mutualisé** entre plusieurs clients. L'investissement initial est de l'ordre
de **130 000 FCFA** (détail au chapitre 10).

### 6.1.3 Faisabilité organisationnelle

La solution s'**intègre au processus d'astreinte** existant d'OPEN MOISE : les
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
l'**administrateur** (technicien OPEN MOISE), les **équipements** supervisés, le
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
