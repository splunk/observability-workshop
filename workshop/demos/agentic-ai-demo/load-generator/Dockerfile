FROM python:3.12-slim-bookworm AS base

FROM base AS builder
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*

COPY ./load-generator/requirements.txt .
RUN pip install --prefix="/reqs" -r requirements.txt

FROM base
WORKDIR /usr/src/app/
COPY --from=builder /reqs /usr/local
COPY ./load-generator/locustfile.py .

ENTRYPOINT ["locust", "-f", "locustfile.py"]
CMD ["--headless", \
     "--users", "3", \
     "--spawn-rate", "1", \
     "-H", "http://app:8080", \
     "--loglevel", "INFO"]