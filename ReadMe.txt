---------------ReadMe Projet de fin de session-------------------------------------------

Notre projet est composé de 3 parties :
Une API qui sert à gérer la base de donnée
Un serveur qui reçoit les requetes et les traite
Une app mobile qui offre les même fonctionnalités que l'interface web

Nous allons voir comment configurer le projet pour le lancer sur votre machine

-----------------Mise en place de l'API----------------------------------------------------

Placer vous dans un dossier sur votre machine et assurer vous que python est installé
Version de python utilisé pour le développement : 3.11

1)Creer un environnement virtuel python avec : python -mvenv API

2) cd API ; cd Scripts ; activate ; cd ..

3) pip install flask 
   pip install firebase_admin
(Un fichier de requirement est aussi disponible)

4) Ajouter les fichiers dans le zip de API (main.py, ServiceBdd.py et config.json)

5) Pour lancer le serveur rentrer la commande suivante 
flask --app main.py run --port=8000

Par défaut notre serveur est fait pour envoyé les requettes à l'api a l'url http://127.0.0.1:8000
Si votre serveur se lance sur une autre adresse ip, il faudra la changer dans le fichier de configuration du serveur

-----------------Mise en place du serveur---------------------------------------------------

Placer vous dans un dossier sur votre machine et assurer vous que python est installé
Version de python utilisé pour le développement : 3.11

1)Creer un environnement virtuel python avec : python -mvenv serveur

2) cd API ; cd Scripts ; activate ; cd ..

3) pip install flask 
   pip install flask_cors
   pip install facebook-sdk
(Un fichier de requirement est aussi disponible)

4) Ajouter les fichiers dans le zip de serveur (main.py, validation.py,config.py, dossier template et dossier static)

5)Si le serveur de l'api ne s'est pas lancé à l'url http://127.0.0.1:8000, il vous faut alors modifier le paramètre "api_url" du fichier
de configuration pour indiquer celui de l'api

6) Pour lancer le serveur rentrer la commande suivante 
flask --app main.py run --host=0.0.0.0

Normalement le serveur se lance sur 127.0.0.1:5000 sur votre machine et une autre adresse qui nous servira pour l'app mobile.
Si vous avez une autre adresse il faut changer le parametre "api_serveur" du fichier de confiiguration pour mettre votre adresse.

A cette étape la vous pouver normalement utiliser le client web et toute les fonctionnalité du serveur.

-----------------Mise en place de l'app mobile--------------------------------------------

Version de Node.js utilisé : v20.11.1

1) Se placer dans un dossier verifier que node.js est installé et installer les packages suivants :

npm install react-native
npm install expo-app
npm install create-expo-app

2) Créer un nouveau projet 

npx create-expo-app AppMobile
cd AppMobile

3)Installer les packages suivants 
npx expo install react-native-web react-dom @expo/metro-runtime
npm i --save react-native-events-calendar

4) Ajouter les fichiers du zip (App.js, LoginScreen.js, HomeScreen.js, config.js)

5) Lorsque vous avez lancé le serveur, un deuxieme url vous est donnée, c'est cet url qu'il faut mettre dans le fichier config.js pour que 
l'app mobile puisse communiquer en réseau local avec le serveur 

5) npx expo start



