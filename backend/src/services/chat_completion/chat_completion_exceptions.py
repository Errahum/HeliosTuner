# Module: chat_completion/chat_completion_exceptions.py
# Description:
# Define exceptions related to chat completion operations.
# -----------------------------------------------------------------------------

class ChatCompletionsError(Exception):
    """Base class for all chat completions related exceptions."""
    pass

class ChatCompletionsRequestError(ChatCompletionsError):
    """Raised when a request to the chat completions endpoint fails."""
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InvalidChatCompletionsModelError(ChatCompletionsError):
    """Raised when an invalid or deprecated model is used for chat completions."""
    pass

class ServiceNotFoundError(ChatCompletionsError):
    """Raised when a requested service is not found."""
    pass
