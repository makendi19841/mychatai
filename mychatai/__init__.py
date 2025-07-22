"""
mychatai Unified chat-LLM orchestration layer.

Expose only the high-level façade so that users do:
    from mychatai import ChatService, OpenAIClient, OllamaClient, settings
"""

from .config import settings                       # singleton settings object
from .chat_service import ChatService
from .clients.openai import OpenAIClient
from .clients.ollama import OllamaClient

__all__ = [
    "ChatService",
    "OpenAIClient",
    "OllamaClient",
    "settings",
]
