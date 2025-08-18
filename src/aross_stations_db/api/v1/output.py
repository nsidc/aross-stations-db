import datetime as dt
import io
from typing import Annotated

from annotated_types import Ge, Le
from geojson_pydantic import (
    Feature,
    FeatureCollection,
    Point,
)
from geojson_pydantic.types import Position2D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pydantic import BaseModel
from sqlalchemy import Row
from sqlalchemy.orm.query import RowReturningQuery

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


def timeseries_query_results_to_bar_plot_buffer(
    query: RowReturningQuery[tuple[dt.datetime, int]],
    start: dt.date,
    end: dt.date,
    format: str = 'png'
) -> io.BytesIO:
    data = pd.read_sql(query.statement, query.session.connection())
    data.set_index('month', inplace=True)

    start_str = start.strftime("%Y-%m")
    end_str = end.strftime("%Y-%m")

    title_parts = [
        f"Monthly Rain-on-Snow Events",
        f"[{start_str} - {end_str}]"
    ]
    title = "\n".join(title_parts)

    if len(data) == 0:
        data.loc[start_str] = 0
        data.loc[end_str] = 0

    
    data.index = pd.to_datetime(data.index)
    data.index = data.index.strftime("%Y-%m")
    data = add_missing_plot_months(data)

    plot = data.plot(
        kind="bar",
        title=title,
        ylabel="Event Count",
        xlabel="Month",
        rot=45,
        legend=False,
    )

    ticks = plot.get_xticklines()
    labels = plot.get_xticklabels()

    # Evenly space out the tick labels to avoid overcrowding
    indexes = np.linspace(0, len(labels)-1, num=12, dtype=int)
    for i, l in enumerate(labels):
        if i not in indexes:
            l.set_visible(False)
        else:
            l.set_horizontalalignment('right')
            l.set_rotation_mode('anchor')
            ticks[i*2].set_markersize(6)
    
    plt.tight_layout()

    # Create the buffer and return it so it can be sent to the requester
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)

    return buffer


# If there are any months missing in the dataframe, add a "count 0" entry for them
def add_missing_plot_months(df: pd.DataFrame) -> pd.DataFrame:
    start = df.index[0]
    end = df.index[-1]

    syear, smonth = map(int, start.split('-'))
    eyear, emonth = map(int, end.split('-'))

    while [syear, smonth] != [eyear, emonth]:
        smonth += 1
        if smonth > 12:
            smonth = 1
            syear += 1
        key = f"{syear:04}-{smonth:02}"
        if key not in df.index:
            df.loc[key] = [0]
        
    return df.sort_index()


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
