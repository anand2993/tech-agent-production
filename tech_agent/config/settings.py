import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model: str = os.getenv("MODEL", "gemini-flash-latest")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    brave_api_key: str | None = os.getenv("BRAVE_API_KEY")
    github_token: str | None = os.getenv("GITHUB_TOKEN")


settings = Settings()
