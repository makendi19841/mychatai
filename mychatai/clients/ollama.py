from __future__ import annotations 
import httpx
import requests
import json
from typing import Iterable, Generator, Dict, Any
from .base import AbstractModelClient, message
from ..config import settings


class OllamaClient(AbstractModelClient):
    """ HTTP client for the Ollama /api/chat endpoint."""

    def __init__(self, model: str | None = None, *, client: httpx.Client | None = None):
        self._base_url = settings.ollama_url
        self._model = settings.ollama_model
        self._headers = settings.ollama_headers
        self._client = client or httpx.Client(timeout=settings.request_timeout)

    def chat(self, messages: Iterable[message], *, stream: bool = False, **kwargs: Any,) -> str | Generator[str, None, None]:
        payload = {
            "model": self._model,
            "messages": list(messages),
            "stream": stream,
            **kwargs,
        }
        if stream:
            response = self._client.post(self._base_url, json=payload, headers=self._headers)  
            response.raise_for_status()

            def _generator():
                for line in response.iter_lines():
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    if data.get("done"):
                        break
                    yield data["message"]["content"]

            return _generator()
        response = self._client.post(self._base_url, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]



        


