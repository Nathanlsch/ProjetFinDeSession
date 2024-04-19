from flask import Flask, request, jsonify
import json
from ServiceBdd import * 

app = Flask(__name__)


#--------------------Serveur Flask permettant de manipuler la base de donnée via une API--------------

'''
Ajoute un utilisateur à la base de données 
Méthode POST : Argument : user_id et user_data
Retourne un json avec un message de succès ou d'échec
'''
@app.route('/ajout-utilisateur', methods=['POST'])
def ajout_utilisateur():
    user_id = request.json.get('user_id')
    user_data = request.json.get('user_data')
    etat = ajoutUtilisateur(user_id, user_data)
    if (etat == 0):
        return jsonify({"message": "User added successfully"}), 201
    else :
        return jsonify({"message": "User already exist"}), 201

'''
# Suppression utilisateur de la table des utilisateurs (user_id) 
@app.route('/supprime-utilisateur', methods=['POST'])
def supprime_utilisateur():
    user_id = request.json.get('user_id')
    etat = supprimeUtilisateur(user_id)
    if (etat == 0):
        return jsonify({"message": "User deleted successfully"}), 201
    else : 
        return jsonify({"message": "User does not exist"}), 201
'''


'''
Création d'un nouveau groupe et ajout du créateur
Méthode POST : Argument : user_id et group_name
Retourne un json avec un message de succès ou d'échec
'''
@app.route('/nouveau-groupe', methods=['POST'])
def nouveau_groupe():
    group_name = request.json.get('group_name')
    user_id = request.json.get('user_id')
    etat = nouveauGroupe(group_name, user_id)
    if (etat == 0):
        return jsonify({"message": "Group created successfully"}), 201
    else:
        return jsonify({"message": "User does not exist"})

'''
#Test de l'existence d'un utilisateur (user_id)
@app.route('/user-exist', methods=['POST'])
def user_exist():
    user_id = request.json.get('user_id')
    etat = user_existe(user_id)
    if (etat):
        return jsonify({"message": "User exist"})
    else:
        return jsonify({"message": "User don't exist"})
'''

'''
Renvoie le nom d'un utilisateur a partir de son id
Méthode POST : Argument : user_id
Retourne un json avec un message contenant le nom ou un message d'échec
'''
@app.route('/user-name', methods=['POST'])
def user_name():
    user_id = request.json.get('user_id')
    reponse = obtenir_nom_utilisateur_par_id_utilisateur(user_id)
    if (reponse == "Utilisateur non trouvé"):
        return jsonify({"message": "User don't exist"})
    else : 
        return jsonify({"message": reponse})


'''
Renvoie la liste des groupes d'un user
Méthode POST : Argument : user_id
Retourne un json avec la liste, ou une liste vide en cas d'échec
'''
@app.route('/user-group', methods=['POST'])
def user_groupe():
    user_id = request.json.get('user_id')
    liste = groupesUtilisateurParIdUtilisateur(user_id)
    return jsonify({"liste": liste})

'''
Renvoie la liste des groupes d'un user (id + nom)
Méthode POST : Argument : group_id
Retourne un json avec la liste, ou une liste vide en cas d'échec
'''
@app.route('/liste-user-group', methods=['POST'])
def liste_user_groupe():
    group_id = request.json.get('group_id')
    liste_user = utilisateursParIdGroupe(group_id)
    if liste:
        return jsonify({"liste": liste})
    else : 
        return jsonify({"liste": "Id group does not exist"})

'''
#Vérifie si un utilisateur est l'admin du goupe (user_id, group_id)
@app.route('/admin-group', methods=['POST'])
def admin_group():
    group_id = request.json.get('group_id')
    user_id = request.json.get('user_id')
    test = estAdminDuGroupe(user_id, group_id)
    if(test):
        return jsonify({"message": "User is admin"})
    else:
        return jsonify({"message": "User is not admin"})
'''

'''
#Renvoie le nom du groupe à partir de son id (group_id)
@app.route('/name-group', methods=['POST'])
def name_group():
    group_id = request.json.get('group_id')
    nom_groupe = nomDuGroupeParId(group_id)
    if (nom_groupe != None):
        return jsonify({"name": nom_groupe})
    else : 
        return jsonify({"name": "Group does not exist"})
'''

'''
Ajoute un user a un groupe et ajoute le groupe dans la liste de l'user
Méthode POST : Argument : user_id et group_id
Retourne un json avec un message d'information 
'''
@app.route('/ajout-user-group', methods=['POST'])
def ajout_user_group():
    group_id = request.json.get('group_id')
    user_id = request.json.get('user_id')
    etat = ajoutUtilisateurGroupe(group_id, user_id)
    if (etat == 0):
        return jsonify({"message": "Utilisateur ajouté au groupe"}), 201
    elif (etat == 2):
        return jsonify({"message": "Utilisateur déja dans le groupe"})
    else :
        return jsonify({"message": "Id du groupe n'existe pas"})

'''
Supprime un groupe et son appariton dans la liste des groupes des user
Méthode POST : Argument : group_id
Retourne un json avec un message d'information 
'''
@app.route('/delete-group', methods=['POST'])
def delete_group():
    group_id = request.json.get('group_id')
    etat = supprimeGroupe(group_id)
    if (etat == 0):
        return jsonify({"message": "Groupe supprimé"})
    else : 
        return jsonify({"message": "Le group n'existe pas"})

'''
Renvoie le nom du groupe, la liste des users et si l'user est admin
Méthode POST : Argument : user_id, group_id
Retourne un json avec les données ou un json avec None en name si le groupe n'existe pas 
'''
@app.route('/info-group', methods=['POST'])
def info_group():
    group_id = request.json.get('group_id')
    user_id = request.json.get('user_id')
    nom_groupe = nomDuGroupeParId(group_id)
    if (nom_groupe != None):
        admin = estAdminDuGroupe(user_id, group_id)
        liste_user = utilisateursParIdGroupe(group_id)
        return jsonify({"name": nom_groupe, "liste": liste_user, "admin": admin})
    else :
        return jsonify({"name": None})

'''
Renvoie la liste de tout les events d'un groupe 
Méthode POST : Argument : group_id
Retourne un json avec la liste ou une liste vide si le groupe n'existe pas 
'''
#Renvoie tout les events d'un groupe (group_id)
@app.route('/liste-event-group', methods=['POST'])
def liste_event_group():
    group_id = request.json.get('group_id')
    liste_event = liste_evenements_groupe(group_id)
    return jsonify({"liste": liste_event})

'''
Renvoie la liste de tout les events d'un user 
Méthode POST : Argument : user_id
Retourne un json avec la liste ou une liste vide si l'user n'existe pas 
'''
#Renvoie tout les events d'un user (user_id)
@app.route('/liste-event-user', methods=['POST'])
def liste_event_user():
    user_id = request.json.get('user_id')
    liste_event = liste_full_events(user_id)
    return jsonify({"liste": liste_event})

'''
Ajoute un event a un groupe
Méthode POST : Argument : group_id et json 
Retourne un json avec un message de succès ou d'échec
'''
#Ajoute un event a un groupe (group_id, json)
@app.route('/add-event-group', methods=['POST'])
def add_event_group():
    group_id = request.json.get('group_id')
    event = request.json.get('json')
    etat = ajouter_evenement_groupe(event, group_id)
    if (etat == 0):
        return jsonify({"message": "Event ajouté"})
    else :
        return jsonify({"message": "Impossible d'ajouter l'event à ce groupe"})

'''
Ajoute un event a un user
Méthode POST : Argument : user_id et json 
Retourne un json avec un message de succès ou d'échec
'''
#Ajoute un event a un user (user_id, json)
@app.route('/add-event-user', methods=['POST'])
def add_event_user():
    user_id = request.json.get('user_id')
    event = request.json.get('json')
    etat = ajouter_evenement_user(event, user_id)
    if (etat == 0):
        return jsonify({"message": "Event ajouté"})
    else :
        return jsonify({"message": "Impossible d'ajouter l'event à ce groupe"})

if __name__ == '__main__':
    app.run(port=8000)