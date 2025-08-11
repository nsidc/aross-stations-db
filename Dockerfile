FROM python:3.12-alpine

# git: for vcs-awareness during install
# build-base, etc.: for building jupyterlab deps
RUN apk add git build-base musl-dev linux-headers gdal-dev

WORKDIR /app
ADD . .

RUN pip install --editable ".[ui]"

ENTRYPOINT ["aross-stations-db"]
