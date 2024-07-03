import datetime as dt
from typing import cast

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import RowReturningQuery

from aross_stations_db.tables import Event, Station


def stations_query(
    db: Session,
    *,
    start: dt.datetime,
    end: dt.datetime,
    polygon: str | None = None,
) -> RowReturningQuery[tuple[Station, float, float, int]]:
    query = (
        cast(
            # TODO: A better way! Avoid duplicating information; the type of Station and
            # func.count() can be inferred automatically, but not ST_X().
            #       https://github.com/sqlalchemy/sqlalchemy/discussions/11564
            RowReturningQuery[tuple[Station, float, float, int]],
            db.query(
                Station,
                Station.location.ST_X(),
                Station.location.ST_Y(),
                func.count(),
            ),
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
    query = cast(
        # TODO: A better way! Avoid duplicating information; the type of func.count()
        # can be inferred automatically, but not func.date_trunc().
        #       https://github.com/sqlalchemy/sqlalchemy/discussions/11564
        RowReturningQuery[tuple[dt.datetime, int]],
        db.query(
            func.date_trunc("month", Event.time_start).label("month"),
            func.count(Event.time_start).label("count"),
        ),
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
    query = cast(
        # TODO: A better way! Avoid duplicating information; the type of func.count()
        # can be inferred automatically, but not func.date_trunc().
        #       https://github.com/sqlalchemy/sqlalchemy/discussions/11564
        RowReturningQuery[tuple[int, int]],
        db.query(
            func.extract("month", Event.time_start).label("month"),
            func.count(Event.time_start).label("count"),
        ),
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
