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

Pour un déploiement en production chez OPEN MOISE, nous recommandons de :

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
aussi la feuille de route commerciale d'OPEN MOISE, sont :

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
l'entreprise **OPEN MOISE** : **détecter en temps réel les pannes des réseaux
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
prolonger les travaux futurs, au service de la compétitivité d'OPEN MOISE et de
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
