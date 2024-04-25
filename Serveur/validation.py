from datetime import datetime
import html

def escape_injection(input_string):
    """
    Échappe les caractères spéciaux dans une chaîne de caractères pour éviter les injections de code.
    Args:
    input_string (str): La chaîne de caractères à échapper.
    Returns:
    str: La chaîne de caractères échappée.
    """
    return html.escape(input_string)

def sauvegarder_creneau_variables_validation(titre, date, heure_debut, heure_fin, group_id):
    # Vérifier si le titre est une chaîne
    if not isinstance(titre, str):
        return [False, "Le titre doit être du texte."]
    
    # Vérifier si la date est une date valide
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return [False, "La date n'est pas valide."]

    # Vérifier si heure_debut et heure_fin sont des heures valides et si heure_fin est supérieure à heure_debut
    try:
        heure_debut = datetime.strptime(heure_debut, '%H:%M')
        heure_fin = datetime.strptime(heure_fin, '%H:%M')
        if heure_fin <= heure_debut:
            return [False, "heure_fin doit être supérieure à heure_debut."]
    except ValueError:
        return [False, "heure_debut ou heure_fin n'est pas valide."]

    
    # Si toutes les vérifications passent
    return [True, "Toutes les variables sont valides."]

