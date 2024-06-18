# aross-stations-db

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]


## Install

For now, you can install from this repository. TODO: PyPI if we decide this package
should continue to exist and not be moved or renamed :)

```bash
pip install git+https://github.com/nsidc/aross-stations-db.git
```


### Dev install

With this method, you can change the source code and the changes will be reflected
without needing to re-install.

```bash
pip install --editable .
```


## Usage

Everything presumes the current working directory is the root of this repo unless
otherwise stated.


### Set envvars

Create a `.env` file or otherwise set the envvars. Your `.env` file might look like this
if you're running a local database:

```bash
POSTGRES_PASSWORD="supersecret"
AROSS_DB_CONNSTR="postgresql+psycopg://aross:${POSTGRES_PASSWORD}@localhost:5432/aross"
# NOTE: This dir should contain "metadata" and "events" subdirectories:
AROSS_DATA_BASEDIR="/path/to/aross-data-dir"
```


### Start a fresh database

This repo provides a quickstart database in Docker, defined in `compose.yml`. Once
started, you (and our code!) can connect on port `5432`.

```bash
docker compose up --detach
```

At this point you can manually connect to your database with:

```bash
psql -h localhost -U aross
```


### Run ingest

```bash
aross-stations-db init  # Create empty tables (deleting any pre-existing ones)
aross-stations-db load  # Load the tables from event files
```


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/nsidc/aross-stations-db/workflows/CI/badge.svg
[actions-link]:             https://github.com/nsidc/aross-stations-db/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/aross-stations-db
[conda-link]:               https://github.com/conda-forge/aross-stations-db-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/nsidc/aross-stations-db/discussions
[pypi-link]:                https://pypi.org/project/aross-stations-db/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/aross-stations-db
[pypi-version]:             https://img.shields.io/pypi/v/aross-stations-db
[rtd-badge]:                https://readthedocs.org/projects/aross-stations-db/badge/?version=latest
[rtd-link]:                 https://aross-stations-db.readthedocs.io/en/latest/?badge=latest
<!-- prettier-ignore-end -->
