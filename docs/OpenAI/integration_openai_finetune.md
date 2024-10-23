
# Intégrer un Modèle OpenAI Finetuné dans une Application

## 1. Créer et Finetuner le Modèle via OpenAI API

Si vous ne l'avez pas déjà fait, vous devez d'abord finetuner votre modèle GPT-3.5 ou GPT-4 avec l'API d'OpenAI.

### Étapes :
1. **Préparer les données pour le fine-tuning** :
   - Assurez-vous que vos données sont au format JSONL.
   - Chaque exemple doit suivre le format : 
     ```json
     {"prompt": "<votre_prompt>", "completion": "<votre_completion>"}
     ```

2. **Uploader les données** :
   - Utilisez l’API d’OpenAI pour uploader les fichiers avec `openai.File.create`.

3. **Démarrer le fine-tuning** :
   - Utilisez la commande `openai.FineTune.create` avec l'ID du fichier pour créer un modèle finetuné.

4. **Récupérer l'ID du modèle** :
   - Une fois le fine-tuning terminé, notez l'ID du modèle finetuné.

## 2. Installer la Bibliothèque OpenAI

Assurez-vous que votre application utilise la bibliothèque Python ou JavaScript pour interagir avec l'API OpenAI.

### Installation pour JavaScript/Node.js :
```bash
npm install openai
```

### Installation pour Python :
```bash
pip install openai
```

## 3. Utiliser le Modèle Finetuné dans l'Application

### Exemple en JavaScript (React ou Node.js) :

1. **Configurer l'API dans l'application** :
   ```javascript
   const { Configuration, OpenAIApi } = require("openai");

   const configuration = new Configuration({
     apiKey: process.env.OPENAI_API_KEY,  // Assurez-vous d'utiliser la clé API
   });

   const openai = new OpenAIApi(configuration);
   ```

2. **Faire une requête à votre modèle finetuné** :
   ```javascript
   async function getCompletion(prompt) {
     const response = await openai.createCompletion({
       model: "ft-your-model-id", // Remplacez par l'ID de votre modèle finetuné
       prompt: prompt,
       max_tokens: 100, // Nombre maximum de tokens
     });
     return response.data.choices[0].text;
   }

   // Exemple d'appel
   getCompletion("Voici votre prompt").then(console.log);
   ```

### Exemple en Python :

1. **Configurer l'API dans votre application** :
   ```python
   import openai

   openai.api_key = 'votre_clé_API'
   ```

2. **Appeler le modèle finetuné** :
   ```python
   response = openai.Completion.create(
     model="ft-your-model-id",  # Remplacez par l'ID de votre modèle finetuné
     prompt="Voici votre prompt",
     max_tokens=100
   )

   print(response.choices[0].text)
   ```

## 4. Gestion des Erreurs et Optimisation
- **Gestion des erreurs** : Pensez à capturer les erreurs API comme les requêtes invalides ou les dépassements de limites de tokens.
- **Limiter les appels API** : Essayez d’optimiser les appels en utilisant des caches locaux si possible.

## 5. Intégration dans l'Interface

Dans une application React, vous pouvez appeler cette fonction dans une composante et afficher la réponse dans l'interface utilisateur. Par exemple, vous pouvez déclencher l'appel OpenAI lorsque l'utilisateur soumet un formulaire.

### Exemple d'intégration dans une composante React :
```jsx
import React, { useState } from 'react';

function CompletionComponent() {
  const [prompt, setPrompt] = useState('');
  const [completion, setCompletion] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/getCompletion', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();
    setCompletion(data.completion);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt"
        />
        <button type="submit">Get Completion</button>
      </form>
      <p>Completion: {completion}</p>
    </div>
  );
}

export default CompletionComponent;
```

## 6. API Backend

Si votre application est en React et que vous gérez les appels API depuis un serveur backend (comme Express.js), vous pouvez créer un endpoint backend pour gérer la requête API OpenAI et renvoyer les résultats au frontend.
