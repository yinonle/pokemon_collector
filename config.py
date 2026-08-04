from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str = ("postgresql://postgres:postgres@127.0.0.1:5434/pokedex_db")
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = "testing"
    AWS_SECRET_ACCESS_KEY: str = "testing"
    SQS_ENDPOINT_URL: Optional[str] = None
    
    INPUT_QUEUE_NAME: str = "sqs_in"
    OUTPUT_QUEUE_NAME: str = "sqs_out"

    INPUT_QUEUE_URL: str = "http://localhost:4566/000000000000/pokemon_input_queue"
    OUTPUT_QUEUE_URL: str = "http://localhost:4566/000000000000/pokemon_output_queue"

    POKEMON_BASE_URL: str = "https://pokemondb.net/pokedex/"

    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36")

    JSON_FILE_PATH: str = "pokedex_backup.json"
    
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "app.log"

    class Config:
        env_file = ".env"

settings = Settings()