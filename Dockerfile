FROM python:3.12-alpine

RUN apk add git

WORKDIR /app
ADD . .

RUN pip install --editable ".[dev,test,docs]"

ENTRYPOINT ["aross-stations-db"]
