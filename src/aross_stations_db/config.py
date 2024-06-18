from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath, PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AROSS_')

    DATA_DIR: DirectoryPath
    DB_CONNSTR: PostgresDsn
