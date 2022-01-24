: Lab: OpenTelemetry & Get Data In

We are going to work in the directory `bootcamp/service/src`.
Your first task: Write a python app to count words in a text file.

*No, wait - we've already done that for you*.

This section will introduce the format for this workshop.

1. First, we will introduce a challenge or task for you to complete, e.g. "Task 1: Service".

1. There will be concepts and references for you to review.

1. We will timebox self-paced content during a live workshop.

1. We use `git` branches to provide important milestones after a task is complete. If you did not complete a specific task, you can use these milestones to proceed to the next task or review the solution.

## Getting started

The task is to write a python app to count words in a text file.
Here is how to get to the milestone that completes this step:

=== "Shell Command"

    ```bash
    git checkout 01service
    ```

This will put you on the first milestone.

In case you have already worked on a milestone, you might see an error like:

=== "Example Output"

    ```bash
    error: Your local changes to the following files would be overwritten by checkout:
        app.py
    Please commit your changes or stash them before you switch branches.
    Aborting
    ```

This is because your work conflicts with changes on the milestone. You have the following options:

1. If you have worked on a task and want to progress to the next one *and DROP all your changes*:

    === "Shell Command"

        ```bash
        git reset --hard && git clean -fdx && git checkout service
        ```

    You will have to re-apply any local changes like settings tokens or names.


1. To preserve your work but move it out of the way, you can use

    === "Shell Command"

        ```bash
        git stash && git checkout service
        ```

    To restore your work, switch to the previous milestone (`main` in this case) and retrieve the stashed changes:

    === "Shell Command"

        ```bash
        git checkout main && git stash pop
        ```

    Sometimes you run into conflicting changes with this approach. We recommend you use the first option in this case.

1. During development changes are recorded by adding and commiting to the repository. This is not necessary for this workshop.

Use the first option and proceed.

To compare two milestones, use

=== "Shell Command"

    ```bash
    git diff main..01service
    ```

To compare what you have with a milestone, , e.g. the milestone `service` use

=== "Shell Command"

    ```bash
    git diff ..01service
    ```

=== "Example Output (excerpt)"

    ```bash
    ...
    diff --git a/bootcamp/service/src/app.py b/bootcamp/service/src/app.py
    index 9bcae83..b7fc141 100644
    --- a/bootcamp/service/src/app.py
    +++ b/bootcamp/service/src/app.py
    @@ -1,10 +1,12 @@
    +import json
     import re
    -from unicodedata import category
    +from flask import Flask, request, Response
    ...
    ```

## Task 1: Service

If you have not done so already, checkout the milestone for this task:

=== "Shell Command"

    ```bash
    git reset --hard && git clean -fdx && git checkout 01service
    ```

Let's get python sorted quickly. On a provided AWS instance, `python3` is available.

If you are on a Mac:

```bash
brew install python@3
```

On another system, install a recent version of python (i.e. 3.x) with your package manager.

Run the provided python service:

=== "Shell Command"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python3 app.py
    ```

=== "Example Output"

    ```bash
     * Serving Flask app 'app' (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on all addresses.
       WARNING: This is a development server. Do not use it in a production deployment.
     * Running on http://10.42.1.202:5000/ (Press CTRL+C to quit)
    ```

Then test the service (in a separate shell) with:

=== "Shell Command"

    ```bash
    curl -X POST http://127.0.0.1:5000/wordcount -F text=@hamlet.txt
    ```

=== "Example Output"

    ```bash
    [["in", 436], ["hamlet", 484], ["my", 514], ["a", 546], ["i", 546], ["you", 550], ["of", 671], ["to", 763], ["and", 969], ["the", 1143]]%
    ```

The bootcamp contains other text files at `~/nlp/resources/corpora`. To use a random example:

=== "Shell Command"

    ```bash
    SAMPLE=$(find ~/nlp/resources/corpora/gutenberg -name '*.txt' | shuf -n1)
    curl -X POST http://127.0.0.1:5000/wordcount -F text=@$SAMPLE
    ```

To generate load:

=== "Shell Command"

    ```bash
    FILES=$(find ~/nlp/resources/corpora/gutenberg -name '*.txt')
    while true; do
        SAMPLE=$(shuf -n1 <<< "$FILES")
        curl -X POST http://127.0.0.1:5000/wordcount -F text=@${SAMPLE}
        sleep 1
    done

## Task 2: Prometheus Metrics

We need visibility into performance - let us add metrics with [Prometheus][prometheus].

Install the [Python Prometheus client][py-prom] as a dependency:

=== "Shell Command"

    ```bash
    echo "prometheus-client" >> requirements.txt
    python3 -m venv .venv
    source .venv/bin/activate
    .venv/bin/pip install -r requirements.txt
    ```

Import the modules in `app.py`:

```python
import prometheus_client
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from prometheus_client import Counter
```

Define a metrics endpoint before `@app.route('/wordcount', methods=['POST'])`:

```python
@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)
```

And use this python snippet after `app = Flask(__name__)` to define a new counter metric:

```python
c_recv = Counter('characters_recv', 'Number of characters received')
```

Increase the counter metric after `data = request.files['text'].read().decode('utf-8')`:

```python
c_recv.inc(len(data))
```

Test that the application exposes metrics by hitting the endpoint while the app is running:

=== "Shell Command"

    ```bash
     curl http://127.0.0.1:5000/metrics
    ```

The milestone for this task is `02service-metrics`.

[prometheus]: https://prometheus.io/docs/introduction/overview/#architecture
[py-prom]: https://pypi.org/project/prometheus-client/

## Task 3: OpenTelemetry Collector

You will need an access token for Splunk Observability Cloud. Set them up as environment variables:

```
export SPLUNK_ACCESS_TOKEN=YOURTOKEN
export SPLUNK_REAM=YOURREALM
```

Create a file called `collector.yaml` in the src directory and add the [configuration][otel-config] for the [OpenTelemetry Collector][otel-col] in this file. Then [run it in a docker container][otel-docker]:

=== "Shell Command"

    ```bash
    docker run --rm \
        -e SPLUNK_ACCESS_TOKEN=${SPLUNK_ACCESS_TOKEN} \
        -e SPLUNK_REALM=${SPLUNK_REALM} \
        -e SPLUNK_CONFIG=/etc/collector.yaml \
        -p 13133:13133 -p 14250:14250 -p 14268:14268 -p 4317:4317 \
        -p 6060:6060 -p 8888:8888 -p 9080:9080 -p 9411:9411 -p 9943:9943 \
        -v "${PWD}/collector.yaml":/etc/collector.yaml:ro \
        --name otelcol quay.io/signalfx/splunk-otel-collector:v0.41.1
    ```

The milestone for this task is `03service-metrics-otel`.

[otel-config]: https://github.com/signalfx/splunk-otel-collector/blob/main/cmd/otelcol/config/collector/agent_config.yaml
[otel-col]: https://github.com/signalfx/splunk-otel-collector
[otel-docker]: https://github.com/signalfx/splunk-otel-collector/blob/main/docs/getting-started/linux-manual.md#docker

## Task 4: Capture Prometheus metrics

Add a [prometheus receiver][prom-recv] to the the otel config so that it captures the metrics introduced in Task 2 from the application.

Hint: The hostname `host.docker.internal` allows you to access the host from within a docker container.

The milestone for this task is `04service-metrics-prom`.

[prom-recv]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/simpleprometheusreceiver

## Task 5: Dockerize the Service

Dockerize the service. Use this Dockerfile as a skeleton:

```docker
ARG APP_IMAGE=python:3
FROM $APP_IMAGE as base

FROM base as builder
WORKDIR /app
RUN python -m venv .venv && .venv/bin/pip install --no-cache-dir -U pip setuptools
COPY requirements.txt .
RUN .venv/bin/pip install -r requirements.txt --no-cache-dir -r requirements.txt

FROM base
WORKDIR /app
COPY --from=builder /app /app
COPY app.py .

ENV PATH="/app/.venv/bin:$PATH"
```

Add the [appropriate `CMD`][docker-cmd] at the end to launch the app.

Then build and run the image:

=== "Shell Command"

    ```bash
    docker build . -t wordcount
    docker run -p 5000:5000 wordcount:latest
    ```

Test the service in another shell:

=== "Shell Command"

    ```bash
    curl -X POST http://127.0.0.1:5000/wordcount -F text=@hamlet.txt
    ```

The milestone for this task is `05docker`.

[docker-cmd]: https://docs.docker.com/engine/reference/builder/#cmd

## Task 6: Docker Compose

The development team wants to use a containerized [redis][redis] cache to improve performance of the service.

Add a [docker-compose][docker-compose] setup for the python app to prepare us for running multiple containers.

A skeleton to run the service on port 8000 might look like this. What port do you need to map 8000 to for the service to work?

```
version: '3'

services:
  yourservicename:
    build: .
    expose:
      - "8000"
    ports:
      - "8000:XXXX"
```

Build the service:

```bash
docker-compose build
```

Then run the whole stack:

```bash
docker-compose up
```

Test the service with curl by hitting the exposed port.

The milestone for this task is `06docker-compose`.

[redis]: https://redis.io/
[docker-compose]: https://docs.docker.com/compose/

## Task 7: Container orchestration

Add the [OpenTelemetry Collector service definition][otel-compose] to the docker-compose setup.


The milestone for this task is `07docker-compose-otel`.

[otel-compose]: https://github.com/signalfx/splunk-otel-collector/tree/main/examples/docker-compose

## Task 8: Monitor containerized service

The development team has started using other containerized services with docker compose. Switch to the provided milestone `08docker-compose-redis` with the instructions from "Getting Started".

Add configuration to the OpenTelemetry Collector to monitor the redis cache.

The milestone for this task is `08docker-compose-redis-otel`.

[redis]: https://redis.io/
[redis-mon]: https://docs.splunk.com/Observability/gdi/redis/redis.html

## Task 9: Kubernetes

The development team has started using [Kubernetes][kubernetes] for container orchestration. Switch to the provided milestone `09k8s` with the instructions from "Getting Started".

Rebuild the container images for the private registry:

```bash
docker-compose build
```

Push the images to the private registry:

```bash
docker-compose push
```

Then deploy the services into the cluster:

```bash
kubectl apply -f k8s
```

Test the service with

```bash
ENDPOINT=$(kubectl get service/wordcount -o jsonpath='{.spec.clusterIP}')
curl http://$ENDPOINT:8000/wordcount -F text=@hamlet.txt
```

Configure and install an OpenTelemetry Collector using [Splunk's helm chart][splunk-otel-helm]:

1. Review the [configuration how-to][otel-docs] and the [advanced configuration][otel-adv-cfg] to create a `values.yaml` that adds the required receivers for redis and prometheus.

1. Use the environment variables for realm,token and cluster name and pass them to `helm` as arguments.

The milestone for this task is `09k8s-otel`.

[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[splunk-otel-helm]: https://github.com/signalfx/splunk-otel-collector-chart
[otel-docs]: https://github.com/signalfx/splunk-otel-collector-chart#how-to-install
[otel-adv-cfg]: https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/advanced-configuration.md

# Lab: Application Performance Monitoring

1. Understand GDI path for APM for common tech stacks (Docker, K8s).
1. Be able to instrument an app from scratch (traces, custom metadata).
1. Understand how distributed tracing works across tech stacks (header propagation, …)
1. Understand positioning vs. trad. APM vendors

## Task 10: Microservices Auto-instrumentation

The development team has broken up the monolithic service into microservices baesd on the `docker-compose` setup. Switch to the provided milestone `10microservices` with the instructions from "Getting Started".

Test the service with

```bash
curl -X POST http://127.0.0.1:8000/api -F text=@hamlet.txt
```

Add auto-instrumentation to the `public_api` microservice using the [Splunk distribution of OpenTelemetry Python][splunk-otel-python]. Review the [documentation][splunk-py-instrument] and the [Getting Started] steps and apply it to `Dockerfile`.

Take into account the [trace exporter][otel-py-exporter] settings and add the required environment variables to the `.env` file for `docker-compose`. Use the configuration to send traces directly to Splunk  Observability Cloud.

The milestone for this task is `10microservices-autoi`. It has auto-instrumentation applied for *all* microservices.

[splunk-otel-python]: https://github.com/signalfx/splunk-otel-python
[getting-started]: https://github.com/signalfx/splunk-otel-python
[otel-py-exporter]: https://github.com/signalfx/splunk-otel-python/blob/main/docs/advanced-config.md#trace-exporters
[splunk-py-instrument]: https://docs.splunk.com/Observability/gdi/get-data-in/application/python/get-started.html#nav-Instrument-a-Python-application

## Task 11: Infrastructure Correlation

There is not task 11 (yet).

## Task 12: Instrumentation in Kubernetes

The development team has started using Kubernetes for container orchestration. Switch to the provided milestone `12microservices-k8s` with the instructions from "Getting Started".

The Kubernetes manifests are located in the `k8s` folder. Add auto-instrumentation to the `public_api` microservice `deployment` by configuring the [Splunk distribution of OpenTelemetry Python][splunk-otel-python]. The `Dockerfile` has already been prepared.

Install the OpenTelemetry Collector to the environment using [Splunk's helm chart][splunk-otel-helm] and use the provided `values.yaml`:

```bash
helm install my-splunk-otel-collector --set="splunkObservability.realm=${SPLUNK_REALM},splunkObservability.accessToken=${SPLUNK_ACCESS_TOKEN},clusterName=${CLUSTER_NAME}" splunk-otel-collector-chart/splunk-otel-collector -f values.yaml
```

Rebuild the container images for the private registry:

```bash
docker-compose build
```

Push the images to the private registry:

```bash
docker-compose push
```

Deploy to the cluster with

```bash
kubectl apply -f k8s
```

Test the service with

```bash
ENDPOINT=$(kubectl get service/public-api -o jsonpath='{.spec.clusterIP}')
curl http://$ENDPOINT:8000/api -F text=@hamlet.txt
```

The milestone for this task is `12microservices-k8s-autoi`. It has auto-instrumentation applied for *all* microservices.

## Task 13: Using OpenTelemetry instrumentation


## Future Tasks

TODO YOUR Idea here? Let us know!

TODO metrics method being traced - how to disable?

```
from opentelemetry.context import attach, detach, set_value
token = attach(set_value("suppress_instrumentation", True))
```

TODO autodetect metrics with k8s labels: `prometheus.io/scrape: true` - run prometheus on separate port `9090`.

TODO [tracing examples][py-trace-ex]

[py-trace-ex]: https://github.com/open-telemetry/opentelemetry-python/blob/main/docs/examples/
