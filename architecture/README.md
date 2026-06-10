# Dossier Architecture

Ce dossier regroupe **toute la documentation de conception** du système
d'automatisation de la supervision réseau : diagrammes UML, schéma
d'architecture technique et schéma d'architecture réseau.

## Contenu

| Fichier | Description |
|---------|-------------|
| `architecture-technique.md` | Description détaillée de la pile technologique (Ubuntu, Python, Cron, MySQL, SMTP, Telegram, Flask) et justification des choix. |
| `schema-architecture-reseau.md` | Schéma de déploiement réseau (topologie, placement du serveur de supervision, flux). |
| `diagrammes/diagramme-contexte.md` | Diagramme de contexte (vision système / acteurs). |
| `diagrammes/cas-utilisation.puml` | Diagramme de cas d'utilisation UML. |
| `diagrammes/diagramme-sequence.puml` | Diagramme de séquence UML (cycle de détection et d'alerte). |
| `diagrammes/diagramme-activite.puml` | Diagramme d'activité UML (logique du moteur). |
| `diagrammes/diagramme-classes.puml` | Diagramme de classes UML. |
| `diagrammes/diagramme-composants.puml` | Diagramme de composants UML. |
| `diagrammes/diagramme-deploiement.puml` | Diagramme de déploiement UML. |

## Comment générer les images des diagrammes

Les diagrammes UML sont écrits en **PlantUML** (format texte, versionnable).
Pour produire les images PNG/SVG :

```bash
# Installation
sudo apt install plantuml          # ou : télécharger plantuml.jar

# Génération de tous les diagrammes
plantuml diagrammes/*.puml         # produit les .png à côté des .puml
```

Les diagrammes de contexte et le schéma réseau utilisent **Mermaid**
(rendu nativement par GitHub/GitLab et la plupart des éditeurs Markdown).

## Galerie des diagrammes générés (PNG)

Les images PNG sont déjà générées et versionnées (régénérables à tout moment).

### Architecture en 5 couches
![Architecture en 5 couches](architecture-5couches.png)

### Les 7 diagrammes UML

| | |
|---|---|
| **1. Contexte** | **2. Cas d'utilisation** |
| ![](diagrammes/diagramme-contexte.png) | ![](diagrammes/cas-utilisation.png) |
| **3. Séquence** | **4. Activité** |
| ![](diagrammes/diagramme-sequence.png) | ![](diagrammes/diagramme-activite.png) |
| **5. Classes** | **6. Composants** |
| ![](diagrammes/diagramme-classes.png) | ![](diagrammes/diagramme-composants.png) |
| **7. Déploiement** | |
| ![](diagrammes/diagramme-deploiement.png) | |

> Le modèle MERISE (MCD / MLD) est généré dans le dossier
> [`../database/`](../database/) (`mcd.png`, `mld.png`).

### Régénérer toutes les images

```bash
# 7 diagrammes UML + MERISE (nécessite Java + Graphviz)
java -jar plantuml.jar architecture/diagrammes/*.puml database/*.puml
# Schéma d'architecture 5 couches (nécessite matplotlib)
python architecture/generer_architecture_5couches.py
```
