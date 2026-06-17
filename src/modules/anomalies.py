# -*- coding: utf-8 -*-
"""
anomalies.py
============
Détection d'anomalies par apprentissage automatique sur l'historique de
supervision (table « journaux ») — supervision PRÉDICTIVE (AIOps).

Objectif : repérer les comportements anormaux AVANT la panne franche.

Principe
--------
À partir de l'historique multi-équipements (donc multi-clients), on calcule pour
chaque équipement un vecteur de caractéristiques :
  * latence moyenne, variabilité (écart-type), latence maximale ;
  * tendance de la latence (pente : une latence qui monte est suspecte) ;
  * taux d'indisponibilité récent ;
  * instabilité de la connexion (flapping = nombre de bascules UP/DOWN).

Un modèle d'apprentissage NON supervisé apprend le « comportement normal » de
l'ensemble du parc et signale les équipements qui s'en écartent. Ceux qui dérivent
tout en étant encore « UP » sont les candidats à une panne imminente : on émet
alors une alerte PRÉVENTIVE (sévérité AVERTISSEMENT).

Robustesse
----------
Le modèle scikit-learn (Isolation Forest) est OPTIONNEL : s'il n'est pas
installé, le module bascule automatiquement sur une méthode statistique
équivalente (scores z), sans aucune dépendance externe. Le système reste donc
opérationnel partout — et « prêt pour l'IA » dès que scikit-learn est disponible.
"""

import statistics

from modules import database
from modules import alertes
from modules.logger import get_logger

logger = get_logger("anomalies")

# Libellés des caractéristiques (ordre du vecteur), utile pour l'explication.
CARACTERISTIQUES = ["latence_moyenne", "latence_ecart_type", "latence_max",
                    "tendance_latence", "taux_indisponibilite", "flapping"]


# ---------------------------------------------------------------------- #
# 1) Construction des caractéristiques (feature engineering)             #
# ---------------------------------------------------------------------- #
def _pente(serie):
    """Pente d'une régression linéaire simple (moindres carrés)."""
    n = len(serie)
    if n < 2:
        return 0.0
    xs = list(range(n))
    mx = statistics.fmean(xs)
    my = statistics.fmean(serie)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, serie))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else 0.0


def _caracteristiques_equipement(equipement, fenetre=200):
    """Construit le vecteur de caractéristiques d'un équipement à partir de ses
    derniers journaux. Retourne None si l'historique est insuffisant."""
    journaux = database.get_journaux(limit=fenetre, equipement_id=equipement["id"])
    if len(journaux) < 5:
        return None

    # get_journaux renvoie les plus récents d'abord.
    latences = [j["latence_ms"] for j in journaux if j["latence_ms"] is not None]
    statuts = [1 if j["statut"] == "UP" else 0 for j in journaux]
    n = len(journaux)
    if not latences:
        latences = [0.0]

    moyenne = statistics.fmean(latences)
    ecart = statistics.pstdev(latences) if len(latences) > 1 else 0.0
    maxi = max(latences)
    # tendance : on remet la série dans l'ordre chronologique (ancien -> récent).
    pente = _pente(list(reversed(latences)))
    taux_indispo = 1.0 - (sum(statuts) / n)
    transitions = sum(1 for a, b in zip(statuts, statuts[1:]) if a != b)
    flapping = transitions / max(1, n - 1)

    return {
        "equipement": equipement,
        "statut_actuel": equipement.get("statut"),
        "vecteur": [moyenne, ecart, maxi, pente, taux_indispo, flapping],
        "latence_moyenne": moyenne, "latence_ecart_type": ecart,
        "tendance_latence": pente, "taux_indisponibilite": taux_indispo,
        "flapping": flapping,
    }


# ---------------------------------------------------------------------- #
# 2) Détection : Isolation Forest, avec repli statistique                #
# ---------------------------------------------------------------------- #
def _detecter_isolation_forest(vecteurs):
    """Apprentissage non supervisé (Isolation Forest). Lève ImportError si
    scikit-learn / numpy ne sont pas installés."""
    from sklearn.ensemble import IsolationForest   # import différé (optionnel)
    import numpy as np

    X = np.array(vecteurs, dtype=float)
    modele = IsolationForest(contamination="auto", random_state=42)
    prediction = modele.fit_predict(X)              # -1 = anomalie, 1 = normal
    scores = modele.score_samples(X)                # plus bas = plus anormal
    indices = [i for i, p in enumerate(prediction) if p == -1]
    return indices, [float(s) for s in scores]


def _detecter_statistique(vecteurs, seuil_z=3.5):
    """Repli sans dépendance : méthode ROBUSTE médiane + MAD (Median Absolute
    Deviation). Un équipement est anormal si l'une de ses caractéristiques
    s'écarte fortement de la médiane du parc, mesurée par un estimateur robuste
    insensible aux valeurs aberrantes elles-mêmes (contrairement à l'écart-type
    classique, qui serait « masqué » par l'outlier)."""
    colonnes = list(zip(*vecteurs))
    medianes = [statistics.median(c) for c in colonnes]
    echelles = []
    for j, col in enumerate(colonnes):
        ecarts_abs = [abs(v - medianes[j]) for v in col]
        mad = statistics.median(ecarts_abs)
        if mad > 0:
            echelle = 1.4826 * mad                  # estimateur robuste de σ
        else:
            # Repli quand la majorité des valeurs sont identiques et qu'un seul
            # point dévie (MAD = 0) : on utilise l'écart absolu moyen.
            echelle = statistics.fmean(ecarts_abs)
        echelles.append(echelle)

    indices, scores = [], []
    for i, vec in enumerate(vecteurs):
        z = [abs((v - medianes[j]) / echelles[j]) if echelles[j] > 0 else 0.0
             for j, v in enumerate(vec)]
        z_max = max(z)
        scores.append(-z_max)                       # cohérent : bas = anormal
        if z_max >= seuil_z:
            indices.append(i)
    return indices, scores


def detecter_anomalies(fenetre=200):
    """Analyse l'ensemble du parc et retourne la liste des équipements au
    comportement anormal (avec leur score et leurs caractéristiques)."""
    equipements = database.get_all_equipements(actifs_seulement=True)
    caracs = [c for c in (_caracteristiques_equipement(e, fenetre)
                          for e in equipements) if c]

    if len(caracs) < 5:
        logger.info("Historique insuffisant pour l'analyse d'anomalies "
                    "(%d équipement(s) exploitable(s)).", len(caracs))
        return []

    vecteurs = [c["vecteur"] for c in caracs]
    try:
        indices, scores = _detecter_isolation_forest(vecteurs)
        methode = "Isolation Forest (scikit-learn)"
    except ImportError:
        indices, scores = _detecter_statistique(vecteurs)
        methode = "statistique 3-sigma (repli sans scikit-learn)"

    logger.info("Analyse d'anomalies via %s : %d/%d équipement(s) signalé(s).",
                methode, len(indices), len(caracs))

    resultats = []
    for i in indices:
        caracs[i]["score"] = scores[i]
        resultats.append(caracs[i])
    return resultats


# ---------------------------------------------------------------------- #
# 3) Explication + alerte préventive                                     #
# ---------------------------------------------------------------------- #
def _expliquer(c):
    """Traduit un profil anormal en raisons lisibles par un humain."""
    raisons = []
    if c["tendance_latence"] > 0.5:
        raisons.append("latence en hausse continue")
    if c["flapping"] > 0.2:
        raisons.append("connexion instable (flapping)")
    if c["taux_indisponibilite"] > 0.1:
        raisons.append("indisponibilités intermittentes")
    if c["latence_ecart_type"] > max(c["latence_moyenne"], 1.0):
        raisons.append("latence très variable")
    return ", ".join(raisons) if raisons else "profil statistique atypique"


def analyser_et_alerter(fenetre=200):
    """Analyse le parc et émet une alerte PRÉVENTIVE pour chaque équipement
    encore en ligne mais au comportement anormal (panne possible).

    Returns:
        int : nombre d'alertes préventives émises.
    """
    anomalies = detecter_anomalies(fenetre)
    emises = 0
    for c in anomalies:
        # On ne pré-alerte que les équipements ENCORE joignables : l'intérêt est
        # d'anticiper la panne, pas de doublonner une alerte de panne déjà émise
        # (un équipement déjà DOWN est traité par le moteur de supervision).
        if c.get("statut_actuel") != "UP":
            continue
        message = "Comportement anormal détecté (panne possible) : " + _expliquer(c)
        # declencher_alerte applique déjà l'anti-spam (une alerte par type/équipement).
        if alertes.declencher_alerte(c["equipement"],
                                     type_alerte="ANOMALIE_PREDICTIVE",
                                     severite="AVERTISSEMENT",
                                     message=message):
            emises += 1
            logger.info("Alerte préventive émise pour %s (%s).",
                        c["equipement"]["nom"], _expliquer(c))
    logger.info("Analyse prédictive terminée : %d alerte(s) préventive(s).", emises)
    return emises
