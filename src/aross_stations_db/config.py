from functools import cached_property

from dotenv import load_dotenv
from pydantic import DirectoryPath, FilePath, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Add magic support for `.env` file 🪄
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AROSS_")

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
    def db_session(self) -> Session:
        engine = create_engine(str(self.DB_CONNSTR))
        return Session(engine)
