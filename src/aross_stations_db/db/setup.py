import datetime as dt

from sqlalchemy import MetaData, insert
from sqlalchemy.orm import Session

from aross_stations_db.db.tables import Base, Event, Station


def _tables_to_drop(session: Session) -> MetaData:
    """Select our application's tables for dropping.

    This isn't as simple as it sounds, because we want to drop tables, even if we've
    changed the name of the table, without dealing with migrations. We just want to
    start over and we don't want the user to have to know to delete the database files.

    WARNING: This function is fragile! If extensions other than PostGIS are installed,
    or PostGIS changes its use of system tables, or this is deployed using a different
    database than the official PostGIS docker image, it may not work!
    """
    # NOTE: "public" is the default schema. Because we're using the out-of-the-box
    # postgres container image config, this works.
    reflected_md = MetaData(schema="public")
    reflected_md.reflect(
        bind=session.get_bind(),
        only=lambda tablename, _: tablename != "spatial_ref_sys",
    )
    return reflected_md


def recreate_tables(session: Session) -> None:
    """Create all application tables, dropping any pre-existing tables."""
    tables_to_drop = _tables_to_drop(session)
    tables_to_drop.drop_all(bind=session.get_bind())

    Base.metadata.create_all(session.get_bind())
    session.commit()


def load_stations(stations: list[dict[str, str]], *, session: Session) -> None:
    session.add_all(
        [
            Station(
                id=station["stid"],
                name=station["station_name"],
                # HACK: Passing a string for location is "wrong" here, but it's working.
                # Something is being handled implicitly to convert the string to binary
                # (WKB).
                location=_station_location_wkt(station),  # type: ignore[arg-type]
                elevation_meters=float(station["elevation"]),
                record_begins=dt.datetime.fromisoformat(station["record_begins"]),
                timezone_name=station["tzname"],
                country_code=station["country"],
                us_state_abbreviation=station["state"] or None,
                us_county_name=station["county"] or None,
                weather_forecast_office=station["wfo"] or None,
                ugc_county_code=station["ugc_county"] or None,
                ugc_zone_code=station["ugc_zone"] or None,
                iem_network=station["iem_network"],
                iem_climate_site=station["climate_site"] or None,
            )
            for station in stations
        ]
    )
    session.commit()


def generate_event_object(raw_event: dict[str, str]) -> Event:
    return Event(
        station_id=raw_event["station_id"],
        time_start=dt.datetime.fromisoformat(raw_event["start"]),
        time_end=dt.datetime.fromisoformat(raw_event["end"]),
        snow_on_ground=_snow_on_ground_status(raw_event["sog"]),
        rain_hours=int(raw_event["RA"]),
        freezing_rain_hours=int(raw_event["FZRA"]),
        solid_precipitation_hours=int(raw_event["SOLID"]),
        unknown_precipitation_hours=int(raw_event["UP"]),
    )


def load_events(events: list[Event], *, session: Session) -> None:
    """Load events into the database.

    Trying to follow the bulk load instructions, but it's hard to tell why this step
    takes as long as it does. When using tqdm to monitor progress, things "stall" for
    some time after the iterable is consumed. I expected this would not happen because
    of under-the-hood batching, so I'm not really sure how to make this more performant,
    or if we can.
    """
    session.execute(
        insert(Event),
        [event.__dict__ for event in events],
    )

    session.commit()


def _station_location_wkt(station: dict[str, str]) -> str:
    return f"SRID=4326;POINT({station['longitude']} {station['latitude']})"


def _snow_on_ground_status(sog_str: str) -> bool | None:
    if sog_str == "":
        return None
    if sog_str.lower() == "true":
        return True
    if sog_str.lower() == "false":
        return False

    msg = f"Unexpected snow-on-ground value: {sog_str}"
    raise RuntimeError(msg)
