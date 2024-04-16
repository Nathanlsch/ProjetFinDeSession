from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import json
from ServiceBdd import * 

# Initialise l'app FireStore
cred = credentials.Certificate("ServicePython/config.json")
firebase_admin.initialize_app(cred)

# Initialise la base de donnée Firestore
db = firestore.client()

app = Flask(__name__)

#Ajoute un nouvel utilisateur a la base de donnée si il n'existe pas 
@app.route('/add-users', methods=['POST'])
def add_user():
    user_id = request.json.get('user_id')
    user_data = request.json.get('user_data')
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        return jsonify({"message": "User already exist"}), 201
    else:
        user_ref.set(user_data)
        return jsonify({"message": "User added successfully"}), 201

#Supprime un utilisateur de la base de donnée a partir de son id 
@app.route('/delete-users', methods=['POST'])
def delete_user():
    user_id = request.json.get('user_id')
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_ref.delete()
        return jsonify({"message": "User deleted successfully"}), 201
    else:
        return jsonify({"message": "User does not exist"}), 201


#Récupérer la liste des id de tout les utilisateurs 
@app.route('/liste-user')
def liste_user():
    user_ids = []
    docs = db.collection("users").stream()
    for doc in docs:
        user_ids.append(doc.id)
    return jsonify({"liste_user": user_ids})

#ajoute l'id d'un groupe a la liste des groupe d'un utilisateur
@app.route('/ajout-groupe', methods=['POST'])
def ajout_groupe():
    user_id = request.json.get('user_id')
    group_id = request.json.get('group_id')
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        groups = user_data.get("groupes", [])
        if group_id not in groups:
            groups.append(group_id)
            user_ref.update({"groupes": groups})
            return jsonify({"message": "Group added to user successfully"}), 201
        else:
            return jsonify({"message": "User already in the group"})
    else:
        return jsonify({"message": "User does not exist"})
