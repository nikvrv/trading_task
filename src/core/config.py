from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Trading Task"
    database_url: str

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    return Settings()
