import requests

# URL de base de votre API Flask
base_url = 'http://127.0.0.1:5000'

# Endpoint pour ajouter un utilisateur
add_user_endpoint = '/ajout-utilisateur'

# Données JSON pour ajouter un utilisateur
user_data = {
    'user_id': 'unique_user_id',
    'user_data': {
        "name": "name_test",
        "groupes": [],
        "events" : []
    }
}



# Envoi de la requête POST pour ajouter un utilisateur
response = requests.post(base_url + add_user_endpoint, json=user_data)
print(response.json())  # Afficher la réponse JSON du serveur

'''

# Endpoint pour supprimer un utilisateur
delete_user_endpoint = '/supprime-utilisateur'

# Données JSON pour supprimer un utilisateur
delete_user_data = {
    'user_id': 'unique_user_id'
}


# Envoi de la requête POST pour supprimer un utilisateur
response = requests.post(base_url + delete_user_endpoint, json=delete_user_data)
print(response.json())  # Afficher la réponse JSON du serveur



# Endpoint pour lister les utilisateurs
list_users_endpoint = '/liste-utilisateurs'

# Envoi de la requête GET pour lister les utilisateurs
response = requests.get(base_url + list_users_endpoint)
print(response.json())  # Afficher la réponse JSON du serveur


# Endpoint pour créer un nouveau groupe
create_group_endpoint = '/nouveau-groupe'

# Données JSON pour créer un nouveau groupe
group_data = {
    'group_name': 'New Group',
    'user_id': 'unique_user_id'
}

# Envoi de la requête POST pour créer un nouveau groupe
response = requests.post(base_url + create_group_endpoint, json=group_data)
print(response.json())  # Afficher la réponse JSON du serveur



# Endpoint pour créer un nouveau groupe
ajout_group_endpoint = '/ajout-groupe-utilisateur'

# Données JSON pour créer un nouveau groupe
data = {
    'group_id': 'YJpnLyhp3rrUwI4aKyFA',
    'user_id': 'unique_user_id'
}

# Envoi de la requête POST pour créer un nouveau groupe
response = requests.post(base_url + ajout_group_endpoint, json=data)
print(response.json())  # Afficher la réponse JSON du serveur
'''

# Endpoint pour créer un nouveau groupe
ajout_group_endpoint = '/supprime-groupe-utilisateur'

# Données JSON pour créer un nouveau groupe
data = {
    'group_id': '2DxFdqSuWURVldYfxUxu',
    'user_id': 'unique_user_id'
}

# Envoi de la requête POST pour créer un nouveau groupe
response = requests.post(base_url + ajout_group_endpoint, json=data)
print(response.json())  # Afficher la réponse JSON du serveur

