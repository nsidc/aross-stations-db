import datetime as dt

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import RowReturningQuery
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.types import DateTime, Float

from aross_stations_db.db.tables import Event, Station


def stations_query(
    db: Session,
    *,
    start: dt.datetime,
    end: dt.datetime,
    polygon: str | None = None,
) -> RowReturningQuery[tuple[Station, float, float, int]]:
    query = (
        db.query(
            Station,
            func.ST_X(Station.location, type_=Float),
            func.ST_Y(Station.location, type_=Float),
            func.count(),
        )
        .join(
            Event,
        )
        .filter(*_rain_on_snow_event_filter(start=start, end=end))
    )

    if polygon:
        query = query.filter(
            Station.location.ST_Within(
                func.ST_SetSRID(func.ST_GeomFromText(polygon), 4326),
            )
        )

    return query.group_by(Station.id)


def station_data_query(
    db: Session,
    *,
    start: dt.datetime,
    end: dt.datetime,
    stations: list[str] = [],
) -> RowReturningQuery[tuple[str, dt.datetime, dt.datetime, bool | None, int, int, int, int]]:
    print(type(stations))
    query = db.query(Event).filter(Event.station_id.in_(stations))

    if start is not None:
        query = query.filter(Event.time_start >= start)
    if end is not None:
        query = query.filter(Event.time_end < end)

    return query.order_by(Event.station_id)


def timeseries_query(
    db: Session,
    *,
    start: dt.datetime,
    end: dt.datetime,
    polygon: str | None = None,
) -> RowReturningQuery[tuple[dt.datetime, int]]:
    query = db.query(
        func.date_trunc("month", Event.time_start, type_=DateTime).label("month"),
        func.count(Event.time_start).label("count"),
    ).filter(*_rain_on_snow_event_filter(start=start, end=end))

    if polygon:
        query = query.join(
            Station,  # TODO: Event.station relationship
        ).filter(
            Station.location.ST_Within(
                func.ST_SetSRID(func.ST_GeomFromText(polygon), 4326),
            )
        )

    return query.group_by("month").order_by("month")


def climatology_query(
    db: Session,
    *,
    start: dt.datetime,
    end: dt.datetime,
    polygon: str | None = None,
) -> RowReturningQuery[tuple[int, int]]:
    query = db.query(
        func.extract("month", Event.time_start).label("month"),
        func.count(Event.time_start).label("count"),
    ).filter(*_rain_on_snow_event_filter(start=start, end=end))

    if polygon:
        query = query.join(
            Station,  # TODO: Event.station relationship
        ).filter(
            Station.location.ST_Within(
                func.ST_SetSRID(func.ST_GeomFromText(polygon), 4326),
            )
        )

    return query.group_by("month").order_by("month")


def _rain_on_snow_event_filter(
    *,
    start: dt.datetime,
    end: dt.datetime,
) -> list[ColumnElement[bool]]:
    """Return filter predicates for selecting rain on snow events within timeframe."""
    return [
        Event.time_start >= start,
        Event.time_end < end,
        # Snow today events occur when snow is on the ground and rain was detected in at
        # least one hour.
        Event.snow_on_ground == True,  # noqa: E712
        Event.rain_hours >= 1,
    ]
