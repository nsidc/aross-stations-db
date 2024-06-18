import csv
import io

import click

from aross_stations_db.config import Settings
from aross_stations_db.db import create_tables

config = Settings()


@click.group()
def cli():
    pass


@cli.command
def init():
    """Create the database tables."""
    create_tables(config.db_engine)


@cli.command
def load():
    """Load the database tables from files on disk."""

    stations_metadata_str = config.stations_metadata_filepath.read_text()
    stations = list(csv.DictReader(io.StringIO(stations_metadata_str)))

    events = config.events_dir.glob("*.event.csv")

    load_stations(stations)
    load_events(events)
