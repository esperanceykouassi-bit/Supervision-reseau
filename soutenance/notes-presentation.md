# Notes de présentation (script de l'orateur)

Durée cible : **12 à 15 minutes** d'exposé + 10 à 15 minutes de questions.
Conseil de rythme : ~45 secondes à 1 minute par diapositive.

---

### Diapo 1 — Page de titre (30 s)
« Bonjour Mesdames et Messieurs les membres du jury. Je vous remercie de votre
présence. Je m'appelle [Nom] et je vais vous présenter mon travail de mémoire
intitulé *Mise en place d'un système d'automatisation de la supervision réseau
basé sur des scripts et outils open-source*, réalisé sous la direction de [Nom]. »

### Diapo 2 — Plan (30 s)
« Ma présentation suivra neuf points : du contexte et de la problématique jusqu'à
la conclusion, en passant par la conception, l'implémentation et les résultats. »

### Diapo 3 — Contexte (1 min)
« Le réseau est aujourd'hui le système nerveux des organisations. Une panne, même
courte, coûte cher. Pourtant, dans beaucoup de PME, la supervision reste manuelle
et réactive : on découvre les pannes par les plaintes des utilisateurs. »

### Diapo 4 — Problématique (1 min)
« Le constat est simple : la détection est trop tardive, ce qui allonge le temps
d'indisponibilité. Ma question de recherche est donc : comment automatiser la
supervision avec des outils open-source pour détecter les pannes en temps réel et
réduire le temps d'intervention ? »

### Diapo 5 — Objectifs & hypothèses (1 min)
« Mon objectif : concevoir un système 100 % open-source de détection en temps
réel. J'ai formulé quatre hypothèses mesurables, autour de la réduction du temps
de détection, du temps de réaction, du coût et de l'amélioration de la
disponibilité. »

### Diapo 6 — État de l'art (1 min 30)
« J'ai comparé cinq solutions de référence. Toutes sont remarquables, mais soit
complexes et gourmandes — Nagios, Zabbix —, soit propriétaires et coûteuses —
PRTG, SolarWinds. Il existe donc un espace pour une solution légère, gratuite et
sur mesure, adaptée aux petites structures. C'est ce que je propose. »

### Diapo 7 — Architecture (1 min 30)
« Mon architecture s'organise en cinq couches, de l'OS Ubuntu jusqu'au tableau de
bord web. Un point de conception important : le moteur de collecte et l'interface
web sont **découplés** ; ils ne communiquent que via la base de données. Ainsi, la
collecte continue même si l'interface est arrêtée. J'ai tout formalisé en UML et
MERISE. »

### Diapo 8 — UML (1 min)
« J'ai produit sept diagrammes UML. Celui-ci, le diagramme de séquence, illustre
le scénario complet : Cron déclenche le moteur, les sondes testent les
équipements, et en cas de panne, l'alerte part par e-mail et Telegram. »

### Diapo 9 — Modules (1 min 30)
« J'ai développé six modules en Python : la découverte automatique du réseau, la
sonde ICMP, la sonde de services TCP, la journalisation, les alertes multi-canal,
et le tableau de bord. Environ 1500 lignes de code commenté, testé et
fonctionnel. »

### Diapo 10 — Cycle automatisé (1 min)
« Concrètement, toutes les deux minutes, Cron lance le moteur qui teste tous les
équipements, journalise, et — après confirmation par un seuil d'échecs pour
éviter les fausses alertes — déclenche une notification instantanée. »

### Diapo 11 — Tests (1 min)
« J'ai validé à trois niveaux. Mes neuf tests unitaires passent à 100 %. Les
scénarios fonctionnels sont validés. Et grâce à la parallélisation, le scan d'un
réseau de 254 machines passe de 150 secondes à 12 secondes. »

### Diapo 12 — Résultats (1 min 30) — **DIAPO CLÉ**
« Voici le résultat le plus parlant. Le temps de détection passe d'environ une
heure à moins de deux minutes. Le temps de réaction chute également grâce aux
notifications Telegram. La disponibilité estimée progresse, et le coût de licence
est nul. Mes quatre hypothèses sont donc confirmées. »

### Diapo 13 — Recommandations (45 s)
« Pour un déploiement réel, je recommande d'isoler le serveur sur un VLAN dédié,
de le protéger par un onduleur et de sauvegarder la base régulièrement. »

### Diapo 14 — Perspectives (1 min)
« Le système est une base extensible. Les perspectives les plus prometteuses sont
l'ajout de SNMP et surtout l'intégration du Machine Learning pour passer d'une
supervision réactive à une supervision prédictive, capable d'anticiper les
pannes. »

### Diapo 15 — Conclusion (1 min)
« En conclusion, j'ai démontré qu'avec des outils gratuits et maîtrisés, on bâtit
une solution efficace, économique et accessible aux petites structures, qui
réduit drastiquement le temps de détection et d'intervention. »

### Diapo 16 — Remerciements (15 s)
« Je vous remercie de votre attention et je me tiens à votre disposition pour
répondre à vos questions. »

---

## Check-list avant la soutenance

- [ ] Tester la **démonstration live** (réseau, alerte Telegram qui arrive).
- [ ] Générer les **images PlantUML** et les insérer dans les diapos.
- [ ] Insérer les **captures d'écran** réelles du tableau de bord.
- [ ] Prévoir un **plan B** (vidéo/captures) si la démo live échoue.
- [ ] Relire les **questions probables du jury**.
- [ ] Vérifier la **durée** en répétant à voix haute (chronomètre).
- [ ] Préparer une **copie PDF** du support en cas de souci technique.
