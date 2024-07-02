import datetime as dt

from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from aross_stations_db.tables import Event, Station


def stations_query(
    db: Session,
    *,
    start: dt.datetime,
    end: dt.datetime,
    polygon: str | None = None,
) -> Query[Station, float, float, int]:
    query = (
        db.query(
            Station,
            Station.location.ST_X(),
            Station.location.ST_Y(),
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
) -> Query[dt.date, int]:
    query = db.query(
        func.date_trunc("month", Event.time_start).label("month"),
        func.count(Event.time_start).label("count"),
    ).filter(Event.time_start >= start, Event.time_end < end)

    if polygon:
        query = query.join(
            Station,
        ).filter(
            Station.location.ST_Within(
                func.ST_SetSRID(func.ST_GeomFromText(polygon), 4326),
            )
        )

    return query.group_by("month").order_by("month")
