# Module: fine_tuning/fine_tuning_manager.py
# Description:
# Manages fine-tuning interactions with the OpenAI API.
# -----------------------------------------------------------------------------

import requests

from .fine_tuning_exceptions import FineTuningRequestError, InvalidFineTuningModelError, ServiceNotFoundError
from .fine_tuning_service import FineTuningService
from ...config import Config


class FineTuningManager:
    def __init__(self, config: Config):
        self.config = config
        self.client = self.initialize_client()
        self.service = self.create_service()

    def initialize_client(self):
        api_key = self.config.get_api_key()
        if not api_key:
            raise ValueError("API key is missing")
        session = requests.Session()
        session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        return session

    def create_service(self):
        endpoint = self.config.get_endpoint('fine_tuning')
        param_label = self.config.get_param_label('fine_tuning')
        return FineTuningService(self.client, endpoint, param_label)

    def cancel_fine_tuning(self, job_id: str):
        try:
            return self.service.cancel(job_id)
        except (FineTuningRequestError, InvalidFineTuningModelError) as e:
            raise e
        except Exception as e:
            raise ServiceNotFoundError(f"An unexpected error occurred: {str(e)}")
