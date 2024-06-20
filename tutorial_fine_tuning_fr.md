# Comment créer votre clé API OpenAI

OpenAI offre une API puissante pour l'intelligence artificielle. Pour l'utiliser, vous devez d'abord créer une clé API. Suivez ces étapes simples pour obtenir votre clé API OpenAI :

1. **Créez un compte OpenAI :**
   - Allez sur le site web d'OpenAI (https://www.openai.com/).
   - Cliquez sur "Sign Up" pour créer un compte si vous n'en avez pas déjà un.

2. **Accédez à votre compte :**
   - Une fois connecté, accédez à votre compte OpenAI.

3. **Accédez à la section API :**
   - Dans votre compte OpenAI, recherchez la section API ou accédez directement à l'URL suivante : [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).

4. **Créez une nouvelle clé API :**
   - Cliquez sur le bouton "Create API Key".
   - Donnez un nom à votre clé API pour la reconnaître facilement.

5. **Copiez votre clé API :**
   - Une fois la clé API créée, copiez-la. Elle ressemblera à quelque chose comme `sk-XXXXXXXXXXXXXXXXXXXXXXXX`.

6. **Conservez votre clé en sécurité :**
   - Il est important de garder votre clé API en sécurité et de ne pas la partager publiquement.

7. **Utilisez votre clé API :**
   - Vous pouvez maintenant utiliser votre clé API pour accéder aux services OpenAI depuis votre application.

8. **Gérez votre clé API :**
   - Dans votre compte OpenAI, vous pouvez gérer vos clés API, en créer de nouvelles ou en révoquer si nécessaire.

C'est tout ! Vous avez maintenant créé votre clé API OpenAI et vous êtes prêt à commencer à utiliser l'API pour vos projets d'intelligence artificielle.


# Créer une variable d'environnement pour l'API OpenAI sur Windows

Pour utiliser l'API OpenAI dans votre environnement Windows, vous devez définir une variable d'environnement pour stocker votre clé API. Voici comment faire :

1. **Trouver les paramètres système avancés :**
   - Cliquez avec le bouton droit sur "Ce PC" ou "Ordinateur" dans l'explorateur de fichiers ou sur le bureau.
   - Sélectionnez "Propriétés" dans le menu contextuel.
   - Cliquez sur "Paramètres système avancés" sur le côté gauche de la fenêtre.

2. **Ouvrir les variables d'environnement :**
   - Dans la fenêtre "Propriétés système", cliquez sur le bouton "Variables d'environnement..." près du bas de la fenêtre.

3. **Ajouter une nouvelle variable d'environnement :**
   - Dans la section "Variables système" ou "Variables utilisateur", cliquez sur "Nouvelle...".
   - Pour "Nom de la variable", entrez : `OPENAI_API_KEY`.
   - Pour "Valeur de la variable", entrez votre clé API OpenAI.

4. **Valider et appliquer les modifications :**
   - Cliquez sur "OK" pour fermer la fenêtre "Nouvelle variable système" ou "Nouvelle variable utilisateur".
   - Cliquez sur "OK" pour fermer la fenêtre "Variables d'environnement".
   - Cliquez sur "OK" pour fermer la fenêtre "Propriétés système".

5. **Redémarrer votre ordinateur :**
   - Pour que les modifications prennent effet, vous devrez peut-être redémarrer votre ordinateur.

Votre variable d'environnement `OPENAI_API_KEY` est maintenant configurée pour être utilisée dans votre environnement Windows.

# Démarche
Voici les étapes pour la procédure du fonctionnement du fine-tuning.

# Étape 1 : Création d'un modèle de fine-tuning

1. **Initialisation de l'interface utilisateur**
   - Ouvrez l'interface utilisateur.
   - Naviguez vers l'onglet "Create Fine-Tuning Job".

   **Classe et fonction requises :**
   - `OpenAIInterfaceFT.__init__`

2. **Sélection du fichier de données d'entraînement**
   - Cliquez sur le bouton "Browse" pour ouvrir une fenêtre de dialogue.
   - Sélectionnez le fichier JSONL contenant les données d'entraînement.

   **Classe et fonction requises :**
   - `OpenAiInterfaceUtils.browse_training_data`

3. **Configuration du modèle**
   - Saisissez le nom du modèle à utiliser dans le champ "Model".
   - Par défaut, le modèle est "gpt-3.5-turbo".

4. **Création du job de fine-tuning**
   - Cliquez sur le bouton "Envoyer" pour démarrer le processus de création du job de fine-tuning.
   - Le fichier de données d'entraînement sera téléchargé et un job de fine-tuning sera créé via l'API OpenAI.

   **Classe et fonction requises :**
   - `OpenAiInterfaceUtils.create_fine_tuning_job`
   - `FineTuningHandle.upload_training_file`
   - `FineTuningHandle.create_fine_tuning_job`

# Étape 2 : Gestion des jobs de fine-tuning https://platform.openai.com/finetune

1. **Visualisation des jobs de fine-tuning**
   - Naviguez vers l'onglet "List Fine-Tuning Jobs".
   - Cliquez sur le bouton "Get All Job IDs" pour récupérer et afficher tous les IDs des jobs de fine-tuning existants.

   **Classe et fonction requises :**
   - `OpenAiInterfaceUtils.display_job_ids`
   - `FineTuningHandle.get_all_job_ids`

2. **Sélection d'un job**
   - Dans la liste des jobs affichés, sélectionnez un job en cliquant dessus.
   - Utilisez le bouton "Select/Copy Job IDs" pour copier l'ID du job sélectionné dans le presse-papiers.
   - Utilisez le bouton "Select/Copy Names" pour copier le nom du job sélectionné dans le presse-papiers.

   **Classe et fonction requises :**
   - `OpenAiInterfaceUtils.select_job_ids`
   - `OpenAiInterfaceUtils.select_names`
   - `OpenAiInterfaceUtils.copy_to_clipboard`

3. **Annulation d'un job**
   - Sélectionnez le job que vous souhaitez annuler.
   - Cliquez sur "Select/Copy Job IDs"
   - Cliquez sur le bouton "Cancel Job" pour annuler le job de fine-tuning sélectionné.
   - Cliquez sur "Get All Job IDs pour vérifier si le job n'est plu présent."

   **Classe et fonction requises :**
   - `OpenAiInterfaceUtils.cancel_job`
   - `FineTuningHandle.cancel_fine_tuning_job`

# Étape 3 : Utilisation d'un job de fine-tuning existant

1. **Chargement des jobs de fine-tuning existants**
   - Lorsque vous ouvrez l'application, les jobs de fine-tuning existants peuvent être chargés automatiquement à partir de l'API OpenAI.

   **Classe et fonction requises :**
   - `OpenAiInterfaceUtils.display_job_ids`
   - `FineTuningHandle.get_all_job_ids`

2. **Sélection d'un job existant**
   - Dans la liste des jobs affichés, sélectionnez le job que vous souhaitez utiliser pour d'autres opérations.
   - Utilisez les boutons appropriés pour copier l'ID ou le nom du job pour des utilisations ultérieures.

   **Classe et fonction requises :**
   - `OpenAiInterfaceUtils.select_job_ids`
   - `OpenAiInterfaceUtils.select_names`
   - `OpenAiInterfaceUtils.copy_to_clipboard`

# Remarques supplémentaires
- Assurez-vous que tous les champs nécessaires sont correctement remplis avant de soumettre un job de fine-tuning.
- En cas d'erreur, un message d'erreur s'affichera dans l'interface utilisateur, indiquant le problème et les actions correctives possibles.
- Les fonctions principales de gestion des jobs de fine-tuning sont encapsulées dans la classe `FineTuningHandle`, qui communique avec l'API OpenAI pour effectuer les opérations nécessaires.

# Hyperparameter:

1. **n_epochs :**
	- string or integer
	- The number of epochs to train the model for. 
	- An epoch refers to one full cycle through the training dataset.
	- "auto" decides the optimal number of epochs based on the size of the dataset.
	- If setting the number manually, we support any number between 1 and 50 epochs.

2. **batch_size :**
	- string or integer
	- Optional
	- Defaults to "auto"
	- Number of examples in each batch. A larger batch size means that model parameters are updated less frequently, but with lower variance.

3. **learning_rate_multiplier :**
	- string or number
	- Optional
	- Defaults to "auto"
	- Scaling factor for the learning rate. A smaller learning rate may be useful to avoid overfitting.


# Options:

1. **seed :**
	- integer or null
	- Optional
	- If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result.
	- Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.
	
2. **suffix :**
	- string or null
	- Optional
	- Defaults to null
	- A string of up to 18 characters that will be added to your fine-tuned model name.
	- For example, a suffix of "custom-model-name" would produce a model name like ft:gpt-3.5-turbo:openai:custom-model-name:7p4lURel.
	- Suffix must only contain letters, numbers, and dashes
	
	
3. **model :**
	- string
	- Required
	- The name of the model to fine-tune. You can select one of the supported models.

4. **training_file :**
	- string
	- Required
	- The ID of an uploaded file that contains training data.
	- See upload file for how to upload a file.
	- Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose fine-tune.
	- See the fine-tuning guide for more details.
	
	
	