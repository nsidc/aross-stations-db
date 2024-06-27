import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from geoalchemy2 import WKTElement
from geojson_pydantic import (
    Feature,
    FeatureCollection,
    Point,
)
from geojson_pydantic.types import Position2D
from sqlalchemy import func
from sqlalchemy.orm import Session

from aross_stations_db.middleware import get_db_session
from aross_stations_db.tables import Event, Station

router = APIRouter(prefix="/v1", tags=["v1"])
GeoJsonReturn = FeatureCollection[Feature[Point, dict[str, object]]]


def _results_to_geojson(
    results: list[tuple[Station, float, float, int]],
) -> GeoJsonReturn:
    return FeatureCollection(
        type="FeatureCollection",
        features=[
            Feature(
                type="Feature",
                properties={
                    "name": station.name,
                    "matching_event_count": event_count,
                },
                geometry=Point(
                    type="Point",
                    coordinates=Position2D(longitude=lon, latitude=lat),
                ),
            )
            for station, lon, lat, event_count in results
        ],
    )


@router.get("/")
def get(
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    db: Annotated[Session, Depends(get_db_session)],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
) -> GeoJsonReturn:
    """Get stations and their events matching query parameters."""
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

    query = query.group_by(Station.id)

    results = query.all()
    return _results_to_geojson(results)
