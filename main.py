from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS  # Importez Flask-CORS
import facebook
import sys
import os

# Ajoutez le chemin du dossier ServicePython au chemin de recherche Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'ServicePython'))

import ServiceBdd


# Facebook app credentials
app_id = '1721756045020268'
app_secret = 'e0239934728a294f232fd1ed7bb16445'
redirect_uri = 'http://localhost:5000/acceuil'  # Update with your own redirect URI

# Initialisation de l'application Flask
app = Flask(__name__, template_folder='template', static_folder='static')

# Clé secrète pour signer la session
app.secret_key = 'votre_cle_secrete'

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login-facebook')
def login():
    auth_url = facebook.GraphAPI().get_auth_url(app_id, redirect_uri)
    return redirect(auth_url)


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

        liste_groupe = ServiceBdd.groupesUtilisateurParIdUtilisateur(id)
          
    return render_template("acceuil.html", nom=name, user_groups2=liste_groupe)

@app.route('/deconnexion')
def deconnexion():
    # Efface les données de session de l'utilisateur
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect('/')

@app.route('/creer-groupe', methods=['POST'])
def nouveauGroupe():
    if request.method == 'POST':
        group_name = request.form['group-name']
        ServiceBdd.nouveauGroupe(group_name, session['user_id'])
    return redirect('/acceuil')

@app.route('/groupe-details')
def groupe_details():
    group_id = request.args.get('id')
    liste_user = ServiceBdd.utilisateursParIdGroupe(group_id)
    admin = ServiceBdd.estAdminDuGroupe(session['user_id'], group_id)
    return render_template("groupe-details.html", group_name=group_id, user_list=liste_user, test_admin = admin)


if __name__ == '__main__':
    app.run(debug=True)
