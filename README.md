# aross-stations-db

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

Reads ASOS station data from disk on the NSIDC archive to create a temporally and
geospatially indexed database to quickly search events.

> [!NOTE]
> TODO: Is this data available publicly and documented? How is it produced? Links!


## Install

For now, you can install from this repository.

> [!NOTE]
> TODO: Publish to PyPI if we decide this package should continue to exist and not be
> moved or renamed :)

```bash
pip install git+https://github.com/nsidc/aross-stations-db.git
```


### Dev install

With this method, you can change the source code and the changes will be reflected
without needing to re-install.

```bash
pip install --editable ".[dev]"
```


#### Checks

If installed correctly, you can now lint & format the code, which is run through
`pre-commit` because these tasks don't require installing the package:

```bash
pre-commit run --all-files
```

You can also type-check and test the code, which are run through `nox` because this
_does_ require installing the package:

```bash
nox
```

> [!TIP]
> To reuse an already-created Nox env, add `-R`.


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

From a fast disk, this should take under 2 minutes.


### Inspect the database

In addition to manually querying the database with `psql`, you can use the included
adminer container for quick inspection. Navigate in your browser to
`http://localhost:80` and enter:

* System: PostgreSQL
* Server: `aross-stations-db`
* Username: `aross`
* Password: Whatever you specified in the environment variable
* Database: `aross`


#### Example query

```sql
select event.*
from event
join station on event.station_id = station.id
where
  ST_Within(
    station.location,
    ST_SetSRID(
      ST_GeomFromText('POLYGON ((-159.32130625160698 69.56469019745796, -159.32130625160698 68.08208920517862, -150.17196253090276 68.08208920517862, -150.17196253090276 69.56469019745796, -159.32130625160698 69.56469019745796))'),
      4326
    )
  )
  AND event.start_timestamp > '2023-01-01'::date
  AND event.end_timestamp < '2023-06-01'::date
;
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
