# Création d'un Frontend React avec un Backend Flask

# Testing step:
1: Start backend app.py
2: start frontend:
  - cd frontend
  - npm start
3: Start Stripe webhook
  - stripe listen --forward-to http://localhost:5000/api/webhook

## Étapes pour créer un frontend React

1. **Assurez-vous d'avoir Node.js installé** :
   - Téléchargez Node.js depuis [nodejs.org](https://nodejs.org/) si ce n'est pas encore fait.
   - Vérifiez l'installation avec :
     ```bash
     node -v
     npm -v
     ```

2. **Créez l'application React** :
   - Ouvrez un terminal à la racine de votre projet (où se trouve le dossier `"backend"`).
   - Exécutez la commande suivante pour créer un projet React dans le dossier `"frontend"` :
     ```bash
     npx create-react-app frontend
     ```

3. **Démarrer l'application React** :
   - Accédez au dossier `"frontend"` :
     ```bash
     cd frontend
     ```
   - Démarrez le serveur de développement React :
     ```bash
     npm start
     ```
   - L'application React sera disponible à `http://localhost:3000`.

## Étapes pour configurer la communication entre React et Flask (app.py)

1. **Configurer le proxy dans React** :
   - Ouvrez le fichier `frontend/package.json`.
   - Ajoutez la ligne suivante pour définir le proxy :
     ```json
     "proxy": "http://localhost:5000",
     ```

2. **Assurer la communication entre le frontend et le backend** :
   - Ouvrez le fichier `frontend/src/App.js` et remplacez le contenu par :
     ```javascript
     import React, { useState } from 'react';

     function App() {
       const [userMessage, setUserMessage] = useState('');
       const [chatResponse, setChatResponse] = useState('');

       const handleChatCompletion = async () => {
         const response = await fetch('/api/chat-completion', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({
             user_message: userMessage,
             max_tokens: 100,
             model: 'gpt-3.5-turbo',
             temperature: 1.0,
             stop: null,
             window_size: 10
           })
         });

         const data = await response.json();
         if (response.ok) {
           setChatResponse(data.response.content); // Afficher la réponse de l'IA
         } else {
           console.error('Erreur lors de la génération du chat:', data.message);
         }
       };

       return (
         <div>
           <h1>Chat App</h1>
           <input
             type="text"
             value={userMessage}
             onChange={(e) => setUserMessage(e.target.value)}
             placeholder="Tapez votre message"
           />
           <button onClick={handleChatCompletion}>Envoyer</button>
           {chatResponse && <div>Réponse de l'IA: {chatResponse}</div>}
         </div>
       );
     }

     export default App;
     ```

## Étapes pour faire fonctionner le backend et le frontend ensemble

1. **Démarrer le backend Flask** :
   - Allez dans votre dossier `"backend"` :
     ```bash
     cd backend
     ```
   - Démarrez le serveur Flask :
     ```bash
     python app.py
     ```
   - Le backend sera disponible à `http://localhost:5000`.

2. **Démarrer le frontend React** :
   - Ouvrez un autre terminal et accédez au dossier `"frontend"` :
     ```bash
     cd frontend
     ```
   - Démarrez l'application React :
     ```bash
     npm start
     ```
   - L'application React sera accessible à `http://localhost:3000`.

## Structure finale du projet

Votre projet devrait ressembler à ceci :

/my-project /backend /app.py # Backend Flask avec les endpoints API /chat_completion_handle.py # Votre module existant /requirements.txt # Les dépendances Python /frontend /public /src /package.json # Projet React


## Conclusion

- Vous avez créé un projet React dans le dossier `"frontend"`.
- Vous avez configuré un proxy pour que React puisse envoyer des requêtes à Flask sur `localhost:5000`.
- Vous avez un exemple de composant React qui envoie des requêtes au backend Flask pour obtenir une réponse de l'API.


# Nettoyez le cache de npm : Parfois, des problèmes peuvent être résolus en nettoyant le cache de npm :

```bash
npm cache clean --force
```