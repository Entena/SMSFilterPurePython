import os
from functools import lru_cache
from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Quantization(str, Enum):
    Q2_K = "Q2_K"
    Q3_K_L = "Q3_K_L"
    Q3_K_M = "Q3_K_M"
    Q3_K_S = "Q3_K_S"
    Q4_0 = "Q4_0"
    Q4_1 = "Q4_1"
    Q4_K_M = "Q4_K_M"
    Q4_K_S = "Q4_K_S"
    Q5_0 = "Q5_0"
    Q5_1 = "Q5_1"
    Q5_K_M = "Q5_K_M"
    Q5_K_S = "Q5_K_S"
    Q6_K = "Q6_K"
    Q8_0 = "Q8_0"


class DefaultCategories(str, Enum):
    VIOLENT_CRIMES = "Violent Crimes"
    NONVIOLENT_CRIMES = "Non-violent Crimes"
    SEX_RELATED_CRIMES = "Sex-related Crimes"
    CHILD_SEXUAL_EXPLOITATION = "Child Sexual Exploitation"
    DEFAMATION = "Defamation"
    SPECIALIZED_ADVICE = "Specialized Advice"
    PRIVACY = "Privacy"
    INTELLECTUAL_PROPERTY = "Intellectual Property"
    INDISCRIMINATE_WEAPONS = "Indiscriminate Weapons"
    HATE = "Hate"
    SUICIDE_AND_SELF_HARM = "Suicide & Self Harm"
    SEXUAL_CONTENT = "Sexual Content"
    ELECTIONS = "Elections"


class Settings(BaseSettings):
    # Networking
    ALLOWED_HOSTS: list[str] = Field(..., description="Allowed hosts")
    # App Settings
    APP_DIR: str = Field(..., description="App Directory")
    # Quantization
    QUANT: Quantization = Field(..., description="Quantization")
    # Categories
    EXCL: list[DefaultCategories] = Field(
        ..., description="Excluded default categories"
    )
    INCL: list[str] = Field(..., description="Descriptions of additional categories")
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    env_file = os.getenv("ENV_FILE", ".env")
    return Settings(_env_file=env_file) if env_file else Settings()
