from flask import Flask, render_template, request, redirect, session
import facebook
import sys
import os
import json
from flask_cors import CORS
from flask import jsonify

# Ajoutez le chemin du dossier ServicePython au chemin de recherche Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'ServicePython'))

import ServiceBdd

def creer_evenement_json(date, heure_debut, heure_fin, titre):
    # Créer un objet JSON avec les clés "title", "start" et "end"
    evenement = {
        "title": titre,
        "start": f"{date}T{heure_debut}:00",
        "end": f"{date}T{heure_fin}:00"
    }
    return json.dumps(evenement)

# Facebook app credentials
app_id = '1721756045020268'
app_secret = 'e0239934728a294f232fd1ed7bb16445'
redirect_uri = 'http://localhost:5000/acceuil'  # Update with your own redirect URI

# Initialisation de l'application Flask
app = Flask(__name__, template_folder='template', static_folder='static')

CORS(app, resources={r"/*": {"origins": "*"}})

# Clé secrète pour signer la session
app.secret_key = 'votre_cle_secrete'

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login-facebook')
def login():
    auth_url = facebook.GraphAPI().get_auth_url(app_id, redirect_uri)
    return redirect(auth_url)

@app.route('/login-app', methods=['POST'])
def login_app():
    session['mobile'] = 1
    userid = request.json.get('userId')
    reponse = ServiceBdd.user_existe(userid)
    if (reponse): 
        nom = ServiceBdd.obtenir_nom_utilisateur_par_id_utilisateur(userid)
        liste_groupe = ServiceBdd.groupesUtilisateurParIdUtilisateur(userid)
        session['user_id'] = userid
        session['user_name'] = nom
        return jsonify({'message': 'Authentification réussie', "id" : userid, "nom": nom, "listeGroupe" : liste_groupe}), 200
    else :
        return jsonify({'message': 'Authentification échoué'}), 200

@app.route('/acceuil')
def acceuil():
    if 'user_id' in session:  # Vérifie si l'utilisateur est connecté en vérifiant si son ID est dans la session
        id = session['user_id']
        name = session['user_name']
        # Récupérer la liste des groupes de l'utilisateur

        liste_groupe = ServiceBdd.groupesUtilisateurParIdUtilisateur(id)

    else:
        code = request.args.get('code')
        access_token = facebook.GraphAPI().get_access_token_from_code(code, redirect_uri, app_id, app_secret)
        graph = facebook.GraphAPI(access_token['access_token'])
        me = graph.get_object('me')
        id = me['id']
        name = me['name']
        #Creer l'utilisateur dans la bdd si il n'existe pas 
        ServiceBdd.ajoutUtilisateur(id,ServiceBdd.CreerDonneeUtilisateur(name))
        # Stocke les informations de l'utilisateur dans la session
        session['user_id'] = id
        session['user_name'] = name
        session['mobile'] = 0

        liste_groupe = ServiceBdd.groupesUtilisateurParIdUtilisateur(id)
          
    return render_template("acceuil.html", nom=name, user_groups2=liste_groupe)

@app.route('/deconnexion')
def deconnexion():
    # Efface les données de session de l'utilisateur
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.clear()
    return redirect('/')

@app.route('/creer-groupe', methods=['POST'])
def nouveauGroupe():
    if request.method == 'POST':
        if(session['mobile']):
            group_name = request.json.get('group_name')
            print(group_name)
            ServiceBdd.nouveauGroupe(group_name, session['user_id'])
            liste_groupe = ServiceBdd.groupesUtilisateurParIdUtilisateur(session['user_id'])
            return jsonify({'message': 'Groupe ajouté', "listeGroupe" : liste_groupe}), 200
        else : 
            group_name = request.form['group-name']
            ServiceBdd.nouveauGroupe(group_name, session['user_id'])
            return redirect('/acceuil')

@app.route('/groupe-details')
def groupe_details():
    if(session['mobile']):
        group_id = request.json.get('group_id')
    else : 
        group_id = request.args.get('id')

    liste_user = ServiceBdd.utilisateursParIdGroupe(group_id)
    admin = ServiceBdd.estAdminDuGroupe(session['user_id'], group_id)
    name = ServiceBdd.nomDuGroupeParId(group_id)
    
    if(session['mobile']):
        return jsonify({'message': 'Info Groupe', 'group_name' : name, 'user_list': liste_user, 'test_admin' : admin}), 200
    else : 
        return render_template("groupe-details.html", group_name=name, group_id=group_id, user_list=liste_user, test_admin = admin)

@app.route('/rejoindre-groupe', methods=['POST'])
def rejoindre_groupe():
    if request.method == 'POST':
        group_id = request.form['group-name']
        ServiceBdd.ajoutUtilisateurGroupe(group_id,session['user_id'])
    return redirect('/acceuil')

@app.route('/supprime-groupe')
def supprimer_groupe():
    group_id = request.args.get('id')
    ServiceBdd.supprimeGroupe(group_id)
    return redirect('/acceuil')

@app.route('/calendrier-groupe')
def calendrier_groupe():
    group_id = request.args.get('id')
    events = ServiceBdd.liste_evenements_groupe(group_id)
    print(events)
    return render_template('emploi_du_temps.html', events=json.dumps(events), group_id=group_id)

@app.route('/sauvegarder-creneau', methods=['POST'])
def sauvegarder_creneau():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.form.get('titre')
        date = request.form.get('date')
        heure_debut = request.form.get('heure-debut')
        heure_fin = request.form.get('heure-fin')
        group_id = request.form.get('group-id')

        json = creer_evenement_json(date, heure_debut,heure_fin,titre)
        ServiceBdd.ajouter_evenement_groupe(json, group_id)
    return 'Créneau ajouté avec succès !'

@app.route('/sauvegarder-creneau-user', methods=['POST'])
def sauvegarder_creneau_user():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.form.get('titre')
        date = request.form.get('date')
        heure_debut = request.form.get('heure-debut')
        heure_fin = request.form.get('heure-fin')
        user_id = session['user_id']

        json = creer_evenement_json(date, heure_debut,heure_fin,titre)
        ServiceBdd.ajouter_evenement_user(json, user_id)
    return 'Créneau ajouté avec succès !'

@app.route('/calendrier-user')
def calendrier_user():
    liste_groupe = ServiceBdd.groupesUtilisateurParIdUtilisateur(session['user_id'])
    liste_ids = [element['id'] for element in liste_groupe]
    events = ServiceBdd.liste_evenements_user(session['user_id'])
    for group_id in liste_ids :
        events_groupe = ServiceBdd.liste_evenements_groupe(group_id)
        events.extend(events_groupe)
    print(events)
    return render_template('emploi_du_temps.html', events=json.dumps(events), group_id="null")

'''
if __name__ == '__main__':
    app.run(debug=True)
'''
