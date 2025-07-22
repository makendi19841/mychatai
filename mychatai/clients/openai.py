from __future__ import annotations
from collections.abc import Iterable, Generator
from typing import Any, Dict

from ..config import settings
from .base import AbstractModelClient, message

# Lazy import so the package is optional until the client is used
from openai import OpenAI


class OpenAIClient(AbstractModelClient):
    """Thin wrapper around openai.chat.completions.create (v1 Python SDK)."""

    def __init__(self, model: str | None = None, *, api_key: str | None = None) -> None:
        self._model = settings.openai_model
        key = settings.openai_api_key
       
        if not key:
            raise RuntimeError(
                "OpenAI API key not found. "
                "Set the OPENAI_API_KEY environment variable or pass api_key=..."
            )
        # create a dedicated client instance instead of mutating global state
        self._client = OpenAI(api_key=key, timeout=settings.request_timeout)

    # ──────────────────────────────────────────────────────────────────────────
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

        if stream:
            def _generator() -> Generator[str, None, None]:
                for chunk in response:
                    if (delta := chunk.choices[0].delta).content:
                        yield delta.content
            return _generator()

        # non-streamed
        return response.choices[0].message.content
