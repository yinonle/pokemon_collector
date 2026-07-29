from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str = ("postgresql://postgres:postgres@127.0.0.1:5434/pokedex_db")
    AWS_REGION: str = "us-east-1"
    SQS_ENDPOINT_URL: Optional[str] = (None)
    
    INPUT_QUEUE_NAME: str = "sqs_in"
    OUTPUT_QUEUE_NAME: str = "sqs_out"

    POKEMON_BASE_URL: str = "https://pokemondb.net/pokedex/"

    
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36")

    JSON_FILE_PATH: str = "pokedex_backup.json"
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "app.log"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()