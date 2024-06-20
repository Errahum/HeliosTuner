import os
from tkinter import messagebox

import openai
from openai import OpenAI

from .fine_tuning_exceptions import FineTuningRequestError, InvalidFineTuningModelError, ServiceNotFoundError
from .fine_tuning_manager import FineTuningManager


class FineTuningHandle:
    def __init__(self, config, training_data_path, model, name, seed, n_epochs, learning_rate, batch_size,
                 job_ids_file='job_ids.txt'):
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
            print(f"OpenAI error: {e}")
            return None

    def upload_training_file(self):
        try:
            with open(self.training_data_path, 'rb') as f:
                response = self.client.files.create(
                    file=f,
                    purpose="fine-tune",
                )
                self.training_file_id = response.id
        except openai.OpenAIError as e:
            print(f"OpenAI error: {e}")

    def create_fine_tuning_job(self):
        if not self.training_file_id:
            self.upload_training_file()
            if not self.training_file_id:
                print("Failed to upload training file.")
                return

        try:
            response = self.client.fine_tuning.jobs.create(
                model=self.model,
                training_file=self.training_file_id,
                suffix=self.name,
                seed=self.seed,
                hyperparameters={
                    "n_epochs": self.n_epochs,
                    "learning_rate_multiplier": self.learning_rate,
                    "batch_size": self.batch_size
                }
            )
            print("\nFine-Tuning Response:")
            print(response)
        except openai.OpenAIError as e:
            print(f"OpenAI error: {e}")

    def cancel_fine_tuning_job(self, job_ids):
        try:
            print("cancel_fine_tuning_job")
            for job_id in job_ids:
                if job_id.startswith("ftjob-"):
                    fine_tuning_response = self.fine_tuning_manager.cancel_fine_tuning(job_id)
                    print("\nCancel Fine-Tuning Job Response:")
                    print(fine_tuning_response)
                else:
                    print(f"Invalid job ID format: {job_id}")
        except FineTuningRequestError as e:
            print(f"Fine-tuning request error: {e.message}")
            messagebox.showerror("Error", f"Fine-tuning request error: {e.message}")
        except InvalidFineTuningModelError as e:
            print(f"Invalid fine-tuning model error: {str(e)}")
        except ServiceNotFoundError as e:
            print(f"Service not found error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
