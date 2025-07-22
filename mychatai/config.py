"""Centralised configuration & secrets (Pydantic-Settings)."""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ── API keys / endpoints ────────────────────────────────────────────────────
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    ollama_url: str = Field(                                     # noqa: RUF001
        default="http://localhost:11434/api/chat",
        env="OLLAMA_URL",
    )

    # ── Model defaults (just regular fields, but **typed**) ────────────────────
    openai_model: str = Field(default="gpt-4o-mini")
    ollama_model: str = Field(default="llama3.2")

    # ── Miscellaneous ──────────────────────────────────────────────────────────
    request_timeout: int = Field(default=60)

    # Tell pydantic-settings to read a local .env file if present
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

# Build ONCE; cache forever
@lru_cache
def _build_settings() -> Settings:
    return Settings()

settings: Settings = _build_settings()
