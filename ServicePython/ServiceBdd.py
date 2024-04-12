import firebase_admin
from firebase_admin import credentials, firestore

# Initialise l'app FireStore
cred = credentials.Certificate("ServicePython/config.json")
firebase_admin.initialize_app(cred)

# Initialise la base de donnée Firestore
db = firestore.client()

# Ajout utilisateur
def ajoutUtilisateur(document_id, document_data):
    user_ref = db.collection("users").document(document_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        print(f"User '{document_id}' already exists.")
    else:
        user_ref.set(document_data)
        print(f"User '{document_id}' added successfully.")

# Function to delete a user
def supprimeUtilisateur(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_ref.delete()
        print(f"User '{user_id}' deleted successfully.")
    else:
        print(f"User '{user_id}' does not exist.")

def CreerDonneeUtilisateur(name):
    user_data = {
        "name": name,
        "groupes": []
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
def ajoutGroupeUtilisateur(user_id, group_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        groups = user_data.get("groupes", [])
        if group_id not in groups:
            groups.append(group_id)
            user_ref.update({"groupes": groups})
            print(f"Group '{group_id}' added to user '{user_id}' successfully.")
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
    #Ajoute le groupe au tableau des groupes dans la bdd

    group_ref = db.collection("groupes").add(group_data)

    group_id = group_ref[1].id

    ajoutGroupeUtilisateur(user_id, group_id)
    
    print(f"Groupe '{group_name}' ajouté avec succès.")

def ajoutUtilisateurGroupe(group_id, user_id):
    group_ref = db.collection("groupes").document(group_id)
    group_doc = group_ref.get()
    if group_doc.exists:
        group_data = group_doc.to_dict()
        users = group_data.get("users", [])
        if user_id not in users:
            users.append(user_id)
            group_doc.reference.update({"users": users})
            ajoutGroupeUtilisateur(user_id,group_name)
            print(f"Utilisateur '{user_id}' ajouté au groupe '{group_id}' avec succès.")
        else:
            print(f"L'utilisateur '{user_id}' est déjà dans le groupe '{group_id}'.")
    else:
        print(f"Le groupe '{group_id}' n'existe pas.")


def groupesUtilisateurParIdUtilisateur(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        group_names_ids = []
        group_ids = user_data.get("groupes", [])
        for group_id in group_ids:
            group_ref = db.collection("groupes").document(group_id)
            group_doc = group_ref.get()
            if group_doc.exists:
                group_data = group_doc.to_dict()
                group_info = {"id": group_id, "name": group_data.get("name", "Unknown")}
                group_names_ids.append(group_info)
            else:
                print(f"Group '{group_id}' does not exist.")
        return group_names_ids
    else:
        print(f"User '{user_id}' does not exist.")
        return []

def utilisateursParIdGroupe(group_id):
    group_ref = db.collection("groupes").document(group_id)
    group_doc = group_ref.get()
    if group_doc.exists:
        group_data = group_doc.to_dict()
        user_ids = group_data.get("users", [])
        user_names = []
        for user_id in user_ids:
            user_ref = db.collection("users").document(user_id)
            user_doc = user_ref.get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                user_name = user_data.get("name", "Unknown")
                user_names.append(user_name)
            else:
                print(f"User '{user_id}' does not exist.")
        return user_names
    else:
        print(f"Group '{group_id}' does not exist.")
        return []

def estAdminDuGroupe(user_id, group_id):
    group_ref = db.collection("groupes").document(group_id)
    group_doc = group_ref.get()
    if group_doc.exists:
        group_data = group_doc.to_dict()
        admin_id = group_data.get("admin")
        return user_id == admin_id
    else:
        print(f"Group '{group_id}' does not exist.")
        return False

def nomDuGroupeParId(group_id):
    group_ref = db.collection("groupes").document(group_id)
    group_doc = group_ref.get()
    if group_doc.exists:
        group_data = group_doc.to_dict()
        return group_data.get("name", "Unknown")
    else:
        print(f"Group '{group_id}' does not exist.")
        return None

def supprimeGroupe(group_id):
    # Supprimer le groupe de la collection "groupes"
    group_ref = db.collection("groupes").document(group_id)
    group_doc = group_ref.get()
    if group_doc.exists:
        group_data = group_doc.to_dict()
        
        # Supprimer le groupe de chaque utilisateur qui y appartient
        users = group_data.get("users", [])
        for user_id in users:
            supprimeGroupeUtilisateur(user_id, group_id)
        
        # Supprimer le groupe de la collection "groupes"
        group_ref.delete()
        print(f"Groupe '{group_id}' supprimé avec succès.")
    else:
        print(f"Groupe '{group_id}' n'existe pas.")