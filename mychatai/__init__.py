"""
mychatai Unified chat-LLM orchestration layer.

Expose only the high-level façade so that users do:
    from mychatai import ChatService, OpenAIClient, OllamaClient, settings
"""

from .config import settings                       # singleton settings object
from .chat_service import ChatService
from .clients.openai import OpenAIClient
from .clients.ollama import OllamaClient
from .clients.gemini import GeminiClient
from .clients.claude import AnthropicClient
from .clients.deepseek import DeepSeekClient

__all__ = [
    "ChatService",
    "OpenAIClient",
    "OllamaClient",
    "GeminiClient",
    "AnthropicClient",
    "DeepSeekClient",
    "settings",
]
