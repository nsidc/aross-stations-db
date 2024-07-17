import click
from loguru import logger
from sqlalchemy.orm import Session
from tqdm import tqdm

from aross_stations_db.config import CliLoadSettings, Settings
from aross_stations_db.db.setup import (
    generate_event_objects,
    load_events,
    load_stations,
    recreate_tables,
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
    """Create the database tables, dropping any that pre-exist."""
    # TODO: False-positive. Remove type-ignore.
    #       See: https://github.com/pydantic/pydantic/issues/6713
    config = Settings()  # type:ignore[call-arg]

    with Session(config.db_engine) as db_session:
        recreate_tables(db_session)

    logger.success("Database initialized")


@cli.command
def load() -> None:
    """Load the database tables from files on disk."""
    # TODO: False-positive. Remove type-ignore.
    #       See: https://github.com/pydantic/pydantic/issues/6713
    config = CliLoadSettings()  # type:ignore[call-arg]

    raw_stations = get_stations(config.stations_metadata_filepath)
    raw_events = get_events(config.events_dir)

    with Session(config.db_engine) as db_session:
        load_stations(raw_stations, session=db_session)
        logger.info("Loaded stations")

        # The event processing steps are split into stages to provide better feadback at
        # runtime. On slower systems, it can be unclear what the bottleneck is. In the
        # long run, we should try to optimize this after learning more.
        events = generate_event_objects(
            tqdm(raw_events, desc="Reading events"),
        )

        logger.info("Loading events; this can take a minute or so")
        load_events(events, session=db_session)
        logger.info("Loaded events")

    logger.success("Database load complete")
