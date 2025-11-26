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

# Per https://opentelemetry.io/docs/zero-code/python/troubleshooting/#pre-fork-server-issues
# if we use uvicorn with more than 1 worker and opentelemetry-instrument, we'll lose metrics
# The workaround is to use gunicorn + uvicorn workers, but then evals don't work
#ENTRYPOINT [ "/venv/bin/opentelemetry-instrument", "/venv/bin/gunicorn", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "300", "--bind", "0.0.0.0:8080", "app:app" ]
ENTRYPOINT [ "/venv/bin/opentelemetry-instrument", "/venv/bin/uvicorn", "app:app", "--workers", "1", "--host", "0.0.0.0", "--port", "8080" ]
