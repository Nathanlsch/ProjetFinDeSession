import React, { useState } from 'react';
import { View, TextInput, StyleSheet, Alert, TouchableOpacity, Text} from 'react-native';
import API_URL from './config';

const LoginScreen = ({ onLogin }) => {
  const [userId, setUserId] = useState('');

  const handleLogin = () => {

    if (!userId.trim()) {
        Alert.alert('Erreur', 'Veuillez entrer votre identifiant.');
        return;
    }

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
        if (data.message === 'Authentification réussie') {
          onLogin(userId,data.nom,data.listeGroupe);
        } else {
          Alert.alert('Erreur', 'Identifiant incorrect');
        }
      })
      .catch((error) => {
        console.error('Erreur:', error);
        Alert.alert('Erreur', 'Une erreur s\'est produite. Veuillez réessayer.');
      });
  };

  return (
    <View style={styles.container}>
    
    <TextInput
      style={styles.input}
      placeholder="Entrez votre identifiant"
      value={userId}
      onChangeText={text => setUserId(text)}
    />
    <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
      <Text style={styles.buttonText}>Se connecter</Text>
    </TouchableOpacity>
    <TouchableOpacity style={styles.registerLink} onPress={() => Alert.alert("Pour pouvoir se connecter, il vous faut avoir récupéré votre identifiant depuis la page Web de l'application")}>
      <Text style={styles.registerText}>Vous n'avez pas d'identifiant ?</Text>
    </TouchableOpacity>
  </View>
  );
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      paddingHorizontal: 20,
      backgroundColor: '#fff',
    },
    logo: {
      width: 150,
      height: 150,
      marginBottom: 40,
    },
    input: {
      width: '100%',
      marginBottom: 20,
      paddingVertical: 15,
      paddingHorizontal: 20,
      borderWidth: 1,
      borderColor: '#ccc',
      borderRadius: 5,
      fontSize: 16,
    },
    loginButton: {
      backgroundColor: '#4267B2',
      width: '100%',
      paddingVertical: 15,
      borderRadius: 5,
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: 20,
    },
    buttonText: {
      color: '#fff',
      fontSize: 16,
      fontWeight: 'bold',
    },
    registerLink: {
      alignItems: 'center',
    },
    registerText: {
      color: '#4267B2',
      fontSize: 14,
    },
  });

export default LoginScreen;
