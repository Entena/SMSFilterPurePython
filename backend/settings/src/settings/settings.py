import os
from typing import Literal
from functools import lru_cache
from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Networking
    ALLOWED_HOSTS: list[str] = Field(..., description="Allowed hosts")
    # App Settings
    APP_DIR: str = Field(..., description="App Directory")
    # Categories
    VIOLENT: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for violent content",
    )
    NON_VIOLENT_ILLEGAL_ACTS: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for non-violent illegal acts",
    )
    SEXUAL_CONTENT_OR_SEXUAL_ACTS: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for sexual content or sexual acts",
    )
    PII: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for PII",
    )
    SUICIDE_AND_SELF_HARM: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for suicide and self-harm",
    )
    UNETHICAL_ACTS: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for unethical acts",
    )
    POLITICALLY_SENSITIVE_TOPICS: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for politically sensitive topics",
    )
    COPYRIGHT_VIOLATION: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for copyright violation",
    )
    JAILBREAK: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for jailbreak",
    )
    NONE: Literal["None", "Unsafe", "Controversial"] = Field(
        "Unsafe",
        description="Block level for none",
    )
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    env_file = os.getenv("ENV_FILE", ".env")
    return Settings(_env_file=env_file) if env_file else Settings()
