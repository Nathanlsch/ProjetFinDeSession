import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialise l'app FireStore
cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred)

# Initialise la base de donnée Firestore
db = firestore.client()

#----------------------Fonction permettant de manipuler la base de données-------------------------

'''
Ajoute un utilisateur dans la table "user"
Prend en argument l'identifiant d'un utilisateur et les données a stocké 
Renvoie 0 si succès, 1 si échec
'''
def ajoutUtilisateur(user_id, user_data):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        print(f"User '{user_id}' already exists.")
        return 1
    else:
        user_ref.set(user_data)
        print(f"User '{user_id}' added successfully.")
        return 0

'''
Supprime un utilisateur de la table "user"
Prend en argument l'identifiant d'un utilisateur 
Renvoie 0 si succès, 1 si échec
'''
def supprimeUtilisateur(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_ref.delete()
        print(f"User '{user_id}' deleted successfully.")
        return 0
    else:
        print(f"User '{user_id}' does not exist.")
        return 1

'''
Renvoie la liste de tout les id des user de la bdd
Ne prend pas d'argument
Renvoie la liste des id user
'''
def listeUtilisateur():
    user_ids = []
    docs = db.collection("users").stream()
    for doc in docs:
        user_ids.append(doc.id)
    return user_ids

'''
Ajoute un groupe dans la liste des groupes d'un utilisateur 
Prend en argument l'identifiant d'un utilisateur et l'identifiant du groupe
Renvoie 0 si ajout, 2 si le groupe est déja dans la liste, 1 si l'user n'existe pas 
'''
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
            return 0
        else:
            print(f"User '{user_id}' already belongs to group '{group_id}'.")
            return 2
    else:
        print(f"User '{user_id}' does not exist.")
        return 1

'''
Supprime un groupe dans la liste des groupes d'un utilisateur 
Prend en argument l'identifiant d'un utilisateur et l'identifiant du groupe
Renvoie 0 si supprésion, 2 si le groupe n'est pas dans la liste, 1 si l'user n'existe pas 
'''
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
            return 0
        else:
            print(f"User '{user_id}' does not belong to group '{group_id}'.")
            return 2
    else:
        print(f"User '{user_id}' does not exist.")
        return 1

'''
Créé un nouveau groupe et ajoute le groupe dans la liste des groupes du créateur
Prend en argument le nom du groupe et l'id de l'utilisateur 
Renvoie 0 si ajout dans la liste de l'user, 1 si l'user n'existe pas 
'''
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
    etat = ajoutGroupeUtilisateur(user_id, group_id)
    print(f"Groupe '{group_name}' ajouté avec succès.")
    return etat


'''
Ajoute un utilisateur a un groupe et ajoute le groupe àla liste de l'utilisateur
Prend en argument le nom du groupe et l'id de l'utilisateur 
Renvoie 0 si ajout, 2 si l'user est déja dans le groupe, 0 si le groupe n'existe pas  
'''
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
            return 0
        else:
            print(f"L'utilisateur '{user_id}' est déjà dans le groupe '{group_id}'.")
            return 2
    else:
        print(f"Le groupe '{group_id}' n'existe pas.")
        return 1

'''
Renvoie la liste des groupe d'un utilisateur (id_group + name_group)
Prend en argument l'id de l'user
Renvoie la liste des groupes ou une liste vide si l'user n'existe pas 
'''
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


'''
Renvoie la liste des nom des utilisateurs d'un groupe
Prend en argument l'id du groupe
Renvoie la liste des nom des user ou une liste vide si le groupe n'existe pas 
'''
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

'''
Vérifie sur un user est l'admin du groupe 
Prend en arguement l'id de l'user et l'id du groupe
Renvoie True(est admin) ou False(n'est pas admin ou le groupe n'existe pas)
'''
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

'''
Renvoie le nom d'un groupe via son id 
Prend en argument l'id du groupe 
Renvoie le nom du groupe ou "None" si le groupe n'existe pas
'''
def nomDuGroupeParId(group_id):
    group_ref = db.collection("groupes").document(group_id)
    group_doc = group_ref.get()
    if group_doc.exists:
        group_data = group_doc.to_dict()
        return group_data.get("name", "Unknown")
    else:
        print(f"Group '{group_id}' does not exist.")
        return None

'''
Supprime un groupe de la base de données et de la liste de tout les user du groupe
Prend en argument l'identifiant d'un groupe
Renvoie 0 si supprésion, 1 si le groupe n'existe pas
'''
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
        return 0
    else:
        print(f"Groupe '{group_id}' n'existe pas.")
        return 1

'''
Ajoute un événement à un groupe 
Prend en argument l'event au bon format json et l'id du groupe 
Renvoie 0 si l'evenement est ajouté, 1 sinon 
'''
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
        return 0
    else:
        print("Le groupe", group_id, "n'existe pas dans la base de données.")
        return 1

'''
Ajoute un événement à un user
Prend en argument l'event au bon format json et l'id de l'user
Renvoie 0 si l'evenement est ajouté, 1 sinon 
'''
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
        return 0
    else:
        print("Le groupe", user_id, "n'existe pas dans la base de données.")
        return 1

'''
Renvoie sous forme de liste tout les event d'un groupe 
Prend en argument l'id du groupe
Renvoie la liste si le groupe existe, une liste vide sinon
'''
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

'''
Renvoie sous forme de liste tout les event d'un user 
Prend en argument l'id de l'user
Renvoie la liste si l'user existe, une liste vide sinon
'''
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

'''
Renvoie sous forme de liste tout les event d'un user et des groupes auxquel il appartient
Prend en argument l'id de l'user
Renvoie la liste si l'user existe, une liste vide sinon
'''
def liste_full_events(user_id):
    liste_groupe = groupesUtilisateurParIdUtilisateur(user_id)
    liste_ids = [element['id'] for element in liste_groupe]
    events = liste_evenements_user(user_id)
    for group_id in liste_ids :
        events_groupe = liste_evenements_groupe(group_id)
        events.extend(events_groupe)
    return events

'''
Vérifie si un utilisateur existe
Prend en argument l'id de l'user
Renvoie True si il existe False sinon 
'''
def user_existe(document_id):
    # Référence du document dans la collection
    doc_ref = db.collection("users").document(document_id)
    # Vérifier si le document existe
    doc_exists = doc_ref.get().exists
    return doc_exists

'''
Renvoie le nom d'un user a partir de son id 
Prend en argument l'id de l'user
Renvoie le nom de l'utilisateur si le nom existe, "Utilisateur non trouvé" sinon
'''
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



