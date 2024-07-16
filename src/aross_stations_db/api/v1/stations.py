import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

from aross_stations_db.api.dependencies import get_db_session
from aross_stations_db.api.v1.output import (
    StationsGeoJson,
    stations_query_results_to_geojson,
)
from aross_stations_db.query import stations_query

router = APIRouter()


@router.get("/")
def get(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
) -> StationsGeoJson:
    """Get stations and their events matching query parameters."""
    query = stations_query(db=db, start=start, end=end, polygon=polygon)

    return stations_query_results_to_geojson(query.all())
