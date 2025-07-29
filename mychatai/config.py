"""Centralised configuration & secrets (Pydantic-Settings)."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── Provider API keys (all optional) ────────────────────────────────────────
    openai_api_key:     Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key:  Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    gemini_api_key:     Optional[str] = Field(None, env="GOOGLE_API_KEY")   # Google Gemini
    deepseek_api_key:   Optional[str] = Field(None, env="DEEPSEEK_API_KEY")

    # ── End-points ─────────────────────────────────────────────────────────────
    ollama_url:  str = Field("http://localhost:11434/api/chat", env="OLLAMA_URL")

    @property
    def ollama_headers(self) -> dict[str, str]:
        """
        Standard request headers for Ollama.

        Always sets Content-Type and, if OLLAMA_TOKEN is provided, adds
        `Authorization: Bearer <token>`.
        """
        headers = {"Content-Type": "application/json"}
       
        return headers

    gemini_url:  str = Field(
        "https://generativelanguage.googleapis.com/v1beta/openai/",
        env="GEMINI_URL",
    )
    deepseek_url: str = Field(
        "https://api.deepseek.com/v1",
        env="DEEPSEEK_URL",
    )

    # ── Model defaults ─────────────────────────────────────────────────────────
    openai_model:    str = "gpt-4o-mini"
    ollama_model:    str = "llama3.2"
    gemini_model:    str = "gemini-2.5-flash"
    anthropic_model: str = "claude-sonnet-4-20250514"
    deepseek_model:  str = "deepseek-chat"

    # ── Misc ───────────────────────────────────────────────────────────────────
    request_timeout: int = 60

    # Pydantic-Settings behaviour
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",        # unknown env-vars won’t raise errors
    )


# Build ONCE; cache forever
@lru_cache
def _build_settings() -> "Settings":
    return Settings()


settings: "Settings" = _build_settings()
