import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

from aross_stations_db.api.v1.output import (
    TimeseriesJsonElement,
    timeseries_query_results_to_json,
)
from aross_stations_db.middleware import get_db_session
from aross_stations_db.query import timeseries_query

router = APIRouter()


@router.get("/monthly")
def get_monthly(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
) -> list[TimeseriesJsonElement]:
    """Get a monthly timeseries of events matching query parameters."""
    query = timeseries_query(db=db, start=start, end=end, polygon=polygon)

    return timeseries_query_results_to_json(query.all())
