import csv
import io
from collections.abc import Iterator
from pathlib import Path

from loguru import logger


def get_stations(metadata_fp: Path) -> list[dict[str, str]]:
    stations_metadata_str = metadata_fp.read_text()
    stations_metadata = list(csv.DictReader(io.StringIO(stations_metadata_str)))

    logger.info(f"Found {len(stations_metadata)} stations")
    return stations_metadata


def get_event_files(events_dir: Path) -> list[Path]:
    event_files = list(events_dir.glob("*.event.csv"))

    logger.info(f"Found {len(event_files)} event files")
    return event_files


def get_events(events_dir: Path) -> Iterator[dict[str, str]]:
    for event_fp in get_event_files(events_dir):
        station_id = event_fp.stem.split(".")[0]

        with event_fp.open() as event_file:
            events = list(csv.DictReader(event_file))

        for event in events:
            yield {
                "station_id": station_id,
                **event,
            }
