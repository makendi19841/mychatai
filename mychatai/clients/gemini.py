""" from __future__ import annotations
from collections.abc import Iterable, Generator
from typing import Any, Dict    
from ..config import settings
from .base import AbstractModelClient, message
#from google.generativeai import GenerativeModel, GenerativeModelClient
from openai import OpenAI 


class GeminiClient(AbstractModelClient):
    #Thin wrapper around Google Gemini API.

    def __init__(self, model: str | None = None, *, api_key: str | None = None) -> None:
        self._model = settings.gemini_model
        gemini_key = settings.gemini_api_key
        gemini_url = settings.gemini_url
        
        if not gemini_key:
            raise RuntimeError(
                "Gemini API key not found. "
                "Set the GEMINI_API_KEY environment variable or pass api_key=..."
            )
        
        self._client = OpenAI(gemini_key, gemini_url, timeout=settings.request_timeout)
    
    def chat(
        self,
        messages: Iterable[message],
        *,
        stream: bool = False,
        **kwargs: Any,
    ) -> str | Generator[str, None, None]:
        #Return either the full response text or stream the tokens.
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
        return response.choices[0].message.content """

from __future__ import annotations
from collections.abc import Iterable, Generator
from typing import Any, Optional

import google.generativeai as genai

from ..config import settings
from .base import AbstractModelClient, message


class GeminiClient(AbstractModelClient):
    """Wrapper around Google Generative AI / Gemini."""

    def __init__(
        self,
        model: Optional[str] = None,
        *,
        api_key: Optional[str] = None,
        timeout: int | None = None,
    ) -> None:
        key = api_key or settings.gemini_api_key
        if not key:
            raise RuntimeError(
                "Gemini API key not found. "
                "Set GOOGLE_API_KEY (or GEMINI_API_KEY) or pass api_key=..."
            )

        genai.configure(api_key=key, transport="rest")  # or "grpc"
        self._model = model or settings.gemini_model
        self._timeout = timeout or settings.request_timeout

    # --------------------------------------------------------------------- #
    def chat(
        self,
        messages: Iterable[message],
        *,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 1,
        **kwargs: Any,
    ) -> str | Generator[str, None, None]:
        """
        Google’s SDK expects a single flattened prompt string for chat.
        We concatenate the role/content pairs into one long prompt.
        """
        prompt = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)

        gen_model = genai.GenerativeModel(self._model)
        response = gen_model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
            stream=stream,
            **kwargs,
        )

        if stream:
            def _gen() -> Generator[str, None, None]:
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            return _gen()

        return response.text
