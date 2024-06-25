import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from geoalchemy2 import WKBElement
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from aross_stations_db.middleware import get_db_session
from aross_stations_db.tables import Event, Station

router = APIRouter(prefix="/v1", tags=["v1"])


class ReturnElement(BaseModel):
    name: str
    location: str
    event_count: int


@router.get("/")
def get(
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    db: Annotated[Session, Depends(get_db_session)],
    polygon: Annotated[str | None, WKBElement, Query(description="WKT shape")] = None,
) -> list[ReturnElement]:
    """Get stations and their events matching query parameters."""
    query = (
        db.query(
            Station,
            Station.location.ST_AsEWKT(),
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

    query = query.group_by(Station.id)

    results = query.all()
    return [
        ReturnElement(
            name=station.name,
            location=location,
            event_count=event_count,
        )
        for station, location, event_count in results
    ]
