import datetime as dt

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import RowReturningQuery
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
        .filter(Event.time_start >= start, Event.time_end < end)
    )

    if polygon:
        query = query.filter(
            Station.location.ST_Within(
                func.ST_SetSRID(func.ST_GeomFromText(polygon), 4326),
            )
        )

    return query.group_by(Station.id)


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
    ).filter(Event.time_start >= start, Event.time_end < end)

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
    ).filter(Event.time_start >= start, Event.time_end < end)

    if polygon:
        query = query.join(
            Station,  # TODO: Event.station relationship
        ).filter(
            Station.location.ST_Within(
                func.ST_SetSRID(func.ST_GeomFromText(polygon), 4326),
            )
        )

    return query.group_by("month").order_by("month")
