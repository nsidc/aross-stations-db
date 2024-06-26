# aross-stations-db

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

Reads Automated Surface Observation Station (ASOS) data from disk on the NSIDC archive
to create a temporally and geospatially indexed database to quickly search events.

> [!NOTE]
> TODO: Is this data available publicly and documented? How is it produced? Links!


## Usage

To get started quickly, [install Docker](https://docs.docker.com/engine/install/).

> [!IMPORTANT]
> Instructions that follow presume the current working directory is the root of this
> repository unless otherwise stated.

<details><summary>Dev quickstart</summary>

> :bangbang: Don't worry about this unless you intend to change the code!

**View
[the contributing docs](https://aross-stations-db.readthedocs.io/en/latest/contributing.html)
for more details!**

Set up the development compose configuration to be automatically loaded:

```bash
ln -s compose.dev.yml compose.override.dev.yml
```

### Debugging

You may wish to run the API process from an attached shell. You can set up the relevant
container to "sleep" in `compose.dev.yml`:

```yaml
  api:
    <<: *dev-common
    entrypoint: "sleep"
    command: ["9999999"]
    # command: ["dev", "--host", "0.0.0.0", "./src/aross_stations_db/api"]
```

Then `docker exec -it api sh` to connect to the container, and manually run the dev server:

```
fastapi dev --host 0.0.0.0 ./src/aross_stations_db/api`.
```

From here, you can interactively pause at any `breakpoint()` calls in the Python code.

</details>


### Set envvars

Create a `.env` file or otherwise `export` the required envvars. If you use an `.env`
file, it should look like this (feel free to change the password :smile:):

```bash
POSTGRES_PASSWORD="supersecret"
AROSS_DB_CONNSTR="postgresql+psycopg://aross:${POSTGRES_PASSWORD}@db:5432/aross"
AROSS_DATA_BASEDIR="/path/to/aross-data-dir"
```

> [!IMPORTANT]
> `$AROSS_DATA_BASEDIR` should be Andy's data directory containing expected "metadata"
> and "events" subdirectories. TODO: Document how that data is created! _How can the
> public access it?_

> [!NOTE]
> The connection string shown here is for connecting within the Docker network to a
> container with the hostname `db`.


### Start the application stack

The stack is configured within `compose.yml` and includes containers:

* `aross-stations-db`: A [PostGIS](https://postgis.net/) database for quickly storing
  and accessing event records.
* `aross-stations-admin`: An [Adminer](https://www.adminer.org/) container for
  inspecting the database in the browser.
* `aross-stations-api`: An HTTP API for accessing data in the database.

```bash
docker compose up --detach
```


### Inspect the database

You can use the included Adminer container for quick inspection. Navigate in your
browser to `http://localhost:80` and enter:

| Field    | Value |
| -------- | ----- |
| System   | PostgreSQL |
| Server   | `aross-stations-db` |
| Username | `aross` |
| Password | Whatever you specified in the environment variable |
| Database | `aross` |

> [!NOTE]
> At this point, the database is empty. We're just verifying we can connect. Continue to
> ingest next!


### Run ingest

```bash
docker compose run ingest init  # Create empty tables (deleting any pre-existing ones)
docker compose run ingest load  # Load the tables from event files
```

From a fast disk, this should take under 2 minutes.


### :sparkles: Check out the data!

Now, you can use Adminer's SQL Query menu to select some data:

<details>
<summary>Example SQL query</summary>

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
  AND event.time_start > '2023-01-01'::date
  AND event.time_end < '2023-06-01'::date
;
```
</details>

Or you can check out the API docs in your browser at `http://localhost:8000/docs` or
submit an HTTP query:

<details>
<summary>Example HTTP query</summary>

```
http://localhost:8000/v1/?start=2023-01-01&end=2023-06-01&polygon=POLYGON%20((-159.32130625160698%2069.56469019745796,%20-159.32130625160698%2068.08208920517862,%20-150.17196253090276%2068.08208920517862,%20-150.17196253090276%2069.56469019745796,%20-159.32130625160698%2069.56469019745796))
```
</details>


### View logs

In this example, we view and follow logs for the `api` service:

```bash
docker compose logs --follow api
```

You can replace `api` with any other service name, or omit it to view logs for all
services.


## View UI

For now, it's just a Jupyterlab instance with a demo notebook. In your browser, navigate
to `http://localhost:8888`. The password is the same as the database password you set earlier.

This UI will likely be replaced with something more robust. Who knows ;)


### Shutdown

```bash
docker compose down
```


#### Cleanup

##### Database

Remove the `_db/` directory to start over with a fresh database.


##### Containers and images

```bash
# Bring down containers, even if a service name has changed
docker compose down --remove-orphans
# Clean up all unused images aggressively
docker system prune -af
```


## Troubleshooting

### `Permission denied` errors from FastAPI

When this error occurs, the webserver still responds to queries, but hot-reloading
doesn't work.

You may need to grant read access to the `_data/` directory if you're running locally.
The problem is that FastAPI's hot-reloading functionality in dev needs to watch the
current directory for changes, and I don't know of a way to ignore this directory that
is usually not readable. The directory is likely owned by root, assuming it was created
automatically by Docker, so you may need to use `sudo`.

```bash
sudo chmod -R ugo+r _data
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
