from flask import Flask, render_template, request, redirect
import facebook
import sys
import os

# Ajoutez le chemin du dossier ServicePython au chemin de recherche Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'ServicePython'))

import ServiceBdd

# Facebook app credentials
app_id = '1721756045020268'
app_secret = 'e0239934728a294f232fd1ed7bb16445'
redirect_uri = 'http://localhost:5000/callback'  # Update with your own redirect URI

# Initialisation de l'application Flask
app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
def index():
    ServiceBdd.ajoutUtilisateurGroupe("groupe6", "id_facebook")
    return render_template('test.html')


@app.route('/login-facebook')
def login():
    auth_url = facebook.GraphAPI().get_auth_url(app_id, redirect_uri)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    access_token = facebook.GraphAPI().get_access_token_from_code(code, redirect_uri, app_id, app_secret)
    graph = facebook.GraphAPI(access_token['access_token'])
    me = graph.get_object('me')
    id = me['id']
    name = me['name']
    return f"Logged in as {name} with ID {id}"

if __name__ == '__main__':
    app.run(debug=True)
