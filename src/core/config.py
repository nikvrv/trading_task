from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     project_name: str = 'Trading Task'
#     database_url: str
#     project_host: str
#     project_port: str
#
#     model_config = SettingsConfigDict(env_file=".env")
# from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

# settings = Settings()
