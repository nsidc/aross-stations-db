import datetime as dt

# TODO: Can we use SQLModel to unify API and DB models?
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Station(Base):
    __tablename__ = "station"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    location: Mapped[WKBElement] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        index=True,
    )

    elevation_meters: Mapped[float]
    record_begins: Mapped[dt.datetime]

    timezone_name: Mapped[str]
    country_code: Mapped[str]
    us_state_abbreviation: Mapped[str | None]
    us_county_name: Mapped[str | None]

    weather_forecast_office: Mapped[str | None]

    # UGC = Universal Geographic Code
    # (https://www.weather.gov/media/directives/010_pdfs_archived/pd01017002b.pdf)
    ugc_county_code: Mapped[str | None]
    ugc_zone_code: Mapped[str | None]

    # IEM = Iowa Environmental Mesonet. See:
    #   https://mesonet.agron.iastate.edu/ASOS/
    #   https://mesonet.agron.iastate.edu/sites/locate.php?network=AKCLIMATE
    iem_network: Mapped[str]
    iem_climate_site: Mapped[str | None]

    events = relationship("Event", backref="station")

    # TODO: More fields:
    #  ncdc81,ncei91,network,start_year,end_year


class Event(Base):
    __tablename__ = "event"

    station_id: Mapped[str] = mapped_column(ForeignKey("station.id"), primary_key=True)
    time_start: Mapped[dt.datetime] = mapped_column(primary_key=True)
    time_end: Mapped[dt.datetime] = mapped_column(primary_key=True)

    # Was there snow on the ground during this event? Only available after 2004 for some
    # stations, never available for other stations.
    snow_on_ground: Mapped[bool | None] = mapped_column(index=True)

    # During how many hours of this event was rain (or other event type) detected? These
    # precipitation types are detected by a horizontal beam that the precipitation falls
    # through.
    rain_hours: Mapped[int] = mapped_column(index=True)
    freezing_rain_hours: Mapped[int] = mapped_column(index=True)
    # Solid precipitation = snow, ice, graupel, hail, etc.
    solid_precipitation_hours: Mapped[int] = mapped_column(index=True)
    unknown_precipitation_hours: Mapped[int] = mapped_column(index=True)

    # TODO: More fields: duration,t2m_mean,t2m_min,t2m_max
    #       I don't think we need to keep duration.
