# aross-stations-db

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]


## Install

TODO


### Dev install

```bash
pip install --editable .
```


## Usage

### Set envvars

```bash
export AROSS_DB_CONNSTR="postgresql://hostname/dbname?user=username&password=supersecret"
# NOTE: This dir should contain "metadata" and "events" subdirectories:
export AROSS_DATA_DIR="/path/to/aross-data-dir"
```


### Run

```bash
python -m aross_stations_db
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
