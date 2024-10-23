# Module: chat_completion/chat_completion_service.py
# Description:
# Service for generating chat completions using OpenAI API.
# -----------------------------------------------------------------------------

import requests
from .chat_completion_exceptions import ChatCompletionsRequestError, InvalidChatCompletionsModelError
from .chat_completion_models import ChatCompletionRequest
import logging


class ChatCompletionService:
    """Service for generating chat completions using OpenAI API."""

    def __init__(self, client, endpoint: str, param_label: str):
        self.client = client
        self.endpoint = endpoint
        self.param_label = param_label
        self.logger = logging.getLogger(__name__)

    def create(self, request: ChatCompletionRequest) -> str:
        self.logger.debug("Creating chat completion with request: %s", request)

        data = {
            self.param_label: [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "model": request.model,
            "stop": request.stop
        }

        try:
            response = self.client.post(self.endpoint, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json()

            if 'choices' in result:
                return result['choices'][0]['message']['content']
            else:
                raise ChatCompletionsRequestError("Invalid response format")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            self.logger.error("HTTP error occurred: %s", e)
            if status_code == 404:
                raise ChatCompletionsRequestError("Endpoint not found", status_code=status_code)
            elif status_code == 401:
                raise ChatCompletionsRequestError("Unauthorized access - check your API key", status_code=status_code)
            else:
                raise ChatCompletionsRequestError(f"HTTP error occurred: {str(e)}", status_code=status_code)
        except requests.RequestException as e:
            self.logger.error("Request error occurred: %s", e)
            raise ChatCompletionsRequestError(f"Failed to create chat completion: {str(e)}")
        except Exception as e:
            self.logger.error("Unexpected error occurred: %s", e)
            raise InvalidChatCompletionsModelError(f"An unexpected error occurred: {str(e)}")
