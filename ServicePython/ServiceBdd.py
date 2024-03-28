import firebase_admin
from firebase_admin import credentials, firestore

# Initialise l'app FireStore
cred = credentials.Certificate("ServicePython/config.json")
firebase_admin.initialize_app(cred)

# Initialise la base de donnée Firestore
db = firestore.client()

# Ajout utilisateur
def ajoutUtilisateur(document_id, document_data):
    db.collection("users").document(document_id).set(document_data)

# Function to delete a user
def supprimeUtilisateur(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_ref.delete()
        print(f"User '{user_id}' deleted successfully.")
    else:
        print(f"User '{user_id}' does not exist.")

def CreerDonneeUtilisateur(name, email, groups):
    user_data = {
        "name": name,
        "email": email,
        "groupes": groups
    }
    return user_data

#Récupérer la liste des id de tout les utilisateurs 
def listeUtilisateur(collection_name):
    user_ids = []
    docs = db.collection(collection_name).stream()
    for doc in docs:
        user_ids.append(doc.id)
    return user_ids

# Ajoute un groupe dans la liste d'un utilisateur 
def ajoutGroupeUtilisateur(user_id, group_name):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        groups = user_data.get("groupes", [])
        if group_name not in groups:
            groups.append(group_name)
            user_ref.update({"groupes": groups})
            print(f"Group '{group_name}' added to user '{user_id}' successfully.")
        else:
            print(f"User '{user_id}' already belongs to group '{group_name}'.")
    else:
        print(f"User '{user_id}' does not exist.")

# Supprime un groupe de la liste d'un utilisateur 
def supprimeGroupeUtilisateur(user_id, group_name):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        groups = user_data.get("groupes", [])
        if group_name in groups:
            groups.remove(group_name)
            user_ref.update({"groupes": groups})
            print(f"Group '{group_name}' removed from user '{user_id}' successfully.")
        else:
            print(f"User '{user_id}' does not belong to group '{group_name}'.")
    else:
        print(f"User '{user_id}' does not exist.")

# Renvoi tout les groupes d'un utilisateur 
def groupesUtilisateur(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        groups = user_data.get("groupes", [])
        return groups
    else:
        print(f"User '{user_id}' does not exist.")
        return []

# Fonction pour creer un nouveau groupe et ajoute le groupe au créataur 
def nouveauGroupe(group_name, user_id):
    group_data = {
        "name": group_name,
        "admin" : user_id,
        "users": [user_id]
    }
    ajoutGroupeUtilisateur(user_id,group_name)
    db.collection("groupes").add(group_data)
    print(f"Groupe '{group_name}' ajouté avec succès.")

def ajoutUtilisateurGroupe(group_name, user_id):
    group_ref = db.collection("groupes").where("name", "==", group_name).limit(1).get()
    if group_ref:
        for group_doc in group_ref:
            group_data = group_doc.to_dict()
            users = group_data.get("users", [])
            if user_id not in users:
                users.append(user_id)
                group_doc.reference.update({"users": users})
                ajoutGroupeUtilisateur(user_id,group_name)
                print(f"Utilisateur '{user_id}' ajouté au groupe '{group_name}' avec succès.")
            else:
                print(f"L'utilisateur '{user_id}' est déjà dans le groupe '{group_name}'.")
    else:
        print(f"Le groupe '{group_name}' n'existe pas.")

