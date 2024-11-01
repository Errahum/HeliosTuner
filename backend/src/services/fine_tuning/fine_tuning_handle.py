import logging
import os
import time

import openai
from openai import OpenAI

from .fine_tuning_exceptions import FineTuningRequestError, InvalidFineTuningModelError, ServiceNotFoundError
from .fine_tuning_manager import FineTuningManager
from src.utils.custom_logging import logging_custom
from datetime import datetime
from supabase_client import get_supabase_client
supabase = get_supabase_client()  # Get the supabase client

logging_custom()

class FineTuningHandle:
    def __init__(self, config, training_data_path, model, name, seed, n_epochs, learning_rate, batch_size, job_ids_file='job_ids.txt'):
        self.fine_tuning_manager = FineTuningManager(config)
        self.client = OpenAI(api_key=config.get_api_key())
        self.training_file_id = None
        self.training_data_path = training_data_path
        self.model = model
        self.name = name
        self.seed = seed
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.local_job_ids = self.load_job_ids(job_ids_file)
        self.job_ids_file = job_ids_file
        self.fine_tuning_response = None  # Pour stocker la réponse du job de fine-tuning
        self.training_file_ids = {}
        self.fine_tuning_responses = {}  # Pour stocker les réponses des jobs de fine-tuning par utilisateur




    def set_parameter(self, training_data_path, model, name, seed, n_epochs, learning_rate, batch_size):
        self.training_data_path = training_data_path
        self.model = model
        self.name = name
        self.seed = seed
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size

    def save_job_id_locally(self, job_id):
        self.local_job_ids.append(job_id)
        # Sauvegarde dans un fichier
        with open(self.job_ids_file, 'a') as f:
            f.write(job_id + '\n')

    def load_job_ids(self, job_ids_file):
        if os.path.exists(job_ids_file):
            with open(job_ids_file, 'r') as f:
                return [line.strip() for line in f.readlines()]
        return []
    
    
    def get_all_job_ids(self):
        try:
            job_ids = []
            after_cursor = None
            while True:
                response = self.client.fine_tuning.jobs.list(after=after_cursor)
                for job in response.data:
                    if job.status not in ['cancelled', 'failed']:
                        job_info = f"name: {job.fine_tuned_model} - Model: {job.model} - Job ID: {job.id}"
                        job_ids.append(job_info)
                        self.save_job_id_locally(job.id)

                # Vérifier s'il y a plus de résultats à récupérer
                if not response.data:
                    break
                after_cursor = response.data[-1].id  # Utiliser l'ID du dernier job comme curseur

            return job_ids
        except openai.OpenAIError as e:
            logging.error(f"get_all_job_ids OpenAI error: {e}")
            return None

    def upload_training_file(self, user_email, training_data_path):
        try:
            with open(training_data_path, 'rb') as f:
                response = self.client.files.create(
                    file=f,
                    purpose="fine-tune",
                )
                self.training_file_ids[user_email] = response.id
            os.remove(training_data_path)  # Delete the temporary file after upload
        except openai.OpenAIError as e:
            logging.error(f"upload_training_file OpenAI error: {e}")
            if os.path.exists(training_data_path):
                os.remove(training_data_path)

    def create_fine_tuning_job(self, user_email, training_data_path, model, name, seed, n_epochs, learning_rate, batch_size):
        if user_email not in self.training_file_ids:
            self.upload_training_file(user_email, training_data_path)
            if not self.training_file_ids[user_email]:
                logging.error("create_fine_tuning_job Failed to upload training file.")
                return

        try:
            # Lancer le job de fine-tuning et stocker la réponse
            self.fine_tuning_responses[user_email] = self.client.fine_tuning.jobs.create(
                model=model,
                training_file=self.training_file_ids[user_email],
                suffix=name,
                seed=seed,
                hyperparameters={
                    "n_epochs": n_epochs,
                    "learning_rate_multiplier": learning_rate,
                    "batch_size": batch_size
                }
            )
            logging.info("\nFine-Tuning Response:")
            logging.info(self.fine_tuning_responses[user_email])

            # Enregistrer les informations du job dans Supabase
            job_id = self.fine_tuning_responses[user_email].id
            if not job_id:
                logging.error("Job ID is not defined.")
                return

            hyperparameters = {
                "n_epochs": n_epochs,
                "learning_rate_multiplier": learning_rate,
                "batch_size": batch_size,
                "seed": seed
            }
            supabase.table('fine_tuning_jobs').insert({
                'user_email': user_email,
                'job_id': job_id,
                'hyperparameters': hyperparameters
            }).execute()

            # Estimation du coût
            base_cost_per_million_tokens = 0.024  # Exemple de coût pour gpt-3.5-turbo-0125
            estimated_cost = self.estimate_cost(user_email, base_cost_per_million_tokens)
            logging.info(f"Estimated cost for fine-tuning job: ${estimated_cost:.2f} USD")

        except openai.OpenAIError as e:
            logging.error(f"create_fine_tuning_job OpenAI error: {e}")

    def cancel_fine_tuning_job(self, job_ids):
        try:
            logging.info("cancel_fine_tuning_job")
            for job_id in job_ids:
                if job_id.startswith("ftjob-"):
                    fine_tuning_response = self.fine_tuning_manager.cancel_fine_tuning(job_id)
                    logging.info("\nCancel Fine-Tuning Job Response:")
                    logging.info(fine_tuning_response)
                else:
                    logging.info("Invalid job ID format: {job_id}")
        except FineTuningRequestError as e:
            logging.error(f"Fine-tuning request error: {e.message}")
        except InvalidFineTuningModelError as e:
            logging.error(f"Invalid fine-tuning model error: {str(e)}")
        except ServiceNotFoundError as e:
            logging.error(f"Service not found error: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")

    def is_job_complete(self, user_email):
        if user_email not in self.fine_tuning_responses:
            logging.error("Fine-tuning response is not initialized for this user.")
            return False

        job_id = self.fine_tuning_responses[user_email].id

        if not job_id:
            logging.error("Job ID is not defined.")
            return False

        try:
            response = self.client.fine_tuning.jobs.retrieve(job_id)
            job_status = response.status
            return job_status == 'succeeded'  # Vérifie si le job est terminé avec succès
        except openai.OpenAIError as e:
            logging.error(f"is_job_complete OpenAI error: {e}")
        return False
    
    def get_total_tokens_used(self, user_email):
        if user_email not in self.fine_tuning_responses:
            logging.error("Fine-tuning response is not initialized for this user.")
            return 0

        job_id = self.fine_tuning_responses[user_email].id

        if not job_id:
            logging.error("Job ID is not defined.")
            return 0

        try:
            response = self.client.fine_tuning.jobs.retrieve(job_id)
            logging.info(response)  # Log the response to see its structure

            # Check if the job status is 'succeeded' before retrieving tokens
            if response.status != 'succeeded':
                logging.error(f"Job {job_id} is not completed. Current status: {response.status}")
                return 0

            # Directly access the 'trained_tokens' attribute
            total_tokens = response.trained_tokens if hasattr(response, 'trained_tokens') else 0
            if total_tokens == 0:
                logging.warning(f"trained_tokens not found or zero for job {job_id}. Retrying...")
                time.sleep(2)  # Introduce a slight delay before retrying
                response = self.client.fine_tuning.jobs.retrieve(job_id)
                total_tokens = response.trained_tokens if hasattr(response, 'trained_tokens') else 0

            if total_tokens == 0:
                logging.error(f"Failed to retrieve trained_tokens for job {job_id} after retry.")

            return total_tokens
        except openai.OpenAIError as e:
            logging.error(f"get_total_tokens_used OpenAI error: {e}")
            return 0
        except Exception as e:
            logging.error(f"Unexpected error in get_total_tokens_used: {e}")
            return 0
        
    def estimate_cost(self, user_email, base_cost_per_million_tokens):
        total_tokens = self.get_total_tokens_used(user_email)
        if total_tokens == 0:
            logging.info("Total tokens used is zero, cannot estimate cost.")
            return 0.0

        # Estimation du coût
        cost = (base_cost_per_million_tokens / 1_000_000) * total_tokens * self.n_epochs
        return cost
    
    def get_job_status(self, job_id):
        try:
            response = self.client.fine_tuning.jobs.retrieve(job_id)
            return response.status
        except openai.OpenAIError as e:
            logging.error(f"get_job_status OpenAI error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in get_job_status: {e}")
            return None