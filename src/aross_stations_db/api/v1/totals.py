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
    monthly_aggregate_query_results_to_plot_buffer
)
from aross_stations_db.db.query import totals_query

router = APIRouter()

PLOT_TITLE = 'Total Rain-on-Snow Events By Month'

@router.get("/monthly")
def get_totals_by_month(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
    stations: Annotated[list[str], Query(description="List of station identifiers")] = [],
) -> list[MonthlyAggregateJsonElement]:
    """Get a set of aggregated totals by month of events matching query parameters."""
    query = totals_query(db=db, start=start, end=end, polygon=polygon, stations=stations)

    return monthly_aggregate_query_results_to_json(query.all())


@router.post("/monthly")
def post_totals_by_month(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Form(description="WKT shape")] = None,
    stations: Annotated[list[str], Form(description="List of station identifiers")] = [],
) -> list[MonthlyAggregateJsonElement]:
    """Get a set of aggregated totals by month of events matching query parameters via POST."""
    query = totals_query(db=db, start=start, end=end, polygon=polygon, stations=stations)

    return monthly_aggregate_query_results_to_json(query.all())


@router.get("/monthly/png")
def get_totals_by_month_png(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
    stations: Annotated[list[str], Query(Description="List of station identifiers")] = [],
) -> StreamingResponse:
    """Get a monthly timeseries image plot of events matching query parameters."""
    query = totals_query(db=db, start=start, end=end, polygon=polygon, stations=stations)
    buffer = monthly_aggregate_query_results_to_plot_buffer(query, start, end, PLOT_TITLE, 'png')

    return StreamingResponse(buffer, media_type="image/png")


@router.post("/monthly/png")
def post_totals_by_month_png(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Form(description="WKT shape")] = None,
    stations: Annotated[list[str], Form(Description="List of station identifiers")] = [],
) -> StreamingResponse:
    """Get a monthly timeseries image plot of events matching query parameters."""
    query = totals_query(db=db, start=start, end=end, polygon=polygon, stations=stations)
    buffer = monthly_aggregate_query_results_to_plot_buffer(query, start, end, PLOT_TITLE, 'png')

    return StreamingResponse(buffer, media_type="image/png")