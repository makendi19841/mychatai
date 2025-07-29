from __future__ import annotations

from collections.abc import Iterable, Generator
from typing import Any

import anthropic

from ..config import settings
from .base import AbstractModelClient, message         # ✅ correct alias
from ..prompts import _SYSTEM_PROMPT                     # (build_messages is used earlier in ChatService)


class AnthropicClient(AbstractModelClient):
    """Thin wrapper around Anthropic Claude API."""

    def __init__(
        self,
        model: str | None = None,
        *,
        api_key: str | None = None,
        timeout: int | None = None,
    ) -> None:
        self._model = model or settings.anthropic_model
        key = api_key or settings.anthropic_api_key
        if not key:
            raise RuntimeError(
                "Anthropic API key not found. "
                "Set ANTHROPIC_API_KEY or pass api_key=..."
            )

        self._client = anthropic.Anthropic(
            api_key=key,
            timeout=timeout or settings.request_timeout,
        )

    # ------------------------------------------------------------------ #
    def chat(
        self,
        messages: Iterable[message],
        *,
        stream: bool = False,
        max_tokens: int = 900,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str | Generator[str, None, None]:
        """
        Call Claude 3.  Any 'system' role in the incoming list is hoisted
        to the top-level system= parameter as Anthropic requires.
        """
        msgs = list(messages)  # materialise the iterator once

        # ── Hoist the system prompt (if present) ────────────────────────────
        sys_prompt = _SYSTEM_PROMPT
        pruned: list[dict[str, str]] = []
        for m in msgs:
            if m.get("role") == "system" and not pruned:
                sys_prompt = m["content"]
                continue                    # drop from messages[]
            pruned.append(m)                # keep user/assistant

        response = self._client.messages.create(
            model=self._model,
            system=sys_prompt,
            messages=pruned,                # no 'system' roles here
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
            **kwargs,
        )

        if stream:
            def _generator() -> Generator[str, None, None]:
                for chunk in response:
                    for block in chunk.content:
                        if block.type == "text":
                            yield block.text
            return _generator()

        return "".join(
            block.text for block in response.content if block.type == "text"
        )