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

config = Settings()


@click.group()
def cli():
    pass


@cli.command
def init():
    """Create the database tables."""
    create_tables(config.db_session)

    logger.success("Tables created")


@cli.command
def load():
    """Load the database tables from files on disk."""
    stations = get_stations(config.stations_metadata_filepath)
    events = get_events(config.events_dir)

    load_stations(stations, session=config.db_session)
    load_events(events, session=config.db_session)

    logger.success("Data loaded")
