from __future__ import annotations

import importlib.metadata

import aross_stations_db as m


def test_version():
    assert importlib.metadata.version("aross_stations_db") == m.__version__
