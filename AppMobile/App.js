import React, { useState } from 'react';
import { View } from 'react-native';
import LoginScreen from './LoginScreen';
import HomeScreen from './HomeScreen';

const App = () => {

  //Information sur l'utilisateur ou l'état de connexion 
  const [loggedIn, setLoggedIn] = useState(false);
  const [userId, setUserId] = useState('');
  const [username, setUsername] = useState('');
  const [groupList, setGroupList] = useState([]);
  
  //Définie localement les informations de l'utilisateur 
  const handleLogin = (userId, username, groupList) => {
    setUserId(userId);
    setUsername(username);
    setGroupList(groupList);
    setLoggedIn(true);
  };

  return (
    <View style={{ flex: 1 }}>
      
      {loggedIn ? ( //Si l'utilisateur est connecté affiche la page d'accueil 
        <HomeScreen 
          userId={userId}
          username={username} 
          groupList={groupList} 
          setGroupList={setGroupList} 
          setUserId={setUserId}
          setLoggedIn={setLoggedIn}
          setUsername={setUsername}
          />
      ) : ( //Sinon afficher la page de connexion 
        <LoginScreen onLogin={handleLogin} />
      )}
    </View>
  );
};

export default App;
