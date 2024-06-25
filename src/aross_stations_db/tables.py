import datetime as dt

# TODO: Can we use SQLModel to unify API and DB models?
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
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

    events = relationship("Event", backref="station")


class Event(Base):
    __tablename__ = "event"

    station_id: Mapped[str] = mapped_column(ForeignKey("station.id"), primary_key=True)
    time_start: Mapped[dt.datetime] = mapped_column(primary_key=True)
    time_end: Mapped[dt.datetime] = mapped_column(primary_key=True)

    # TODO: More fields: duration,RA,UP,FZRA,SOLID,t2m_mean,t2m_min,t2m_max,sog
    #       Don't think we need to keep duration.
