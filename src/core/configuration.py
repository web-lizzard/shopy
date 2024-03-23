from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class DatabaseConfiguration(BaseModel):
    url: PostgresDsn


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    is_debug: bool = False
    port: int = 80

    database: DatabaseConfiguration


configuration = Configuration()
