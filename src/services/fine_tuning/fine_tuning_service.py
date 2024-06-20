# Module: fine_tuning/fine_tuning_service.py
# Description:
# Service for fine-tuning models using OpenAI API.
# -----------------------------------------------------------------------------

import requests
from .fine_tuning_exceptions import FineTuningRequestError, InvalidFineTuningModelError


class FineTuningService:
    """Service for fine-tuning models using OpenAI API."""

    def __init__(self, client, endpoint: str, param_label: str):
        self.client = client
        self.endpoint = endpoint
        self.param_label = param_label

    def create(self, request) -> dict:
        """Create a fine-tuning job using the OpenAI fine-tuning endpoint."""
        data = {self.param_label: request.params}
        try:
            response = self.client.post(self.endpoint, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise FineTuningRequestError(f"Failed to create fine-tuning job: {str(e)}")
        except Exception as e:
            raise InvalidFineTuningModelError(f"An unexpected error occurred: {str(e)}")

    def retrieve(self, job_id: str) -> dict:
        """Retrieve a fine-tuning job using the OpenAI fine-tuning endpoint."""
        url = f"{self.endpoint}/{job_id}"
        try:
            response = self.client.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise FineTuningRequestError(f"Failed to retrieve fine-tuning job: {str(e)}")
        except Exception as e:
            raise InvalidFineTuningModelError(f"An unexpected error occurred: {str(e)}")

    def list(self) -> list:
        """List all fine-tuning jobs using the OpenAI fine-tuning endpoint."""
        try:
            response = self.client.get(self.endpoint)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.RequestException as e:
            raise FineTuningRequestError(f"Failed to list fine-tuning jobs: {str(e)}")
        except Exception as e:
            raise InvalidFineTuningModelError(f"An unexpected error occurred: {str(e)}")

    def cancel(self, job_id: str) -> dict:
        """Cancel a fine-tuning job using the OpenAI fine-tuning endpoint."""
        url = f"{self.endpoint}/{job_id}/cancel"
        try:
            response = self.client.post(url, json={})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise FineTuningRequestError(f"Failed to cancel fine-tuning job: {str(e)}")
        except Exception as e:
            raise InvalidFineTuningModelError(f"An unexpected error occurred: {str(e)}")
