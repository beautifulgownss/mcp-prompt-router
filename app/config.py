from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()