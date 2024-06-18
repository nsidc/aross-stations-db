from loguru import logger
from pydantic import PostgresDsn
from sqlalchemy import Engine, MetaData

from aross_stations_db.tables import Base


def create_tables(engine: Engine) -> None:
    """Create all tables.

    IMPORTANT: Because this data is purely derived and can be loaded in a reasonable
               amount of time, there is no need to ever drop tables or migrate data. We
               just start with a fresh database every time we need to change the
               structure.
    """
    Base.metadata.create_all(engine)
    logger.success("Tables created.")
