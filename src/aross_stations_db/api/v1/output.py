import datetime as dt
from typing import Annotated

from annotated_types import Ge, Le
from geojson_pydantic import (
    Feature,
    FeatureCollection,
    Point,
)
from geojson_pydantic.types import Position2D
from pydantic import BaseModel
from sqlalchemy import Row

from aross_stations_db.db.tables import Station

StationsGeoJson = FeatureCollection[Feature[Point, dict[str, object]]]


def stations_query_results_to_geojson(
    results: list[Row[tuple[Station, float, float, int]]],
) -> StationsGeoJson:
    return FeatureCollection(
        type="FeatureCollection",
        features=[
            Feature(
                type="Feature",
                geometry=Point(
                    type="Point",
                    coordinates=Position2D(longitude=lon, latitude=lat),
                ),
                properties={
                    "id": station.id,
                    "name": station.name,
                    "elevation_meters": station.elevation_meters,
                    "record_begins": station.record_begins,
                    "timezone_name": station.timezone_name,
                    "country_code": station.country_code,
                    "us_state_abbreviation": station.us_state_abbreviation,
                    "us_county_name": station.us_county_name,
                    "weather_forecast_office": station.weather_forecast_office,
                    "ugc_county_code": station.ugc_county_code,
                    "ugc_zone_code": station.ugc_zone_code,
                    "iem_network": station.iem_network,
                    "iem_climate_site": station.iem_climate_site,
                    "matching_rain_on_snow_event_count": rain_on_snow_event_count,
                },
            )
            for station, lon, lat, rain_on_snow_event_count in results
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


class ClimatologyJsonElement(BaseModel):
    month: Annotated[int, Ge(1), Le(12)]
    event_count: int


def climatology_query_results_to_json(
    results: list[Row[tuple[int, int]]],
) -> list[ClimatologyJsonElement]:
    return [
        ClimatologyJsonElement(month=month, event_count=event_count)
        for month, event_count in results
    ]
