import datetime as dt

from geojson_pydantic import (
    Feature,
    FeatureCollection,
    Point,
)
from geojson_pydantic.types import Position2D
from pydantic import BaseModel
from sqlalchemy import Row

from aross_stations_db.tables import Station

StationsGeoJson = FeatureCollection[Feature[Point, dict[str, object]]]


def stations_query_results_to_geojson(
    results: list[Row[tuple[Station, float, float, int]]],
) -> StationsGeoJson:
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


class TimeseriesJsonElement(BaseModel):
    date: dt.date
    event_count: int


def timeseries_query_results_to_json(
    results: list[Row[tuple[dt.datetime, int]]],
) -> list[TimeseriesJsonElement]:
    return [
        TimeseriesJsonElement(date=date, event_count=event_count)
        for date, event_count in results
    ]
