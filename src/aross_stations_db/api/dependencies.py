from collections.abc import Iterator
from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from aross_stations_db.config import Settings


@cache
def get_config() -> Settings:
    # TODO: False-positive. Remove type-ignore.
    #       See: https://github.com/pydantic/pydantic/issues/6713
    return Settings()  # type:ignore[call-arg]


def get_db_session(
    config: Annotated[Settings, Depends(get_config)],
) -> Iterator[Session]:
    SessionFactory = sessionmaker(config.db_engine)
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
