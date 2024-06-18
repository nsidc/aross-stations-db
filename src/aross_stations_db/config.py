from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath, FilePath, PostgresDsn, computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AROSS_')

    DATA_BASEDIR: DirectoryPath
    DB_CONNSTR: PostgresDsn

    @computed_field
    @property
    def events_dir(self) -> DirectoryPath:
        return self.DATA_BASEDIR / "events"

    @computed_field
    @property
    def metadata_filepath(self) -> FilePath:
        return self.DATA_BASEDIR / "metadata" / "aross.asos_stations.metadata.csv"
