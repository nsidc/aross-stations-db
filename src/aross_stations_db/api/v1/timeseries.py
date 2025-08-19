import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query
from fastapi.responses import StreamingResponse
from geoalchemy2 import WKTElement
import pandas as pd
from sqlalchemy.orm import Session

from aross_stations_db.api.dependencies import get_db_session
from aross_stations_db.api.v1.output import (
    TimeseriesJsonElement,
    timeseries_query_results_to_json,
    timeseries_query_results_to_bar_plot_buffer,
)
from aross_stations_db.db.query import timeseries_query

from loguru import logger

router = APIRouter()

@router.get("/monthly")
def get_monthly_timeseries(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
    stations: Annotated[list[str], Query(description="List of station identifiers")] = [],
) -> list[TimeseriesJsonElement]:
    """Get a monthly timeseries of events matching query parameters."""
    logger.debug(f"STATIONS: {stations}")
    query = timeseries_query(db=db, start=start, end=end, polygon=polygon, stations=stations)

    return timeseries_query_results_to_json(query.all())


@router.post("/monthly")
def post_monthly_timeseries(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Form(description="WKT shape")] = None,
    stations: Annotated[list[str], Form(description="List of station identifiers")] = [],
) -> list[TimeseriesJsonElement]:
    """Get a monthly timeseries of events matching query parameters."""
    logger.debug(f"STATIONS: {stations}")
    query = timeseries_query(db=db, start=start, end=end, polygon=polygon, stations=stations)

    return timeseries_query_results_to_json(query.all())


@router.get("/monthly/png")
def get_monthly_timeseries_png(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
    stations: Annotated[list[str], Query(Description="List of station identifiers")] = [],
) -> StreamingResponse:
    """Get a monthly timeseries image plot of events matching query parameters."""
    query = timeseries_query(db=db, start=start, end=end, polygon=polygon, stations=stations)
    buffer = timeseries_query_results_to_bar_plot_buffer(query, start, end, 'png')

    return StreamingResponse(buffer, media_type="image/png")


@router.post("/monthly/png")
def post_monthly_timeseries_png(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Form(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Form(description="WKT shape")] = None,
    stations: Annotated[list[str], Form(Description="List of station identifiers")] = [],
) -> StreamingResponse:
    """Get a monthly timeseries image plot of events matching query parameters."""
    query = timeseries_query(db=db, start=start, end=end, polygon=polygon, stations=stations)
    buffer = timeseries_query_results_to_bar_plot_buffer(query, start, end, 'png')
    
    return StreamingResponse(buffer, media_type="image/png")
