from functools import cached_property
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath, FilePath, PostgresDsn, computed_field
from sqlalchemy import Engine, create_engine

# Add magic support for `.env` file 🪄
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AROSS_')

    DATA_BASEDIR: DirectoryPath
    DB_CONNSTR: PostgresDsn

    @computed_field
    @cached_property
    def events_dir(self) -> DirectoryPath:
        return self.DATA_BASEDIR / "events"

    @computed_field
    @cached_property
    def stations_metadata_filepath(self) -> FilePath:
        return self.DATA_BASEDIR / "metadata" / "aross.asos_stations.metadata.csv"

    @computed_field
    @cached_property
    def db_engine(self) -> Engine:
        return create_engine(str(self.DB_CONNSTR), echo=True)
