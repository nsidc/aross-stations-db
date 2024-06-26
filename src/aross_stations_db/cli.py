import click
from loguru import logger
from sqlalchemy.orm import Session

from aross_stations_db.config import CliLoadSettings, Settings
from aross_stations_db.db import (
    create_tables,
    load_events,
    load_stations,
)
from aross_stations_db.source_data import (
    get_events,
    get_stations,
)


@click.group()
def cli() -> None:
    pass


@cli.command
def init() -> None:
    """Create the database tables."""
    # TODO: False-positive. Remove type-ignore.
    #       See: https://github.com/pydantic/pydantic/issues/6713
    config = Settings()  # type:ignore[call-arg]

    with Session(config.db_engine) as db_session:
        create_tables(db_session)

    logger.success("Tables created")


@cli.command
def load() -> None:
    """Load the database tables from files on disk."""
    # TODO: False-positive. Remove type-ignore.
    #       See: https://github.com/pydantic/pydantic/issues/6713
    config = CliLoadSettings()  # type:ignore[call-arg]

    stations = get_stations(config.stations_metadata_filepath)
    events = get_events(config.events_dir)

    with Session(config.db_engine) as db_session:
        load_stations(stations, session=db_session)
        load_events(events, session=db_session)

    logger.success("Data loaded")
