#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py
======
APPLICATION WEB FLASK — tableau de bord de supervision.

Cette application fournit l'interface d'administration et de visualisation :
  - tableau de bord temps réel (statistiques, état global) ;
  - gestion des équipements (CRUD) ;
  - historique des alertes (avec acquittement) ;
  - journaux de supervision ;
  - rapports et statistiques ;
  - API REST JSON consommée par le front (rafraîchissement AJAX).

L'authentification protège l'accès (Flask-Login). Le moteur de collecte
(supervisor.py) tourne indépendamment via Cron : Flask ne fait que LIRE et
présenter les données, ce qui garde l'interface légère et réactive.
"""

from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                   flash, jsonify, session)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from modules import database
from modules.logger import get_logger

logger = get_logger("webapp")

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY


# ---------------------------------------------------------------------- #
# Authentification minimaliste (décorateur)                              #
# ---------------------------------------------------------------------- #
def login_required(vue):
    """Décorateur protégeant une route : redirige vers /login si non connecté."""
    @wraps(vue)
    def wrapper(*args, **kwargs):
        if not session.get("utilisateur"):
            return redirect(url_for("login", next=request.path))
        return vue(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    """Page de connexion. Vérifie les identifiants contre la table utilisateurs."""
    if request.method == "POST":
        identifiant = request.form.get("identifiant", "")
        mot_de_passe = request.form.get("mot_de_passe", "")
        utilisateur = _verifier_identifiants(identifiant, mot_de_passe)
        if utilisateur:
            session["utilisateur"] = utilisateur["identifiant"]
            session["role"] = utilisateur["role"]
            logger.info("Connexion réussie : %s", identifiant)
            return redirect(request.args.get("next") or url_for("dashboard"))
        flash("Identifiants invalides.", "danger")
        logger.warning("Échec de connexion pour : %s", identifiant)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Déconnexion : vide la session."""
    session.clear()
    return redirect(url_for("login"))


def _verifier_identifiants(identifiant, mot_de_passe):
    """Vérifie l'identifiant/mot de passe (hash) contre la base."""
    with database.get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM utilisateurs WHERE identifiant = %s", (identifiant,)
        )
        utilisateur = cursor.fetchone()
    if utilisateur and check_password_hash(utilisateur["mot_de_passe_hash"], mot_de_passe):
        return utilisateur
    return None


# ---------------------------------------------------------------------- #
# Pages de l'interface                                                    #
# ---------------------------------------------------------------------- #
@app.route("/")
@login_required
def dashboard():
    """Tableau de bord principal : vue d'ensemble et indicateurs."""
    stats = database.get_statistiques()
    equipements = database.get_all_equipements()
    alertes_actives = database.get_alertes(limit=10, non_acquittees=True)
    return render_template(
        "dashboard.html", stats=stats, equipements=equipements,
        alertes=alertes_actives,
    )


@app.route("/equipements")
@login_required
def equipements():
    """Page de gestion (liste) des équipements supervisés."""
    return render_template("equipements.html",
                           equipements=database.get_all_equipements(actifs_seulement=False))


@app.route("/equipements/ajouter", methods=["POST"])
@login_required
def ajouter_equipement():
    """Ajoute un équipement depuis le formulaire de la page équipements."""
    database.add_equipement(
        nom=request.form["nom"],
        adresse_ip=request.form["adresse_ip"],
        type_equipement=request.form["type_equipement"],
        emplacement=request.form.get("emplacement", ""),
    )
    flash("Équipement ajouté avec succès.", "success")
    return redirect(url_for("equipements"))


@app.route("/equipements/supprimer/<int:equipement_id>", methods=["POST"])
@login_required
def supprimer_equipement(equipement_id):
    """Supprime un équipement et ses données associées."""
    database.delete_equipement(equipement_id)
    flash("Équipement supprimé.", "info")
    return redirect(url_for("equipements"))


@app.route("/alertes")
@login_required
def alertes_page():
    """Historique des alertes."""
    return render_template("alertes.html", alertes=database.get_alertes(limit=200))


@app.route("/alertes/acquitter/<int:alerte_id>", methods=["POST"])
@login_required
def acquitter(alerte_id):
    """Acquitte (marque comme traitée) une alerte."""
    database.acquitter_alerte(alerte_id)
    flash("Alerte acquittée.", "success")
    return redirect(url_for("alertes_page"))


@app.route("/journaux")
@login_required
def journaux():
    """Affiche l'historique des vérifications (journaux)."""
    return render_template("journaux.html", journaux=database.get_journaux(limit=300))


@app.route("/rapports")
@login_required
def rapports():
    """Page de rapports et statistiques avancées."""
    return render_template("rapports.html", stats=database.get_statistiques(),
                           equipements=database.get_all_equipements())


# ---------------------------------------------------------------------- #
# API REST (JSON) — consommée par le JavaScript pour le rafraîchissement  #
# ---------------------------------------------------------------------- #
@app.route("/api/statistiques")
@login_required
def api_statistiques():
    """Retourne les statistiques au format JSON (pour les graphiques temps réel)."""
    return jsonify(database.get_statistiques())


@app.route("/api/equipements")
@login_required
def api_equipements():
    """Retourne l'état des équipements au format JSON."""
    equipements = database.get_all_equipements()
    # On convertit les dates en chaînes pour la sérialisation JSON.
    for e in equipements:
        if e.get("derniere_verification"):
            e["derniere_verification"] = e["derniere_verification"].isoformat()
    return jsonify(equipements)


@app.route("/api/alertes")
@login_required
def api_alertes():
    """Retourne les alertes actives au format JSON."""
    alertes = database.get_alertes(limit=20, non_acquittees=True)
    for a in alertes:
        if a.get("date_alerte"):
            a["date_alerte"] = a["date_alerte"].isoformat()
    return jsonify(alertes)


# ---------------------------------------------------------------------- #
# Filtres de gabarit (templates)                                          #
# ---------------------------------------------------------------------- #
@app.template_filter("statut_badge")
def statut_badge(statut):
    """Associe une classe CSS Bootstrap à un statut (pour colorer les badges)."""
    return {"UP": "success", "DOWN": "danger"}.get(statut, "secondary")


if __name__ == "__main__":
    logger.info("Démarrage du tableau de bord Flask sur %s:%s", config.HOST, config.PORT)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
