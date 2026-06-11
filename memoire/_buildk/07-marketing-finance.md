# CHAPITRE 9 — MARKETING, VENTE ET CONCURRENCE

## 9.1 Une double valeur

La solution présente une **double valeur** pour toute organisation — ou pour un prestataire de services :

1. **Outil interne** : elle industrialise la supervision des parcs déjà gérés,
   fiabilise le respect des **SLA**, réduit la charge d'astreinte et renforce la
   relation de confiance avec les clients existants ;
2. **Nouvelle offre commerciale** : elle devient un **service de supervision
   managée** facturable, que l'entreprise peut proposer à l'ensemble de son
   portefeuille et à de nouveaux prospects.

## 9.2 Segmentation et cible

Le marché visé est celui des organisations ne disposant pas d'une équipe
informatique étoffée, mais dépendantes de leur réseau :

- **PME et commerces** (agences, cabinets, distribution) ;
- **Établissements** (écoles, cliniques, hôtels) ;
- **Administrations et collectivités** ;
- **Hébergeurs, cybercafés et autres ESN** partenaires.

## 9.3 Proposition de valeur

> *« Nous surveillons votre réseau 24h/24 et intervient avant que vous ne
> constatiez la panne — sans licence, sans matériel coûteux. »*

Cette proposition transforme un **centre de coût** (la maintenance réactive) en
un **service à valeur ajoutée**, proactif et contractualisé.

## 9.4 Modèle économique (open-core et service managé)

| Composante | Description | Mode de revenu |
|------------|-------------|----------------|
| Cœur open-source | Le moteur et le tableau de bord, gratuits | Adoption / confiance |
| Mise en service | Installation, paramétrage, formation chez le client | Forfait unique |
| Supervision managée | Surveillance continue + astreinte | **Abonnement mensuel** |
| Option « Pro » | SNMP, multi-sites, IA prédictive, rapports SLA avancés | Supplément |

## 9.5 Positionnement concurrentiel

| Critère | Nagios/Zabbix | PRTG/SolarWinds | **Solution proposée** |
|---------|:-------------:|:---------------:|:--------------------:|
| Prix | Gratuit mais coûteux à exploiter | Très coûteux | **Gratuit + services** |
| Simplicité | Faible | Élevée | **Élevée** |
| Légèreté | Moyenne / faible | Faible | **Très élevée** |
| Alerte mobile native | Plugin | Application | **Telegram natif** |
| Sur-mesure / ouvert | Limité | Non | **Total** |

**Stratégie « océan bleu » :** plutôt que d'affronter les géants sur le segment
des grandes infrastructures, la solution se **différencie auprès des PME** avec
une offre **simple, sans licence et au prix du marché local**, là où les
solutions internationales sont trop chères ou trop lourdes.

## 9.6 Plan d'action commercial

1. **Déployer** la solution en interne et l'**éprouver** sur les clients
   existants (preuve par l'usage) ;
2. **Packager** l'offre de supervision managée (niveaux de service et tarifs) ;
3. **Communiquer** : démonstrations, témoignages clients, présence en ligne ;
4. **Convertir** progressivement le portefeuille existant à l'abonnement ;
5. **Prospecter** de nouveaux clients sur la base des résultats mesurés.

## 9.7 Analyse SWOT de l'offre

| Forces (Strengths) | Faiblesses (Weaknesses) |
|--------------------|--------------------------|
| Coût nul de licence, marge élevée | Dépend des compétences internes (clé de l'humain) |
| Notification mobile native (Telegram) | Pas encore de métriques SNMP / IA |
| Solution maîtrisée et personnalisable | Notoriété de l'offre à construire |
| Déploiement rapide (« plug & supervise ») | Serveur de supervision à sécuriser/redonder |

| Opportunités (Opportunities) | Menaces (Threats) |
|------------------------------|--------------------|
| Forte demande PME (digitalisation, mobile money) | Concurrence des grands éditeurs |
| Évolution vers la maintenance prédictive (IA) | Solutions cloud SaaS low-cost |
| Élargissement du portefeuille existant | Exigence croissante des SLA clients |
| Partenariats avec d'autres ESN locales | Dépendance à la connectivité Internet |

Cette analyse confirme que les **forces** et les **opportunités** l'emportent :
l'offre s'appuie sur un avantage de coût structurel et répond à une demande
croissante, tandis que les faiblesses identifiées correspondent précisément aux
**perspectives** d'évolution (chapitre 11).

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# CHAPITRE 10 — PRÉVISIONS FINANCIÈRES

> *Montants exprimés en francs CFA (XOF). Parité fixe de référence : 1 € =
> 655,957 FCFA. Les hypothèses sont indicatives et à ajuster aux prix réellement
> pratiqués sur le marché ivoirien.*

## 10.1 Investissement initial

| Poste | Coût (FCFA) |
|-------|-------------|
| Licences logicielles | **0** (100 % open-source) |
| Serveur / VM (mutualisable) | 100 000 – 200 000 |
| Développement et déploiement | Interne (déjà réalisé) |
| **Total d'entrée** | **≈ 130 000 FCFA** |

L'investissement est **quasi nul** : absence de licence, matériel léger et
mutualisable, développement réalisé en interne dans le cadre de ce projet.

## 10.2 Revenus et gains prévisionnels (année 1)

| Source | Hypothèse | Montant (FCFA) |
|--------|-----------|----------------|
| Supervision managée | 10 clients × 25 000 FCFA/mois | 3 000 000 |
| Mise en service | 10 × 200 000 FCFA | 2 000 000 |
| Option « Pro » (SNMP/IA) | 3 × 325 000 FCFA | 975 000 |
| Pénalités SLA évitées | estimation | gain additionnel |
| **Total année 1** | | **≈ 6 000 000 FCFA** |

## 10.3 Analyse de rentabilité et seuil critique

Le **seuil de rentabilité** est atteint extrêmement tôt : l'investissement
d'entrée (**≈ 130 000 FCFA**) est couvert dès le **premier mois** d'abonnement
d'un seul client (25 000 FCFA/mois) cumulé à sa mise en service (200 000 FCFA).
Autrement dit, **un seul client** suffit à rentabiliser le projet.

Au-delà, chaque client supplémentaire en supervision managée génère un **revenu
récurrent** de l'ordre de **300 000 FCFA par an** (25 000 × 12), pour un coût
marginal d'exploitation très faible (le serveur étant mutualisé). La marge est
donc **élevée et croissante** avec le nombre de clients.

## 10.4 Gains internes (économies)

Outre les revenus, la solution génère des **économies
internes** :

- **Réduction du temps d'astreinte** consacré à la détection manuelle ;
- **Diminution des pénalités SLA** grâce à une détection et une intervention
  plus rapides ;
- **Préservation de l'image** et **fidélisation** des clients, donc réduction du
  coût de renouvellement du portefeuille.

## 10.5 Synthèse financière

| Indicateur | Valeur |
|------------|--------|
| Investissement initial | ≈ 130 000 FCFA |
| Revenus prévisionnels année 1 | ≈ 6 000 000 FCFA |
| Coût de licence | 0 FCFA |
| Seuil de rentabilité | **≈ 1 client** |

Le projet présente ainsi un **rapport bénéfice/coût très favorable** : un
investissement marginal pour des revenus récurrents et des économies internes
substantielles.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
