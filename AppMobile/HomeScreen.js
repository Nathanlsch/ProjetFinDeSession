import React, { useState } from 'react';
import { View, Text, StyleSheet, Button, Dimensions, Alert, TextInput, TouchableOpacity, ScrollView, RefreshControl } from 'react-native';
import EventCalendar from 'react-native-events-calendar';
import { Clipboard} from 'react-native';
import API_URL from './config';

const HomeScreen = ({ userId, username, groupList, setGroupList, setUserId, setLoggedIn, setUsername}) => {

  //Variable pour l'interface 
  const [showCalendar, setShowCalendar] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [events, setEvents] = useState([]);
  const [newGroupName, setNewGroupName] = useState('');
  const [Titre, setTitre] = useState('');
  const [Date, setDate] = useState('');
  const [HeureDebut, setHeureDebut] = useState('');
  const [HeureFin, setHeureFin] = useState('');
  const [Titre2, setTitre2] = useState('');
  const [Date2, setDate2] = useState('');
  const [HeureDebut2, setHeureDebut2] = useState('');
  const [HeureFin2, setHeureFin2] = useState('');
  const [groupeAdd, setGroupAdd] = useState('');
  const [refreshing, setRefreshing] = useState(false); // Ajout de refreshing

  //Pour gérer la dimension du calendrier 
  const { width, height } = Dimensions.get('window');
  const calendarMarginTop = 50; // Ajustez cette valeur selon vos besoins
  const calendarContainerHeight = height- 2*calendarMarginTop; // Ajustez cette valeur selon vos besoins

  //Requete pour creer un groupe 
  const handleCreateGroup = () => {

    if (!newGroupName.trim()) {
      Alert.alert('Erreur', 'Veuillez entrer un nom de groupe');
      return;
    }

    fetch(`${API_URL}/creer-groupe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        group_name: newGroupName,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.message === 'Groupe ajouté') {
          // Mettre à jour la liste des groupes de l'utilisateur
          setGroupList(data.listeGroupe)
          setNewGroupName('');
          Alert.alert('Succès', 'Groupe créé avec succès.');
        } else {
          Alert.alert('Erreur', 'Échec de la création du groupe.');
        }
      })
      .catch((error) => {
        console.error('Erreur:', error);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete pour rejoindre un groupe 
  const handleJoinGroup = () => {

    if (!groupeAdd.trim()) {
      Alert.alert('Erreur', 'Veuillez entrer un identifiant de groupe');
      return;
    }

    fetch(`${API_URL}/rejoindre-groupe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        group_id: groupeAdd,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.message === 'Utilisateur ajouté au groupe') {
          // Mettre à jour la liste des groupes de l'utilisateur
          setGroupList(data.listeGroupe)
          setGroupAdd('');
          Alert.alert(data.message);
        } else {
          Alert.alert('Erreur', data.message);
        }
      })
      .catch((error) => {
        console.error('Erreur:', error);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Fonction pour afficher ou cacher le calendrier 
  const handleToggleCalendar = () => {
    setShowCalendar(!showCalendar);
  };

  //Requete recuperer les events afficher le calendrier d'un utilisateur 
  const handleCalendar = () => {
    fetch(`${API_URL}/calendrier-user`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.events) {
          setEvents(data.events)
          setShowCalendar(!showCalendar);
        } 
      })
      .catch((error) => {
        console.error('Erreur:', error);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete pour recuperer les events et afficher le calendrier d'un groupe 
  const handleCalendarGroup = () => {
    fetch(`${API_URL}/calendrier-groupe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        group_id: selectedGroup.id,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.events) {
          setEvents(data.events)
          setShowCalendar(!showCalendar);
        } 
      })
      .catch((error) => {
        console.error('Erreur:', error);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete pour récuperer les inforamtions d'un groupe et afficher la page d'information 
  const handleGroupPress = (groupId) => {
    fetch(`${API_URL}/groupe-details`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        group_id: groupId,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.message == "Info Groupe") {
          setSelectedGroup({
            id: groupId,
            nom: data.group_name,
            listeUser: data.user_list,
            admin: data.test_admin
          });
          setShowCalendar(false);
        } else {
          setGroupList(prevList => prevList.filter(groupe => groupe.id !== groupId));
          setSelectedGroup(null);
          Alert.alert("Le groupe n'est plus disponible");
        }
      })
      .catch((error) => {
        console.error('Erreur:', error);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete pour ajouter un event a un utilisateur 
  const handleAddEventUser = () => {

    if (!Titre.trim()) {
      Alert.alert('Erreur', "Veuillez entrer un nom d'évènement");
      return;
    }

    fetch(`${API_URL}/sauvegarder-creneau-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        titre : Titre,
        date : Date,
        heure_debut : HeureDebut,
        heure_fin : HeureFin
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.message == "Créneau ajouté avec succès !") {
          Alert.alert("Créneau ajouté avec succès !")
          setTitre('')
          setDate('')
          setHeureDebut('')
          setHeureFin('')
        } else {
          Alert.alert(data.message)
        }
      })
      .catch((error) => {
        console.error('Erreur:', data.message);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete ajouter un event a un groupe 
  const handleAddEventGroupe = () => {

    if (!Titre2.trim()) {
      Alert.alert('Erreur', "Veuillez entrer un nom d'évènement");
      return;
    }

    fetch(`${API_URL}/sauvegarder-creneau`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        titre : Titre2,
        date : Date2,
        heure_debut : HeureDebut2,
        heure_fin : HeureFin2,
        group_id : selectedGroup.id
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.message == "Créneau ajouté avec succès !") {
          Alert.alert("Créneau ajouté avec succès !")
          setTitre2('')
          setDate2('')
          setHeureDebut2('')
          setHeureFin2('')
        } else {
          Alert.alert(data.message)
        }
      })
      .catch((error) => {
        console.error('Erreur:', data.message);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete pour se déconnecter 
  const deconnexion = () => {
    fetch(`${API_URL}/deconnexion`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === 'Déconnexion') {
          // Réinitialisation des variables d'état
          setLoggedIn(false);
          setUserId('');
          setUsername('');
          setGroupList([]);
        } else {
          Alert.alert('Erreur', 'Erreur lors de la déconnexion. Veuillez réessayer.');
        }
      })
      .catch((error) => {
        console.error('Erreur:', data.message);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete pour supprimer un groupe si on en est l'admin 
  const supprimer_groupe = () => {
    fetch(`${API_URL}/supprime-groupe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        group_id: selectedGroup.id,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
          setGroupList(data.listeGroupe)
          setSelectedGroup(null)
      })
      .catch((error) => {
        console.error('Erreur:', data.message);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Requete pour quitter un groupe 
  const quitter_groupe = () => {
    fetch(`${API_URL}/quitter-groupe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        group_id: selectedGroup.id,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
          setGroupList(data.listeGroupe)
          setSelectedGroup(null)
      })
      .catch((error) => {
        console.error('Erreur:', data.message);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  //Fonction pour copie dans le presse papier l'id d'un groupe 
  const handleCopyGroupId = () => {
    if (selectedGroup) {
      Clipboard.setString(selectedGroup.id);
      Alert.alert('Succès', 'Identifiant du groupe copié dans le presse-papiers');
    }
  };

  //Requete pour rafraichir la page d'acceuil 
  const refreshPage = () => {
    setRefreshing(true);
    // Effectuez ici la requête pour obtenir les données de l'utilisateur
    fetch(`${API_URL}/login-app`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userId: userId,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        /*if (data.message === 'Authentification réussie') {
          onLogin(userId,data.nom,data.listeGroupe);
        } else {
          Alert.alert('Erreur', 'Identifiant incorrect');
        }*/
        if (data.message === 'Authentification réussie') {
          setUsername(data.nom);
          setGroupList(data.listeGroupe);
          setLoggedIn(true);
        } else {
          // Déconnexion en cas d'échec de connexion
          setLoggedIn(false);
          setUserId('');
          setUsername('');
          setGroupList([]);
        }
        setRefreshing(false);
      })
      .catch((error) => {
        console.error('Erreur:', error);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
    };


  return (
    <View style={styles.container}>
      {!showCalendar && !selectedGroup ? ( //Si on ne veux pas afficher de calendrier ni de groupe alors on affiche la page d'accueil 
        <View style={styles.container}>
          <Text style={styles.welcome}>Bienvenue, {username}!</Text>
          <ScrollView 
            refreshControl={
              <RefreshControl
                refreshing={refreshing}
                onRefresh={refreshPage}
              />
            } 
            showsVerticalScrollIndicator={false}> 
            
            <View style={styles.section}> 
                <Text style={styles.sectionTitle}>Ajouter un événement au calendrier</Text> 
                <TextInput //Section pour ajouter saisir les information d'un event de l'utilisateur 
                  style={styles.input_events}
                  placeholder="Titre de l'événement"
                  onChangeText={(text) => setTitre(text)}
                  value={Titre}
                />
                <TextInput
                  style={styles.input_events}
                  placeholder="Date (YYYY-MM-DD)"
                  onChangeText={(text) => setDate(text)}
                  value={Date}
                />
                <TextInput
                  style={styles.input_events}
                  placeholder="Heure de début (HH:MM)"
                  onChangeText={(text) => setHeureDebut(text)}
                  value={HeureDebut}
                />
                <TextInput
                  style={styles.input_events}
                  placeholder="Heure de fin (HH:MM)"
                  onChangeText={(text) => setHeureFin(text)}
                  value={HeureFin}
                />
                <TouchableOpacity
                  style={styles.button}
                  onPress={handleAddEventUser}
                >
                  <Text style={styles.buttonText}>Envoyer</Text>
                </TouchableOpacity>
              </View>
            
    
            <View style={styles.section}> 
              <Text style={styles.sectionTitle}>Créer un nouveau groupe</Text>
              <View style={styles.inputContainer}>
                <TextInput //Section pour creer un nouveau groupe 
                  style={styles.input}
                  placeholder="Nom du nouveau groupe"
                  onChangeText={(text) => setNewGroupName(text)}
                  value={newGroupName}
                />
                <TouchableOpacity
                  style={styles.button}
                  onPress={handleCreateGroup}
                >
                  <Text style={styles.buttonText}>Créer un groupe</Text>
                </TouchableOpacity>
              </View>
            </View>

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Rejoindre un groupe</Text>
              <View style={styles.inputContainer}>
                <TextInput //Section pour rejoindre un groupe 
                  style={styles.input}
                  placeholder="Identifiant du groupe"
                  onChangeText={(text) => setGroupAdd(text)}
                  value={groupeAdd}
                />
                <TouchableOpacity
                  style={styles.button}
                  onPress={handleJoinGroup}
                >
                  <Text style={styles.buttonText}>Rejoindre groupe</Text>
                </TouchableOpacity>
              </View>
            </View>
    
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Vos groupes :</Text>
              <ScrollView style={styles.groupList} showsVerticalScrollIndicator={false}>
                {groupList.map((groupe) => ( //Affiche la liste des groupes de l'user 
                  <TouchableOpacity
                    key={groupe.id}
                    onPress={() => handleGroupPress(groupe.id)}
                    style={styles.groupButton}
                  >
                    <Text>{groupe.name}</Text>
                  </TouchableOpacity>
                ))}
              </ScrollView>
            </View>
    
            <View> 
              <TouchableOpacity //Affiche un bouton pour pouvoir afficher le calendrier de l'utilisateur 
                style={styles.button2}
                onPress={handleCalendar}
              > 
                <Text style={styles.buttonText}>Mon Calendrier</Text>
              </TouchableOpacity> 
            </View>
            
            <View>
              <TouchableOpacity // Bouton de déconnexion 
                style={styles.button3}
                onPress={deconnexion}
              >
                <Text style={styles.buttonText}>Déconnexion</Text>
              </TouchableOpacity>
            </View>
          </ScrollView>
        </View>
      ) : showCalendar ? ( // Page d'affichage du calendrier  
        <View style={{ flex: 1 }}>
          <View style={[styles.calendarContainer, { height: calendarContainerHeight, marginTop: calendarMarginTop }]}>
            <EventCalendar
              eventTapped={() => {}}
              events={events}
              width={width}
              height={calendarContainerHeight}
              initDate={'2024-04-25'}
            />
            <Button
              title="Retour"
              onPress={handleToggleCalendar}
            />
          </View>
        </View>
      ) : selectedGroup ? ( //Page d'information sur un groupe 
        <View style={styles.containerGroupe}>
          <Text style={styles.welcome}>Details du groupe: {selectedGroup.nom}</Text>
          <Text style={styles.sectionTitle}>Identifiant: "
            <TouchableOpacity onPress={handleCopyGroupId}>
                <Text style={styles.copyText}>{selectedGroup.id}</Text>
            </TouchableOpacity>
          "</Text>
          <Text style={styles.sectionTitle}>Liste utilisateurs:</Text>
          <View style={styles.userListContainer}>
              {selectedGroup.listeUser.map((user, index) => (
                <Text key={index} style={styles.userItem}>{user}</Text>
              ))}
          </View>
          <TouchableOpacity
            style={styles.button2}
            onPress={handleCalendarGroup}
          >
            <Text style={styles.buttonText}>Calendrier du groupe</Text>
          </TouchableOpacity>
           <View style={styles.section}>
            <Text style={styles.sectionTitle}>Ajouter un événement au calendrier du groupe</Text>
            <TextInput
              style={styles.input_events}
              placeholder="Titre de l'événement"
              onChangeText={(text) => setTitre2(text)}
              value={Titre2}
            />
            <TextInput
              style={styles.input_events}
              placeholder="Date (YYYY-MM-DD)"
              onChangeText={(text) => setDate2(text)}
              value={Date2}
            />
            <TextInput
              style={styles.input_events}
              placeholder="Heure de début (HH:MM)"
              onChangeText={(text) => setHeureDebut2(text)}
              value={HeureDebut2}
            />
            <TextInput
              style={styles.input_events}
              placeholder="Heure de fin (HH:MM)"
              onChangeText={(text) => setHeureFin2(text)}
              value={HeureFin2}
            />
            <TouchableOpacity
              style={styles.button}
              onPress={handleAddEventGroupe}
            >
              <Text style={styles.buttonText}>Envoyer</Text>
            </TouchableOpacity>
          </View>
            {selectedGroup.admin ? (
              <TouchableOpacity
                style={styles.button3}
                onPress={supprimer_groupe}
              >
                <Text style={styles.buttonText}>Supprimer Groupe</Text>
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                style={styles.button3}
                onPress={quitter_groupe}
              >
                <Text style={styles.buttonText}>Quitter le groupe</Text>
              </TouchableOpacity>
            )}
          <Button title="Retour" onPress={() => setSelectedGroup(null)} />
        </View>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({ //Style de la page 
  container: {
    flex: 1,
    padding: 3,
    paddingTop: 20,
  },
  containerGroupe: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  containerCalendar: {
    flex: 1,
    paddingTop: 20
  },
  scrollContainer: {
    flexGrow: 1,
  },
  welcome: {
    fontSize: 25,
    marginBottom: 20,
    textAlign: 'center',
  },
  section: {
    marginBottom: 10,
    backgroundColor: '#f5f5f5',
    padding: 10,
    borderRadius: 10,
  },
  sectionTitle: {
    fontSize: 16,
    marginBottom: 10,
    textAlign: 'center',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  groupButton: {
    backgroundColor: '#e0e0e0',
    padding: 10,
    marginBottom: 5,
    minWidth: 150,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
  },
  groupList: {
    maxHeight: 200,
  },
  input_events: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  logoutButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: 'red',
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 20,
    marginBottom: 10,
  },
  button2: {
    backgroundColor: '#414246',
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 20,
    marginBottom: 10,
  },
  button3: {
    backgroundColor: '#DB2418',
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 20,
    marginBottom: 10,
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
  },
  userListContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  userItem: {
    padding: 5,
    marginBottom: 5,
    minWidth: 100,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
    marginBottom: 10,
  },
});


export default HomeScreen;
