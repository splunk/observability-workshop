FROM docker.io/library/python:3.12-alpine3.22 AS build-venv

RUN apk update && \
    apk add gcc g++ linux-headers

# install git, which is referenced by requirements.txt
RUN apk update && \
    apk add --no-cache git

COPY ./app/requirements.txt requirements.txt

RUN python -m venv venv && \
    venv/bin/pip install --no-cache-dir -r requirements.txt

RUN venv/bin/opentelemetry-bootstrap -a install

FROM docker.io/library/python:3.12-alpine3.22

COPY --from=build-venv /venv/ /venv/

WORKDIR /app

COPY ./app/. /app

EXPOSE 8080
ENTRYPOINT [ "/venv/bin/uvicorn", "app:app", "--workers", "2", "--reload", "--host", "0.0.0.0", "--port", "8080" ]
