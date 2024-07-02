import datetime as dt

from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from aross_stations_db.tables import Event, Station


def stations_query(
    db: Session,
    start: dt.datetime,
    end: dt.datetime,
    polygon: str | None = None,
) -> Query:
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
