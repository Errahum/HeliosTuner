# Comment partir le projet en locale?

## Terminal 1
Exécuter le backend fineurai/backend/app.py

## Terminal 2

``
cd frontend
``

``
stripe listen --forward-to http://localhost:5000/api/webhook
``

## Terminal 3
### Soit exécuter le serveur ou en créer un:
#### Création:

``
npm install
``

``
cd frontend
``

``
npm start
``

#### Utilisation du serveur:
``
cd frontend
``

``
npm install
``

``
npm run build
``

``
node server.js
``

# Comment partir le projet en ligne?

Mettre les variables d'environnements dans le hosting de backend.

Frontend prend seulement l'url du backend pour fonctionner.

## Backend:

### env var:
````
PORT:8000
FLASK_ENV:production
PYTHONPATH:./backend:./backend/src
e.c.t.
````

### Build Command:
``
$pip install -r requirements.txt
``
### Start Command:
``
$gunicorn -b 0.0.0.0:$PORT backend.app:app
``
## Frontend:
Foward de Cloudflare jusqu'au Hosting pour l'URL du Frontend

### env var:
````
PORT:10000
REACT_APP_BACKEND_URL:BACKEND_URL_PUBLIC
````

### Build Command:
``
$cd frontend && npm install && npm run build
``
### Start Command:
``
$cd frontend && node server.js
``