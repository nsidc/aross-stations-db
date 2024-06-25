from functools import cached_property

from dotenv import load_dotenv
from pydantic import DirectoryPath, FilePath, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Engine, create_engine

# Add magic support for `.env` file 🪄
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AROSS_")

    DATA_BASEDIR: DirectoryPath
    DB_CONNSTR: PostgresDsn

    # TODO: Specifically ignore this type of error instead of using type-ignore; but
    # mypy doesn't yet categorize this error in its own type, so we need to wait for a
    # release, likely 1.11:  https://github.com/python/mypy/pull/16571/files
    @computed_field  # type:ignore[misc]
    @cached_property
    def events_dir(self) -> DirectoryPath:
        return self.DATA_BASEDIR / "events"

    @computed_field  # type:ignore[misc]
    @cached_property
    def stations_metadata_filepath(self) -> FilePath:
        return self.DATA_BASEDIR / "metadata" / "aross.asos_stations.metadata.csv"

    # TODO: Remove?
    @computed_field  # type:ignore[misc]
    @cached_property
    def db_engine(self) -> Engine:
        return create_engine(str(self.DB_CONNSTR))
