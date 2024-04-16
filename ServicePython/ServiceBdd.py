import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialise l'app FireStore
cred = credentials.Certificate("ServicePython/config.json")
firebase_admin.initialize_app(cred)

# Initialise la base de donnée Firestore
db = firestore.client()

# Ajout utilisateur
def ajoutUtilisateur(user_id, user_data):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        print(f"User '{user_id}' already exists.")
    else:
        user_ref.set(user_data)
        print(f"User '{user_id}' added successfully.")

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
        "groupes": [],
        "events" : []
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
            print(f"User '{user_id}' already belongs to group '{group_id}'.")
    else:
        print(f"User '{user_id}' does not exist.")

# Supprime un groupe de la liste d'un utilisateur 
def supprimeGroupeUtilisateur(user_id, group_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        groups = user_data.get("groupes", [])
        if group_id in groups:
            groups.remove(group_id)
            user_ref.update({"groupes": groups})
            print(f"Group '{group_id}' removed from user '{user_id}' successfully.")
        else:
            print(f"User '{user_id}' does not belong to group '{group_id}'.")
    else:
        print(f"User '{user_id}' does not exist.")

# Fonction pour creer un nouveau groupe et ajoute le groupe au créataur 
def nouveauGroupe(group_name, user_id):
    group_data = {
        "name": group_name,
        "admin" : user_id,
        "users": [user_id],
        "events" : []
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
            ajoutGroupeUtilisateur(user_id, group_id)
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

def ajouter_evenement_groupe(event_json, group_id):
    # Convertir l'objet JSON en dictionnaire Python
    event_data = json.loads(event_json)
        
    # Référence du groupe dans la base de données
    group_ref = db.collection("groupes").document(group_id)
        
    # Obtenir le document du groupe
    group_doc = group_ref.get()
        
    # Vérifier si le groupe existe dans la base de données
    if group_doc.exists:
        # Obtenir les données du groupe
        group_data = group_doc.to_dict()
            
        # Obtenir la liste des événements actuels du groupe
        events = group_data.get("events", [])
            
        # Ajouter le nouvel événement à la liste des événements
        events.append(event_data)
            
        # Mettre à jour les données du groupe avec la nouvelle liste d'événements
        group_ref.update({"events": events})
            
        print("Événement ajouté avec succès au groupe", group_id)
    else:
        print("Le groupe", group_id, "n'existe pas dans la base de données.")

def ajouter_evenement_user(event_json, user_id):
    # Convertir l'objet JSON en dictionnaire Python
    event_data = json.loads(event_json)
        
    # Référence de l'user dans la base de données
    user_ref = db.collection("users").document(user_id)
        
    # Obtenir le document de l'user
    user_doc = user_ref.get()
        
    # Vérifier si l'user existe dans la base de données
    if user_doc.exists:
        # Obtenir les données du groupe
        user_data = user_doc.to_dict()
            
        # Obtenir la liste des événements actuels du groupe
        events = user_data.get("events", [])
            
        # Ajouter le nouvel événement à la liste des événements
        events.append(event_data)
            
        # Mettre à jour les données du groupe avec la nouvelle liste d'événements
        user_ref.update({"events": events})
            
        print("Événement ajouté avec succès au groupe", user_id)
    else:
        print("Le groupe", user_id, "n'existe pas dans la base de données.")

def liste_evenements_groupe(group_id):
    # Référence du groupe dans la base de données
    group_ref = db.collection("groupes").document(group_id)
    
    # Obtenir le document du groupe
    group_doc = group_ref.get()
    
    # Vérifier si le groupe existe dans la base de données
    if group_doc.exists:
        # Obtenir les données du groupe
        group_data = group_doc.to_dict()
        
        # Obtenir la liste des événements du groupe
        events = group_data.get("events", [])
        
        # Retourner la liste des événements (convertis en JSON)
        return events
    else:
        print("Le groupe", group_id, "n'existe pas dans la base de données.")
        return []

def liste_evenements_user(user_id):
    # Référence du groupe dans la base de données
    user_ref = db.collection("users").document(user_id)
    
    # Obtenir le document du groupe
    user_doc = user_ref.get()
    
    # Vérifier si le groupe existe dans la base de données
    if user_doc.exists:
        # Obtenir les données du groupe
        user_data = user_doc.to_dict()
        
        # Obtenir la liste des événements du groupe
        events = user_data.get("events", [])
        
        # Retourner la liste des événements (convertis en JSON)
        return events
    else:
        print("Le groupe", user_id, "n'existe pas dans la base de données.")
        return []

def user_existe(document_id):
    # Référence du document dans la collection
    doc_ref = db.collection("users").document(document_id)
    
    # Vérifier si le document existe
    doc_exists = doc_ref.get().exists
    
    return doc_exists

def obtenir_nom_utilisateur_par_id_utilisateur(user_id):
    # Référence du document utilisateur dans la collection "users"
    user_ref = db.collection("users").document(user_id)
    
    # Obtenir le document de l'utilisateur
    user_doc = user_ref.get()
    
    # Vérifier si le document de l'utilisateur existe
    if user_doc.exists:
        # Obtenir les données de l'utilisateur sous forme de dictionnaire
        user_data = user_doc.to_dict()
        
        # Extraire le nom de l'utilisateur à partir des données
        nom_utilisateur = user_data.get("name", "Nom inconnu")
        
        return nom_utilisateur
    else:
        # Si l'utilisateur n'existe pas, retourner une valeur par défaut
        return "Utilisateur non trouvé"



