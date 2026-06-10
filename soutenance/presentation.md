---
marp: true
theme: default
paginate: true
header: 'Automatisation de la supervision réseau — Master 2 RIT'
footer: '© 2026'
---

<!--
SUPPORT DE SOUTENANCE (15 à 20 diapositives)
============================================
Ce fichier est au format MARP : il se convertit en PowerPoint/PDF.

  npm install -g @marp-team/marp-cli
  marp presentation.md -o presentation.pptx      # PowerPoint
  marp presentation.md -o presentation.pdf       # PDF

Chaque "---" sépare une diapositive. Les commentaires <!-- ... --> sont les
notes de l'orateur (visibles en mode présentateur, masquées à l'écran).
-->

# Mise en place d'un système d'automatisation de la supervision réseau

### basé sur des scripts et outils open-source

**[NOM Prénom]** — Master 2 RIT
Sous la direction de **[Directeur de mémoire]**
Année académique 2025–2026

<!-- Bonjour Mesdames et Messieurs les membres du jury. Je vous remercie de
votre présence. Je vais vous présenter mon travail de mémoire portant sur
l'automatisation de la supervision réseau avec des outils open-source. -->

---

## Plan de la présentation

1. Introduction & contexte
2. Problématique
3. Objectifs & hypothèses
4. État de l'art (étude de l'existant)
5. Conception du système
6. Implémentation
7. Tests & résultats
8. Recommandations & perspectives
9. Conclusion

<!-- Voici le déroulé : je commencerai par le contexte et la problématique,
puis je présenterai la conception et l'implémentation, avant de discuter les
résultats obtenus. -->

---

## 1. Introduction & contexte

- Le réseau = **système nerveux** des organisations
- Une **indisponibilité** = pertes financières + image dégradée
- Exigence croissante de **disponibilité** (99,9 %)
- Dans les PME : supervision encore **manuelle et réactive**

> La continuité de service est devenue un enjeu **stratégique**.

<!-- Aujourd'hui tout repose sur le réseau. La moindre panne coûte cher. Or
beaucoup de petites structures surveillent encore leur réseau à la main. -->

---

## 2. Problématique

**Constat :** détection des pannes par les plaintes des utilisateurs → trop tard

**Problème :** temps de détection et d'intervention élevés

**Question principale :**
> *Comment concevoir un système automatisé de supervision réseau, basé sur des
> outils open-source, permettant de détecter les pannes en temps réel et de
> réduire le temps d'intervention ?*

<!-- Le cœur du problème : on découvre les pannes trop tard, ce qui allonge le
temps d'indisponibilité. D'où ma question de recherche. -->

---

## 3. Objectifs & hypothèses

**Objectif général :** concevoir et implémenter un système automatisé de
supervision, 100 % open-source, pour détecter les pannes en temps réel.

**Hypothèses :**
- **H1** : ↓ temps de détection (MTTD)
- **H2** : ↓ temps de réaction (MTTR)
- **H3** : coût quasi nul (open-source)
- **H4** : ↑ traçabilité & disponibilité

<!-- Mon objectif est de prouver qu'on peut faire aussi bien que les solutions
payantes avec des outils gratuits. J'ai posé quatre hypothèses mesurables. -->

---

## 4. État de l'art — solutions existantes

| Solution | Licence | Limite principale |
|----------|---------|-------------------|
| Nagios | Open-source | Configuration complexe |
| Zabbix | Open-source | Gourmand en ressources |
| PRTG | Propriétaire | Payant, Windows |
| Centreon | Mixte | Modules avancés payants |
| SolarWinds | Propriétaire | Très coûteux |

→ **Espace pour une solution légère, gratuite et sur mesure pour les PME**

<!-- J'ai comparé les principales solutions. Toutes sont soit complexes, soit
payantes. Il y a donc une place pour une solution légère et personnalisable. -->

---

## 5. Conception — architecture en couches

```
PRÉSENTATION   →  Tableau de bord Flask + Bootstrap + Chart.js
TRAITEMENT     →  Moteur Python + Cron (sondes ICMP/TCP)
NOTIFICATION   →  SMTP (e-mail) + Bot Telegram (push mobile)
DONNÉES        →  Base MySQL
SYSTÈME        →  Serveur Ubuntu Linux
```

- Découplage **moteur (collecte)** / **interface (lecture)**
- Conception formalisée en **UML** (7 diagrammes) + **MERISE**

<!-- L'architecture est en cinq couches. Point clé : le moteur de collecte et
l'interface web sont découplés, ils communiquent uniquement par la base. -->

---

## 5. Conception — diagrammes UML

- Diagramme de **contexte** : 4 acteurs (admin, équipements, SMTP, Telegram)
- Cas d'utilisation, **séquence**, **activité**
- **Classes**, composants, **déploiement**

![h:330](../architecture/diagrammes/diagramme-sequence.puml)

<!-- J'ai modélisé le système avec 7 diagrammes UML. Le diagramme de séquence
montre le scénario complet de détection et d'alerte. (Remplacer par l'image
générée par PlantUML lors de la présentation.) -->

---

## 6. Implémentation — modules développés

- 🔍 **Découverte** automatique du réseau (scan CIDR parallélisé)
- 📡 **Sonde ICMP** (ping + latence)
- 🔌 **Sonde de services** TCP (HTTP, SSH, MySQL…)
- 📝 **Journalisation** avec rotation
- 🚨 **Alertes** e-mail + Telegram (avec anti-spam)
- 📊 **Tableau de bord** web temps réel

**~1500 lignes de Python commenté**, testé et fonctionnel

<!-- J'ai développé six modules en Python. La découverte est parallélisée, les
alertes sont multi-canal avec une logique anti-spam pour éviter le harcèlement
de notifications. -->

---

## 6. Implémentation — le cycle automatisé

1. **Cron** déclenche le moteur toutes les 2 min
2. Sondes ICMP/TCP sur chaque équipement
3. Mise à jour du statut + **journalisation**
4. Seuil d'échecs (anti-faux positif) → **alerte**
5. Notification **e-mail + Telegram** instantanée
6. Retour en ligne → notification de **rétablissement**

<!-- Voici le cycle : toutes les deux minutes, le système teste tout, journalise,
et alerte en cas de panne confirmée. Tout est automatique. -->

---

## 7. Tests réalisés

- **Tests unitaires** : 9/9 réussis (100 %)
- **Tests fonctionnels** : 6 scénarios validés
- **Tests de performance** : parallélisation ×10 à ×15

| Équipements | Séquentiel | Parallélisé |
|:-----------:|:----------:|:-----------:|
| 100 | ~60 s | **~7 s** |
| 254 | ~150 s | **~12 s** |

<!-- J'ai validé le système à trois niveaux. Les tests unitaires passent tous, et
la parallélisation rend le scan d'un réseau entier très rapide. -->

---

## 7. Résultats — manuel vs automatisé

| Indicateur | Manuel | **Automatisé** |
|------------|:------:|:--------------:|
| Temps de détection (MTTD) | ~30–60 min | **< 2 min** |
| Temps de réaction (MTTR) | ~45 min | **< 5 min** |
| Taux de disponibilité | ~97,5 % | **~99,5 %** |
| Coût de licence | — | **0 FCFA** |

→ **Les 4 hypothèses sont confirmées**

<!-- Voici le résultat le plus parlant : on passe d'une détection en une heure à
moins de deux minutes. Toutes mes hypothèses sont validées. -->

---

## 8. Recommandations

- VLAN d'administration dédié + IP fixe
- Onduleur (le superviseur doit survivre aux pannes)
- Sauvegarde de la base, mots de passe robustes
- Redondance pour les environnements critiques

<!-- Pour un déploiement réel, je recommande quelques bonnes pratiques,
notamment isoler le serveur et le protéger électriquement. -->

---

## 8. Perspectives

- 📈 Intégration **SNMP** (CPU, mémoire, trafic)
- 🤖 **Machine Learning** : détection d'anomalies
- 🔮 **Maintenance prédictive** (anticiper les pannes)
- ⚙️ **Auto-remédiation** (AIOps)
- 🐳 Conteneurisation (Docker / Kubernetes)

> D'une supervision **réactive** vers une supervision **prédictive**

<!-- Les perspectives sont nombreuses : l'ajout de l'IA permettrait de prédire
les pannes plutôt que de les subir. C'est l'évolution naturelle du projet. -->

---

## 9. Conclusion

- ✅ Système **fonctionnel**, 100 % open-source
- ✅ Détection **temps réel** (< 2 min)
- ✅ Temps d'intervention **réduit**
- ✅ Coût quasi **nul**
- ✅ Base **extensible** (IA, SNMP…)

**L'automatisation rend la supervision accessible aux petites structures.**

<!-- En conclusion, j'ai démontré qu'avec des outils gratuits et maîtrisés, on
construit une solution efficace et économique. -->

---

# Merci de votre attention

### Je suis à votre disposition pour vos questions

**[NOM Prénom]** — Master 2 RIT

<!-- Je vous remercie de votre attention et je suis prêt à répondre à vos
questions. -->
