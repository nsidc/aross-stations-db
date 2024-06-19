import click
from loguru import logger

from aross_stations_db.config import Settings
from aross_stations_db.db import (
    create_tables,
    load_events,
    load_stations,
)
from aross_stations_db.source_data import (
    get_events,
    get_stations,
)

# TODO: False-positive. Remove type-ignore.
#       See: https://github.com/pydantic/pydantic/issues/6713
config = Settings()  # type:ignore[call-arg]


@click.group()
def cli() -> None:
    pass


@cli.command
def init() -> None:
    """Create the database tables."""
    create_tables(config.db_session)

    logger.success("Tables created")


@cli.command
def load() -> None:
    """Load the database tables from files on disk."""
    stations = get_stations(config.stations_metadata_filepath)
    events = get_events(config.events_dir)

    load_stations(stations, session=config.db_session)
    load_events(events, session=config.db_session)

    logger.success("Data loaded")
