from flask import Flask, render_template, request, redirect, session, jsonify
from flask_cors import CORS
import facebook
import json
import requests
import urllib
from validation import *
from config import *

# Crée le json pour les events au bon format pour la bdd
def creer_evenement_json(date, heure_debut, heure_fin, titre):
    # Créer un objet JSON avec les clés "title", "start" et "end"
    evenement = {
        "title": titre,
        "start": f"{date}T{heure_debut}:00",
        "end": f"{date}T{heure_fin}:00"
    }
    return json.dumps(evenement)

# Crée le json au bon format pour stocker les données d'un utilisateur 
def CreerDonneeUtilisateur(name):
    user_data = {
        "name": name,
        "groupes": [],
        "events" : []
    }
    return user_data


# Initialisation de l'application Flask
app = Flask(__name__, template_folder='template', static_folder='static')

# Clé secrète pour signer la session
app.secret_key = 'votre_cle_secrete'

#Ouverture des requetes a tout les domaines pour pouvoir echnager avec l'interface mobile 
CORS(app, resources={r"/*": {"origins": "*"}})


#Route pour afficher la page de connexion 
@app.route('/')
def index():
    return render_template('login.html')


#Route pour rediriger vers la page d'authentification de facebook
@app.route('/login-facebook')
def login():
    auth_url = facebook.GraphAPI().get_auth_url(app_id, redirect_uri)
    return redirect(auth_url)


#Route pour gérer la connexion depuis un mobile 
@app.route('/login-app', methods=['POST'])
def login_app():
    #Récupère l'id de l'utilisateur 
    user_id = request.json.get('userId')
 
    #Intérroge la bdd pour savoir si l'user existe
    reponse = requests.post(api_url + "/user-exist", json={"user_id":user_id})
    json_data = reponse.json()
    message = json_data.get('message')

    #Si il existe 
    if (message == "User exist"): 
        
        session['mobile'] = 1
        print(session['mobile'])
        #Récuperer son nom dans la bdd
        reponse = requests.post(api_url + "/user-name", json={"user_id":user_id})
        json_data = reponse.json()
        nom = json_data.get('message')

        #Récupérer la liste de ses groupes
        reponse = requests.post(api_url + "/user-group", json={"user_id":user_id})
        json_data = reponse.json()
        liste_groupe = json_data.get('liste') 
        
        #Enregistrer les données dans la session 
        session['user_id'] = user_id
        session['user_name'] = nom

        #Retourner les données pour l'interface mobile 
        return jsonify({'message': 'Authentification réussie', "id" : user_id, "nom": nom, "listeGroupe" : liste_groupe}), 200
    else :
        #Si l'identifiant n'existe pas 
        return jsonify({'message': 'Authentification échoué'}), 200


#Page d'acceuil de l'interface web 
@app.route('/acceuil')
def acceuil():
    #Stocke que l'utilisateur se connecte depuis le web 
    session['mobile'] = 0
    # Vérifie si l'utilisateur est connecté en vérifiant si son ID est dans la session
    if 'user_id' in session:
        #Si oui on récupère les informations de l'utilisateur 
        id = session['user_id']
        name = session['user_name']
        
        #Récupération de la liste des groupes de l'utilisateur
        reponse = requests.post(api_url + "/user-group", json={"user_id":id})
        json_data = reponse.json()
        liste_groupe = json_data.get('liste') 

    else:
        #Sinon on récupère les informations depuis facebook
        code = request.args.get('code')
        access_token = facebook.GraphAPI().get_access_token_from_code(code, redirect_uri, app_id, app_secret)
        graph = facebook.GraphAPI(access_token['access_token'])
        me = graph.get_object('me')
        id = me['id']
        name = me['name']

        #Creer l'utilisateur dans la bdd si il n'existe pas 
        user_data = CreerDonneeUtilisateur(name)
        requests.post(api_url + "/ajout-utilisateur", json={"user_id":id, "user_data":user_data})
  
        # Stocke les informations de l'utilisateur dans la session
        session['user_id'] = id
        session['user_name'] = name
        
        #Récupération de la liste des groupes de l'utilisateur
        reponse = requests.post(api_url + "/user-group", json={"user_id":id})
        json_data = reponse.json()
        liste_groupe = json_data.get('liste')
    
    return render_template("acceuil.html", nom=name, user_groups2=liste_groupe, user_id=session['user_id'])


#Déconnecte l'utilisateur et le renvoie sur la page de connexion 
@app.route('/deconnexion')
def deconnexion():
    # Efface les données de session de l'utilisateur
    temp = session['mobile']
    session.clear()
    if (temp):
        return jsonify({'message': 'Déconnexion'}), 200
    else:
        return redirect('/')


#Route pour créer un nouveau groupe 
@app.route('/creer-groupe', methods=['POST'])
def nouveauGroupe():
    if request.method == 'POST':
        #Récupère le nom du groupe de la bonne facon selon mobile ou web 
        if(session['mobile']):
            #Récupère le nom du groupe à creer
            group_name = request.json.get('group_name')
        else : 
            group_name = request.form['group-name']

        #Fait la requete a la bdd pour ajouter un nouveau groupe
        requests.post(api_url + "/nouveau-groupe", json={"user_id":session['user_id'], "group_name" : group_name})

        reponse = requests.post(api_url + "/user-group", json={"user_id":session['user_id']})
        json_data = reponse.json()
        liste_groupe = json_data.get('liste')
       
        #Récupération de la liste des groupes de l'utilisateur
        return jsonify({'message': 'Groupe ajouté', "listeGroupe" : liste_groupe}), 200
 


#Route pour afficher les détails d'un groupe
@app.route('/groupe-details', methods=['POST','GET'])
def groupe_details():
    #Récupération de l'id du groupe 
    if(session['mobile']):
        group_id = request.json.get('group_id')
    else : 
        group_id = request.args.get('id')
    
    #Récupération du nom, de la liste des utilisateur et de l'information sur l'admin du groupe
    reponse = requests.post(api_url + "/info-group", json={"user_id":session['user_id'], "group_id":group_id})
    json_data = reponse.json()
    name = json_data.get('name')
    liste_user = json_data.get('liste')
    admin = json_data.get('admin')

    if(name != None):   
    #Envoie des données
        if(session['mobile']):
            return jsonify({'message': 'Info Groupe', 'group_name' : name, 'user_list': liste_user, 'test_admin' : admin}), 200
        else : 
            return render_template("groupe-details.html", group_name=name, group_id=group_id, user_list=liste_user, test_admin = admin)
    else : 
        if(session['mobile']):
            return jsonify({'message': 'Groupe indisponible'}), 200
        else : 
            return redirect("/acceuil")

#Route pour rejoindre un groupe existant
@app.route('/rejoindre-groupe', methods=['POST'])
def rejoindre_groupe():
    if request.method == 'POST':
        #Récupération de l'id du groupe
        if(session['mobile']):
            group_id = request.json.get('group_id')
        else :
            group_id = request.form['group-id']
            
        result = requests.post(api_url + "/ajout-user-group", json={"user_id":session['user_id'], "group_id": group_id})
        message = result.json().get('message')

        reponse = requests.post(api_url + "/user-group", json={"user_id":session['user_id']})
        json_data = reponse.json()
        liste_groupe = json_data.get('liste') 

        return jsonify({'listeGroupe': liste_groupe, 'message' : message})
      
    
#Supprime un groupe si l'utilisateur est l'admin
@app.route('/supprime-groupe', methods=['POST', 'GET'])
def supprimer_groupe():
    #Récupération de l'id du groupe
    if(session['mobile']):
        group_id = request.json.get('group_id')
    else :
        group_id = request.args.get('id')

    requests.post(api_url + "/delete-group", json={"group_id": group_id})

    if(session['mobile']):
        reponse = requests.post(api_url + "/user-group", json={"user_id":session['user_id']})
        json_data = reponse.json()
        liste_groupe = json_data.get('liste') 
        return jsonify({'listeGroupe': liste_groupe})
    else :
        return redirect('/acceuil')


#Affiche le calendrier d'un groupe 
@app.route('/calendrier-groupe', methods=['POST', 'GET'])
def calendrier_groupe():
    #Récupère l'id du groupe
    if(session['mobile'] == 1):
        group_id = request.json.get('group_id')
    else:
        group_id = request.args.get('id')

    #Récupère la liste des événement du groupe
    reponse = requests.post(api_url + "/liste-event-group", json={"group_id": group_id})
    json_data = reponse.json()
    events = json_data.get('liste')

    if (session['mobile'] == 1):
        return jsonify({'events': events})
    else : 
        return render_template('emploi_du_temps.html', events=json.dumps(events), group_id=group_id)


#Sauvegarde un créneau de groupe
@app.route('/sauvegarder-creneau', methods=['POST'])
def sauvegarder_creneau():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        if(session['mobile'] == 1):
            titre = request.json.get('titre')
            date = request.json.get('date')
            heure_debut = request.json.get('heure_debut')
            heure_fin = request.json.get('heure_fin')
            group_id = request.json.get('group_id')
        else:
            # Récupérer les données du formulaire
            titre = request.form.get('titre')
            date = request.form.get('date')
            heure_debut = request.form.get('heure-debut')
            heure_fin = request.form.get('heure-fin')
            group_id = request.form.get('group-id')

        result = sauvegarder_creneau_variables_validation(titre, date, heure_debut, heure_fin, group_id)

        titre = escape_injection(titre)

        if result[0] :
            #Création du json pour stocker l'event
            json = creer_evenement_json(date, heure_debut,heure_fin,titre)
            #Ajout a la bdd
            requests.post(api_url + "/add-event-group", json={"group_id": group_id, "json" : json})
            if(session['mobile'] == 1):
                return jsonify({'message':"Créneau ajouté avec succès !"})
            else :
                return 'Créneau ajouté avec succès !'
        else : 
            if(session['mobile'] == 1):
                return jsonify({'message':result[1]})
            else :
                return result[1]


@app.route('/sauvegarder-creneau-user', methods=['POST'])
def sauvegarder_creneau_user():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        if(session['mobile'] == 1):
            titre = request.json.get('titre')
            date = request.json.get('date')
            heure_debut = request.json.get('heure_debut')
            heure_fin = request.json.get('heure_fin')
            user_id = session['user_id']
        else:
            titre = request.form.get('titre')
            date = request.form.get('date')
            heure_debut = request.form.get('heure-debut')
            heure_fin = request.form.get('heure-fin')
            user_id = session['user_id']

        result = sauvegarder_creneau_variables_validation(titre, date, heure_debut, heure_fin, user_id)
        titre = escape_injection(titre)

        print(result[0])
        if (result[0] == True):
            #Création du json pour stocker l'event
            json = creer_evenement_json(date, heure_debut,heure_fin,titre)
            #Ajout a la bdd
            reponse = requests.post(api_url + "/add-event-user", json={"user_id": user_id, "json" : json})
            if(session['mobile'] == 1):
                return jsonify({'message':"Créneau ajouté avec succès !"})
            else :
                return 'Créneau ajouté avec succès !'
        else : 
            if(session['mobile'] == 1):
                return jsonify({'message':result[1]})
            else :
                return result[1]


#Retourne la liste de tout les événement de l'utilisateur
@app.route('/calendrier-user')
def calendrier_user():
    reponse = requests.post(api_url + "/liste-event-user", json={"user_id":session['user_id']})
    json_data = reponse.json()
    events = json_data.get('liste')
    if(session['mobile'] == 1):
        return jsonify({'events': events})
    else : 
        return render_template('emploi_du_temps.html', events=json.dumps(events), group_id="null")

#Route pour quitter un groupe dont l'utilisateur n'est pas l'admin 
@app.route('/quitter-groupe', methods=['POST', 'GET'])
def quitter_groupe():
   #Récupère l'id du groupe
    if(session['mobile'] == 1):
        group_id = request.json.get('group_id')
    else:
        group_id = request.args.get('id')

    requests.post(api_url + "/quitter-groupe", json={"group_id": group_id, "user_id": session['user_id']})

    if(session['mobile']):
        reponse = requests.post(api_url + "/user-group", json={"user_id":session['user_id']})
        json_data = reponse.json()
        liste_groupe = json_data.get('liste') 
        return jsonify({'listeGroupe': liste_groupe})
    else :
        return redirect('/acceuil')


