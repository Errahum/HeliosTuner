# How to Create Your OpenAI API Key

OpenAI offers a powerful API for artificial intelligence. To use it, you first need to create an API key. Follow these simple steps to get your OpenAI API key:

1. **Create an OpenAI Account:**
   - Go to the OpenAI website (https://www.openai.com/).
   - Click on "Sign Up" to create an account if you don't already have one.

2. **Access Your Account:**
   - Once logged in, navigate to your OpenAI account.

3. **Go to the API Section:**
   - In your OpenAI account, look for the API section or go directly to the following URL: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).

4. **Create a New API Key:**
   - Click on the "Create API Key" button.
   - Give your API key a name for easy recognition.

5. **Copy Your API Key:**
   - Once the API key is created, copy it. It will look something like `sk-XXXXXXXXXXXXXXXXXXXXXXXX`.

6. **Keep Your Key Secure:**
   - It's important to keep your API key secure and not share it publicly.

7. **Use Your API Key:**
   - You can now use your API key to access OpenAI services from your application.

8. **Manage Your API Key:**
   - In your OpenAI account, you can manage your API keys, create new ones, or revoke them if necessary.

That's it! You have now created your OpenAI API key and are ready to start using the API for your artificial intelligence projects.

# Setting Up an Environment Variable for the OpenAI API on Windows

To use the OpenAI API in your Windows environment, you need to set up an environment variable to store your API key. Here's how:

1. **Find Advanced System Settings:**
   - Right-click on "This PC" or "Computer" in File Explorer or on the desktop.
   - Select "Properties" from the context menu.
   - Click on "Advanced system settings" on the left side of the window.

2. **Open Environment Variables:**
   - In the "System Properties" window, click the "Environment Variables..." button near the bottom of the window.

3. **Add a New Environment Variable:**
   - In the "System Variables" or "User Variables" section, click "New...".
   - For "Variable name", enter: `OPENAI_API_KEY`.
   - For "Variable value", enter your OpenAI API key.

4. **Confirm and Apply Changes:**
   - Click "OK" to close the "New System Variable" or "New User Variable" window.
   - Click "OK" to close the "Environment Variables" window.
   - Click "OK" to close the "System Properties" window.

5. **Restart Your Computer:**
   - To apply the changes, you may need to restart your computer.

Your `OPENAI_API_KEY` environment variable is now set up for use in your Windows environment.

# Procedure
Here are the steps for the fine-tuning process.

# Step 1: Creating a Fine-Tuning Model

1. **Initializing the User Interface**
   - Open the user interface.
   - Navigate to the "Create Fine-Tuning Job" tab.

   **Required Class and Function:**
   - `OpenAIInterfaceFT.__init__`

2. **Selecting the Training Data File**
   - Click the "Browse" button to open a file dialog.
   - Select the JSONL file containing the training data.

   **Required Class and Function:**
   - `OpenAiInterfaceUtils.browse_training_data`

3. **Configuring the Model**
   - Enter the model name to use in the "Model" field.
   - By default, the model is "gpt-3.5-turbo".

4. **Creating the Fine-Tuning Job**
   - Click the "Send" button to start the fine-tuning job creation process.
   - The training data file will be uploaded, and a fine-tuning job will be created via the OpenAI API.

   **Required Classes and Functions:**
   - `OpenAiInterfaceUtils.create_fine_tuning_job`
   - `FineTuningHandle.upload_training_file`
   - `FineTuningHandle.create_fine_tuning_job`

# Step 2: Managing Fine-Tuning Jobs https://platform.openai.com/finetune

1. **Viewing Fine-Tuning Jobs**
   - Navigate to the "List Fine-Tuning Jobs" tab.
   - Click the "Get All Job IDs" button to retrieve and display all existing fine-tuning job IDs.

   **Required Classes and Functions:**
   - `OpenAiInterfaceUtils.display_job_ids`
   - `FineTuningHandle.get_all_job_ids`

2. **Selecting a Job**
   - From the list of displayed jobs, click on a job to select it.
   - Use the "Select/Copy Job IDs" button to copy the ID of the selected job to the clipboard.
   - Use the "Select/Copy Names" button to copy the name of the selected job to the clipboard.

   **Required Classes and Functions:**
   - `OpenAiInterfaceUtils.select_job_ids`
   - `OpenAiInterfaceUtils.select_names`
   - `OpenAiInterfaceUtils.copy_to_clipboard`

3. **Canceling a Job**
   - Select the job you want to cancel.
   - Click "Select/Copy Job IDs"
   - Click the "Cancel Job" button to cancel the selected fine-tuning job.
   - Click "Get All Job IDs to verify if the job is no longer present."

   **Required Classes and Functions:**
   - `OpenAiInterfaceUtils.cancel_job`
   - `FineTuningHandle.cancel_fine_tuning_job`

# Step 3: Using an Existing Fine-Tuning Job

1. **Loading Existing Fine-Tuning Jobs**
   - When you open the application, existing fine-tuning jobs can be automatically loaded from the OpenAI API.

   **Required Classes and Functions:**
   - `OpenAiInterfaceUtils.display_job_ids`
   - `FineTuningHandle.get_all_job_ids`

2. **Selecting an Existing Job**
   - From the list of displayed jobs, select the job you want to use for further operations.
   - Use the appropriate buttons to copy the ID or name of the job for future use.

   **Required Classes and Functions:**
   - `OpenAiInterfaceUtils.select_job_ids`
   - `OpenAiInterfaceUtils.select_names`
   - `OpenAiInterfaceUtils.copy_to_clipboard`

# Additional Notes
- Ensure all required fields are correctly filled before submitting a fine-tuning job.
- In case of an error, an error message will be displayed in the user interface, indicating the problem and possible corrective actions.
- The main functions for managing fine-tuning jobs are encapsulated in the `FineTuningHandle` class, which communicates with the OpenAI API to perform necessary operations.

# Hyperparameters:

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
