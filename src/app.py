#!/usr/bin/env python3
"""
app.py - Application Flask de supervision réseau.

Routes :
    GET  /login                 Formulaire de connexion
    POST /login                 Authentification
    GET  /logout                Déconnexion
    GET  /                      Tableau de bord
    GET  /equipements           Liste des équipements
    POST /equipements/ajouter   Ajout d'un équipement
    POST /equipements/<id>/supprimer  Suppression
    GET  /journal               Journal des événements (paginé)
    GET  /rapports              Rapports de disponibilité
    POST /rapports/generer      Génère un nouveau rapport
    GET  /api/stats             API JSON – statistiques en temps réel
"""

import os
import sys
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask, render_template, redirect, url_for,
    request, session, flash, jsonify,
)
from werkzeug.security import check_password_hash

# Assurer que src/ est dans sys.path
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(_src_dir, '.env'))

from modules.db import get_connection, fetch_all, fetch_one, execute_query
from modules.monitor import calculer_disponibilite

# ---------------------------------------------------------------------------
# Initialisation Flask
# ---------------------------------------------------------------------------

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(_src_dir), 'templates'),
    static_folder=os.path.join(os.path.dirname(_src_dir), 'static'),
)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)


# ---------------------------------------------------------------------------
# Décorateur d'authentification
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter pour accéder à cette page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash("Accès réservé aux administrateurs.", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Authentification
# ---------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash("Veuillez remplir tous les champs.", "danger")
            return render_template('login.html')

        try:
            db  = get_connection()
            user = fetch_one(
                "SELECT * FROM utilisateurs WHERE email = %s AND actif = TRUE",
                (email,),
                connection=db,
            )
            db.close()
        except Exception as exc:
            flash(f"Erreur de connexion à la base de données : {exc}", "danger")
            return render_template('login.html')

        if user and check_password_hash(user['mot_de_passe'], password):
            session.permanent = True
            session['user_id']    = user['id']
            session['user_nom']   = user['nom']
            session['user_email'] = user['email']
            session['user_role']  = user['role']
            flash(f"Bienvenue, {user['nom']} !", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Identifiants incorrects.", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for('login'))


# ---------------------------------------------------------------------------
# Tableau de bord
# ---------------------------------------------------------------------------

@app.route('/')
@login_required
def dashboard():
    try:
        db = get_connection()

        total        = fetch_one("SELECT COUNT(*) AS n FROM equipements", connection=db)['n']
        nb_actifs    = fetch_one("SELECT COUNT(*) AS n FROM equipements WHERE statut='actif'", connection=db)['n']
        nb_inactifs  = fetch_one("SELECT COUNT(*) AS n FROM equipements WHERE statut='inactif'", connection=db)['n']
        nb_alertes   = fetch_one("SELECT COUNT(*) AS n FROM alertes WHERE envoye=FALSE", connection=db)['n']

        derniers_evenements = fetch_all(
            """SELECT j.niveau, j.message, j.timestamp,
                      e.nom AS equipement_nom, e.ip AS equipement_ip
               FROM journaux j
               JOIN equipements e ON j.equipement_id = e.id
               ORDER BY j.timestamp DESC
               LIMIT 10""",
            connection=db,
        )

        alertes_recentes = fetch_all(
            """SELECT a.type_alerte, a.message, a.timestamp, a.envoye,
                      e.nom AS equipement_nom, e.ip AS equipement_ip
               FROM alertes a
               JOIN equipements e ON a.equipement_id = e.id
               ORDER BY a.timestamp DESC
               LIMIT 5""",
            connection=db,
        )

        db.close()
    except Exception as exc:
        flash(f"Erreur base de données : {exc}", "danger")
        total = nb_actifs = nb_inactifs = nb_alertes = 0
        derniers_evenements = alertes_recentes = []

    return render_template(
        'dashboard.html',
        total=total,
        nb_actifs=nb_actifs,
        nb_inactifs=nb_inactifs,
        nb_alertes=nb_alertes,
        derniers_evenements=derniers_evenements,
        alertes_recentes=alertes_recentes,
        now=datetime.now(),
    )


# ---------------------------------------------------------------------------
# Équipements
# ---------------------------------------------------------------------------

@app.route('/equipements')
@login_required
def equipements():
    filtre_statut = request.args.get('statut', '')
    filtre_type   = request.args.get('type', '')

    sql    = "SELECT * FROM equipements WHERE 1=1"
    params = []

    if filtre_statut in ('actif', 'inactif', 'inconnu'):
        sql    += " AND statut = %s"
        params.append(filtre_statut)

    if filtre_type:
        sql    += " AND type = %s"
        params.append(filtre_type)

    sql += " ORDER BY nom ASC"

    try:
        db          = get_connection()
        liste       = fetch_all(sql, tuple(params), connection=db)
        types_dispo = fetch_all("SELECT DISTINCT type FROM equipements ORDER BY type", connection=db)
        db.close()
    except Exception as exc:
        flash(f"Erreur base de données : {exc}", "danger")
        liste = types_dispo = []

    return render_template(
        'equipements.html',
        equipements=liste,
        types_dispo=[r['type'] for r in types_dispo],
        filtre_statut=filtre_statut,
        filtre_type=filtre_type,
    )


@app.route('/equipements/ajouter', methods=['POST'])
@admin_required
def ajouter_equipement():
    nom          = request.form.get('nom', '').strip()
    ip           = request.form.get('ip', '').strip()
    type_eq      = request.form.get('type', 'inconnu').strip()
    localisation = request.form.get('localisation', '').strip()

    if not nom or not ip:
        flash("Le nom et l'adresse IP sont obligatoires.", "danger")
        return redirect(url_for('equipements'))

    try:
        db = get_connection()
        execute_query(
            """INSERT INTO equipements (nom, ip, type, localisation, statut, date_ajout)
               VALUES (%s, %s, %s, %s, 'inconnu', NOW())""",
            (nom, ip, type_eq, localisation),
            connection=db,
        )
        db.close()
        flash(f"Équipement « {nom} » ajouté avec succès.", "success")
    except Exception as exc:
        flash(f"Erreur lors de l'ajout : {exc}", "danger")

    return redirect(url_for('equipements'))


@app.route('/equipements/<int:eq_id>/supprimer', methods=['POST'])
@admin_required
def supprimer_equipement(eq_id):
    try:
        db = get_connection()
        eq = fetch_one("SELECT nom FROM equipements WHERE id=%s", (eq_id,), connection=db)
        if eq:
            execute_query("DELETE FROM equipements WHERE id=%s", (eq_id,), connection=db)
            flash(f"Équipement « {eq['nom']} » supprimé.", "success")
        else:
            flash("Équipement introuvable.", "warning")
        db.close()
    except Exception as exc:
        flash(f"Erreur lors de la suppression : {exc}", "danger")

    return redirect(url_for('equipements'))


# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------

@app.route('/journal')
@login_required
def journal():
    page     = max(1, int(request.args.get('page', 1)))
    par_page = 25
    offset   = (page - 1) * par_page
    niveau   = request.args.get('niveau', '')

    sql    = """SELECT j.id, j.niveau, j.message, j.timestamp,
                       e.nom AS equipement_nom, e.ip AS equipement_ip
                FROM journaux j
                JOIN equipements e ON j.equipement_id = e.id
                WHERE 1=1"""
    params = []

    if niveau in ('INFO', 'WARNING', 'ERROR', 'CRITICAL'):
        sql    += " AND j.niveau = %s"
        params.append(niveau)

    sql_count = sql.replace(
        "SELECT j.id, j.niveau, j.message, j.timestamp,\n                       e.nom AS equipement_nom, e.ip AS equipement_ip",
        "SELECT COUNT(*) AS n",
    )

    sql    += f" ORDER BY j.timestamp DESC LIMIT {par_page} OFFSET {offset}"

    try:
        db      = get_connection()
        total_n = fetch_one(sql_count, tuple(params), connection=db)['n']
        logs    = fetch_all(sql, tuple(params), connection=db)
        db.close()
    except Exception as exc:
        flash(f"Erreur base de données : {exc}", "danger")
        total_n = 0
        logs    = []

    total_pages = max(1, (total_n + par_page - 1) // par_page)

    return render_template(
        'journal.html',
        logs=logs,
        page=page,
        total_pages=total_pages,
        niveau=niveau,
        niveaux=['INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    )


# ---------------------------------------------------------------------------
# Rapports
# ---------------------------------------------------------------------------

@app.route('/rapports')
@login_required
def rapports():
    try:
        db      = get_connection()
        liste   = fetch_all("SELECT * FROM rapports ORDER BY genere_le DESC LIMIT 20", connection=db)
        equips  = fetch_all("SELECT id, nom FROM equipements ORDER BY nom", connection=db)
        db.close()
    except Exception as exc:
        flash(f"Erreur base de données : {exc}", "danger")
        liste  = []
        equips = []

    return render_template('rapports.html', rapports=liste, equipements=equips)


@app.route('/rapports/generer', methods=['POST'])
@admin_required
def generer_rapport():
    debut_str = request.form.get('debut', '')
    fin_str   = request.form.get('fin', '')

    if not debut_str or not fin_str:
        flash("Veuillez spécifier les dates de début et de fin.", "danger")
        return redirect(url_for('rapports'))

    try:
        debut = datetime.strptime(debut_str, '%Y-%m-%d')
        fin   = datetime.strptime(fin_str,   '%Y-%m-%d')
    except ValueError:
        flash("Format de date invalide (attendu : AAAA-MM-JJ).", "danger")
        return redirect(url_for('rapports'))

    if fin < debut:
        flash("La date de fin doit être postérieure à la date de début.", "danger")
        return redirect(url_for('rapports'))

    jours = max(1, (fin - debut).days)

    try:
        db         = get_connection()
        equipements = fetch_all("SELECT id FROM equipements", connection=db)
        nb_equips  = len(equipements)

        dispos = []
        for eq in equipements:
            dispos.append(calculer_disponibilite(eq['id'], db, jours=jours))

        dispo_moy  = round(sum(dispos) / nb_equips, 2) if nb_equips else 0.0
        nb_alertes = fetch_one(
            "SELECT COUNT(*) AS n FROM alertes WHERE timestamp BETWEEN %s AND %s",
            (debut, fin + timedelta(days=1)),
            connection=db,
        )['n']

        execute_query(
            """INSERT INTO rapports
                   (periode_debut, periode_fin, nb_equipements, disponibilite_moyenne, nb_alertes, genere_le)
               VALUES (%s, %s, %s, %s, %s, NOW())""",
            (debut.date(), fin.date(), nb_equips, dispo_moy, nb_alertes),
            connection=db,
        )
        db.close()
        flash(
            f"Rapport généré : {nb_equips} équipements, "
            f"disponibilité moyenne {dispo_moy:.2f} %, "
            f"{nb_alertes} alerte(s).",
            "success",
        )
    except Exception as exc:
        flash(f"Erreur lors de la génération du rapport : {exc}", "danger")

    return redirect(url_for('rapports'))


# ---------------------------------------------------------------------------
# API JSON
# ---------------------------------------------------------------------------

@app.route('/api/stats')
@login_required
def api_stats():
    try:
        db = get_connection()

        total       = fetch_one("SELECT COUNT(*) AS n FROM equipements", connection=db)['n']
        nb_actifs   = fetch_one("SELECT COUNT(*) AS n FROM equipements WHERE statut='actif'", connection=db)['n']
        nb_inactifs = fetch_one("SELECT COUNT(*) AS n FROM equipements WHERE statut='inactif'", connection=db)['n']
        nb_inconnus = fetch_one("SELECT COUNT(*) AS n FROM equipements WHERE statut='inconnu'", connection=db)['n']
        nb_alertes  = fetch_one("SELECT COUNT(*) AS n FROM alertes WHERE envoye=FALSE", connection=db)['n']

        derniers = fetch_all(
            """SELECT j.niveau, j.message, j.timestamp,
                      e.nom AS equipement_nom
               FROM journaux j
               JOIN equipements e ON j.equipement_id = e.id
               ORDER BY j.timestamp DESC
               LIMIT 5""",
            connection=db,
        )

        db.close()

        # Sérialiser les datetimes
        for row in derniers:
            row['timestamp'] = row['timestamp'].isoformat() if hasattr(row['timestamp'], 'isoformat') else str(row['timestamp'])

        return jsonify({
            'total':       total,
            'actifs':      nb_actifs,
            'inactifs':    nb_inactifs,
            'inconnus':    nb_inconnus,
            'alertes':     nb_alertes,
            'derniers':    derniers,
            'updated_at':  datetime.now().isoformat(),
        })

    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


# ---------------------------------------------------------------------------
# Gestion des erreurs
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template('base.html', error="Page introuvable (404)."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('base.html', error="Erreur interne du serveur (500)."), 500


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=debug,
    )
