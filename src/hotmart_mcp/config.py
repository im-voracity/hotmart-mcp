from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class HotmartMCPConfig(BaseSettings):
    """Configuration loaded from HOTMART_* environment variables.

    See SPEC.md §2 for details.
    """

    model_config = SettingsConfigDict(
        env_prefix="HOTMART_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    client_id: str
    client_secret: str
    basic: str
    sandbox: bool = False

    @field_validator("client_id", "client_secret", "basic")
    @classmethod
    def _must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            msg = "must not be empty"
            raise ValueError(msg)
        return v
