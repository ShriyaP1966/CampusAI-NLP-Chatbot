"""Runtime configuration, read from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CORS_ORIGINS = ("http://localhost:5173", "http://127.0.0.1:5173")


def _csv(value: str) -> list[str]:
    return [item.strip().rstrip("/") for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Settings for the API server. See ``.env.example`` for the variable names."""

    docs_dir: Path | None = None
    cors_origins: list[str] = field(default_factory=lambda: list(DEFAULT_CORS_ORIGINS))
    rate_limit_per_minute: int = 30
    max_message_length: int = 500

    @classmethod
    def from_env(cls) -> Settings:
        env = os.environ
        origins = _csv(env.get("CORS_ORIGINS", ""))
        return cls(
            docs_dir=Path(env["CAMPUSAI_DOCS_DIR"]) if env.get("CAMPUSAI_DOCS_DIR") else None,
            cors_origins=origins or list(DEFAULT_CORS_ORIGINS),
            rate_limit_per_minute=int(env.get("RATE_LIMIT_PER_MINUTE", "30")),
            max_message_length=int(env.get("MAX_MESSAGE_LENGTH", "500")),
        )
