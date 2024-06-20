# Module: chat_completion/chat_completion_models.py
# Description:
# Define models for chat completion requests.
# -----------------------------------------------------------------------------

from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: int
    temperature: float = 1.0
    stop: Optional[List[str]] = None
