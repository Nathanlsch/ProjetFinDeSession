import React, { useState } from 'react';
import { View } from 'react-native';
import LoginScreen from './LoginScreen';
import HomeScreen from './HomeScreen';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [userId, setUserId] = useState('');
  const [username, setUsername] = useState('');
  const [groupList, setGroupList] = useState([]);
  

  const handleLogin = (userId, username, groupList) => {
    setUserId(userId);
    setUsername(username);
    setGroupList(groupList);
    setLoggedIn(true);
  };

  return (
    <View style={{ flex: 1 }}>
      {loggedIn ? (
        <HomeScreen 
          userId={userId}
          username={username} 
          groupList={groupList} 
          setGroupList={setGroupList} 
          setUserId={setUserId}
          setLoggedIn={setLoggedIn}
          setUsername={setUsername}
          />
      ) : (
        <LoginScreen onLogin={handleLogin} />
      )}
    </View>
  );
};

export default App;
