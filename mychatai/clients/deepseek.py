from __future__ import annotations
from collections.abc import Iterable, Generator
from typing import Any, Dict    
from ..config import settings
from .base import AbstractModelClient, message
#from google.generativeai import GenerativeModel, GenerativeModelClient
from openai import OpenAI 



class DeepSeekClient(AbstractModelClient):
    """Thin wrapper around DeepSeek API."""

    def __init__(self, model: str | None = None, *, api_key: str | None = None) -> None:
        self._model = settings.deepseek_model
        deepseek_key = settings.deepseek_api_key
        deepseek_url = settings.deepseek_url
        
        if not deepseek_key:
            raise RuntimeError(
                "DeepSeek API key not found. "
                "Set the DEEPSEEK_API_KEY environment variable or pass api_key=..."
            )
        
        self._client = OpenAI(api_key=deepseek_key, base_url=deepseek_url, timeout=settings.request_timeout)
    
    def chat(
        self,
        messages: Iterable[message],
        *,
        stream: bool = False,
        **kwargs: Any,
    ) -> str | Generator[str, None, None]:
        """Return either the full response text or stream the tokens."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=list(messages),
            stream=stream,
            **kwargs,
        )
        # Note: DeepSeek's API is similar to OpenAI's, so we can use the same method 
        if stream:
            def _generator() -> Generator[str, None, None]:
                for chunk in response:
                    if (delta := chunk.choices[0].delta).content:
                        yield delta.content
            return _generator()

        # non-streamed
        return response.choices[0].message.content