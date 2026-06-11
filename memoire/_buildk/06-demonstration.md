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
