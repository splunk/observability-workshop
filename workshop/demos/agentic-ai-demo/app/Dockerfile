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

# uninstall opentelemetry-instrumentation-openai-v2 as it causes issues with our application
RUN venv/bin/pip uninstall -y opentelemetry-instrumentation-openai-v2 opentelemetry.instrumentation.httpx

FROM docker.io/library/python:3.12-alpine3.22

COPY --from=build-venv /venv/ /venv/

WORKDIR /app

COPY ./app/. /app

EXPOSE 8080
ENTRYPOINT [ "/venv/bin/opentelemetry-instrument", "/venv/bin/gunicorn", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "180", "--bind", "0.0.0.0:8080", "app:app" ]
