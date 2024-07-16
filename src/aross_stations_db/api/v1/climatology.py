import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

from aross_stations_db.api.dependencies import get_db_session
from aross_stations_db.api.v1.output import (
    ClimatologyJsonElement,
    climatology_query_results_to_json,
)
from aross_stations_db.query import climatology_query

router = APIRouter()


@router.get("/monthly")
def get_monthly_climatology(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
) -> list[ClimatologyJsonElement]:
    """Get a monthly climatology of events matching query parameters."""
    # TODO: Validate query spans >1 year? Or >= 2 years? Should the query parameters be
    # changed to enforce best practices for visualizing a climatology (e.g. there
    # should always be the same number of Januaries as Februaries as ...etc., so we
    # could accept a start year, end year, and start month.)
    query = climatology_query(db=db, start=start, end=end, polygon=polygon)

    return climatology_query_results_to_json(query.all())
