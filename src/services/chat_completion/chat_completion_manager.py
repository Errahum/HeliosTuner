# Module: chat_completion/chat_completion_manager.py
# Description:
# Manages chat completion interactions with the OpenAI API.
# -----------------------------------------------------------------------------

import requests
from ...config import Config
from .chat_completion_service import ChatCompletionService, ChatCompletionRequest
from .chat_completion_exceptions import (
    ServiceNotFoundError, ChatCompletionsRequestError, InvalidChatCompletionsModelError)


class ChatCompletionManager:
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
        endpoint = self.config.get_endpoint('chat_completion')
        param_label = self.config.get_param_label('chat_completion')
        return ChatCompletionService(self.client, endpoint, param_label)

    def create_chat_completion(self, request: ChatCompletionRequest):
        try:
            return self.service.create(request)
        except (ChatCompletionsRequestError, InvalidChatCompletionsModelError) as e:
            raise e
        except Exception as e:
            raise ServiceNotFoundError(f"An unexpected error occurred: {str(e)}")
