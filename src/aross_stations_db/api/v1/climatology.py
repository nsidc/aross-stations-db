import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query
from fastapi.responses import StreamingResponse
from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

from aross_stations_db.api.dependencies import get_db_session
from aross_stations_db.api.v1.output import (
    MonthlyAggregateJsonElement,
    monthly_aggregate_query_results_to_json,
)
from aross_stations_db.db.query import climatology_query

router = APIRouter()


# TODO: For all these methods, we may want to validate query spans >1 year? 
# Or >= 2 years? Should the query parameters be changed to enforce best
# practices for visualizing a climatology (e.g. there should always be the
# same number of Januaries as Februaries as ...etc., so we could accept a
# start year, end year, and start month.)
#
# ALSO: Currently, these aren't actually climatologies, they are just aggregate
# totals by month.  To get a true climatology average for each month, we will
# need to take the average from each year and divide it by some number of years.
# For that to be accurate, though, we need to know the true number of years to
# divide by.  For a single station, this is easy of the range is insdie the maximum/
# minimum dates for the station, but if the range it outside, it's hard to know
# if the months with 0 events are because of "no data" (stations wasn't functional)
# or if it truly is 0.  For multiple stations, it can get tricky because different
# stations could have different start/end dates.
#
# For now, leaving these here as stubs for later, but this may need to be refactored
# in the future.

@router.get("/monthly")
def get_monthly_climatology(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
    stations: Annotated[list[str], Query(description="List of station identifiers")] = [],
) -> list[MonthlyAggregateJsonElement]:
    """Get a monthly climatology of events matching query parameters."""
    query = climatology_query(db=db, start=start, end=end, polygon=polygon, stations=stations)

    return monthly_aggregate_query_results_to_json(query.all())


@router.post("/monthly")
def post_monthly_climatology(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Form(description="WKT shape")] = None,
    stations: Annotated[list[str], Form(description="List of station identifiers")] = [],
) -> list[MonthlyAggregateJsonElement]:
    """Get a monthly climatology of events matching query parameters via POST."""
    query = climatology_query(db=db, start=start, end=end, polygon=polygon, stations=stations)

    return monthly_aggregate_query_results_to_json(query.all())
