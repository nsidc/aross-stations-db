import datetime as dt
import io
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Form
from fastapi.responses import StreamingResponse
from geoalchemy2 import WKTElement
import pandas as pd
from sqlalchemy.orm import Session

from aross_stations_db.api.dependencies import get_db_session
from aross_stations_db.api.v1.output import (
    StationsGeoJson,
    stations_query_results_to_geojson,
)
from aross_stations_db.db.query import (
    stations_query,
    station_data_query
)

router = APIRouter()

@router.get("/")
async def get(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")],
    polygon: Annotated[str | None, WKTElement, Query(description="WKT shape")] = None,
) -> StationsGeoJson:
    """Get stations and their events matching query parameters."""
    query = stations_query(db=db, start=start, end=end, polygon=polygon)

    return stations_query_results_to_geojson(query.all())


def station_data(
    db: Session,
    start: dt.datetime | None,
    end: dt.datetime | None,
    stations: list[str]
) -> StreamingResponse:
    now = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    fileRoot = 'stationdata'

    query = station_data_query(db=db, start=start, end=end, stations=stations)
    df = pd.read_sql(query.statement, query.session.connection())

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type='text/csv')
    response.headers['Content-Disposition'] = f"attachment; filename={fileRoot}_{now}.csv"
    return response


@router.get("/data")
async def station_data_get(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Query(description="ISO-format timestamp")] | None = None,
    end: Annotated[dt.datetime, Query(description="ISO-format timestamp")] | None = None,
    stations: Annotated[list[str], Query(description="Station ID(s)")]
) -> StreamingResponse:
    return station_data(db, start, end, stations)


@router.post("/data")
async def station_data_post(
    db: Annotated[Session, Depends(get_db_session)],
    *,
    start: Annotated[dt.datetime, Form(description="ISO-format timestamp")] | None  = None,
    end: Annotated[dt.datetime, Form(description="ISO-format timestamp")] | None  = None,
    stations: Annotated[list[str], Form(description="Station ID(s)")]
) -> StreamingResponse:
    return station_data(db, start, end, stations)