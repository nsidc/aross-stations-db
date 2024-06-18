import datetime as dt
from collections.abc import Iterator

from sqlalchemy.orm import Session

from aross_stations_db.tables import Base, Event, Station


def create_tables(session: Session) -> None:
    """Create all tables.

    IMPORTANT: Because this data is purely derived and can be loaded in a reasonable
               amount of time, there is no need to ever drop tables or migrate data. We
               just start with a fresh database every time we need to change the
               structure.
    """
    Base.metadata.create_all(session.get_bind())


def load_stations(stations: Iterator[dict], *, session: Session) -> None:
    session.add_all(
        [
            Station(
                id=station["stid"],
                name=station["station_name"],
                country_code=station["country"],
                location=_station_location_wkt(station),
            )
            for station in stations
        ]
    )
    session.commit()


def load_events(events: Iterator[dict], *, session: Session) -> None:
    session.add_all(
        [
            Event(
                station_id=event["station_id"],
                start_timestamp=dt.datetime.fromisoformat(event["start"]),
                end_timestamp=dt.datetime.fromisoformat(event["end"]),
            )
            for event in events
        ]
    )
    session.commit()


def _station_location_wkt(station: dict) -> str:
    return f"SRID=4326;POINT({station['longitude']} {station['latitude']})"
