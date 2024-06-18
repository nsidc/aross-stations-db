import datetime as dt

# TODO: Can we use SQLModel to unify API and DB models?
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Station(Base):
    __tablename__ = "station"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    country_code: Mapped[str]

    location: Mapped[WKBElement] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        index=True,
    )


class Event(Base):
    __tablename__ = "event"

    # TODO: Is this a good PK or should it be station_id + start?
    id: Mapped[int] = mapped_column(primary_key=True)

    station_id: Mapped[str] = mapped_column(ForeignKey("station.id"), index=True)
    start_timestamp: Mapped[dt.datetime] = mapped_column(index=True)
    end_timestamp: Mapped[dt.datetime] = mapped_column(index=True)

    # TODO: More fields: duration,RA,UP,FZRA,SOLID,t2m_mean,t2m_min,t2m_max,sog
    #       Don't think we need to keep duration.
