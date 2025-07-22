"""High-level façade that orchestrates prompts and model calls."""
from __future__ import annotations
from typing import Iterable, Generator
from .clients.base import AbstractModelClient
from .prompts import build_messages


class ChatService:
    def  __init__(self, model_client: AbstractModelClient):
         self._model = model_client

    def answer(
        self,
        question: str,
        stream: bool = False,
        **model_kwargs,
    ) -> str | Generator[str, None, None]:
        messages = build_messages(question)
        return self._model.chat(messages, stream=stream, **model_kwargs)
