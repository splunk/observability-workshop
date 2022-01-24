# Lab: OpenTelemetry & Get Data In

We are going to work in the directory `o11y-bootcamp/bootcamp/service/src`.
Your first task: Write a python app to count words in a text file.

*No, wait - we've already done that for you*.

## Task 1: Service

Checkout the milestone for this task. See the introduction for a brief howto.

=== "Shell Command"

    ```bash
    git reset --hard && git clean -fdx && git checkout 01service
    ```

Let's get python sorted first. On a provided AWS instance, `python3` is already available.

If you are on a Mac:

=== "Shell Command"

    ```bash
    brew install python@3
    ```

On another system, install a recent version of python (i.e. 3.x) with your package manager.

Navigate to `o11y-bootcamp/bootcamp/service/src` and run the provided python service:

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

Then test the service in a separate shell in the `~/o11y-bootcamp/bootcamp/service/src` directory with:

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
    ```

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

Import the modules by editing `app.py`. These imports go towards the top of the file:

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

```bash
export SPLUNK_ACCESS_TOKEN=YOURTOKEN
export SPLUNK_REALM=YOURREALM
```

Start with the [default configuration][otel-config] for the [OpenTelemetry Collector][otel-col]  and name it `collector.yaml` in the `src` directory.

You can also start with a blank configuration, which is what the milestone does for clarity.

Then run OpenTelemetry Collector with this configuration in a docker container:

=== "Shell Command"

    ```bash
    docker run --rm \
        -e SPLUNK_ACCESS_TOKEN=${SPLUNK_ACCESS_TOKEN} \
        -e SPLUNK_REALM=${SPLUNK_REALM} \
        -e SPLUNK_CONFIG=/etc/collector.yaml \
        -p 13133:13133 -p 14250:14250 -p 14268:14268 -p 4317:4317 \
        -p 6060:6060 -p 8888:8888 -p 9080:9080 -p 9411:9411 -p 9943:9943 \
        -v "${PWD}/collector.yaml":/etc/collector.yaml:ro \
        --name otelcol quay.io/signalfx/splunk-otel-collector:0.41.1
    ```

The milestone for this task is `03service-metrics-otel`.

[otel-config]: https://github.com/signalfx/splunk-otel-collector/blob/main/cmd/otelcol/config/collector/agent_config.yaml
[otel-col]: https://github.com/signalfx/splunk-otel-collector
[otel-docker]: https://github.com/signalfx/splunk-otel-collector/blob/main/docs/getting-started/linux-manual.md#docker

## Task 4: Capture Prometheus metrics

Add a [prometheus receiver][prom-recv] to the OpenTelemetry Collector configuration so that it captures the metrics introduced in Task 2 from the application.

Hint: The hostname `host.docker.internal` allows you to access the host from within a docker container. Add

    ```
    --add-host=host.docker.internal:host-gateway
    ```

to the


Validate that you are getting data for the custom metric `characters_recv_total` introduced in Task 2.

The milestone for this task is `04service-metrics-prom`.

[prom-recv]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/simpleprometheusreceiver

## Task 5: Dockerize the Service

Dockerize the service. Use this `Dockerfile` as a skeleton:

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

Stop other instances of the app if you had any running.

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

Stop any other running containers from this app or the OpenTelemetry Collector.

Add a [`docker-compose.yaml`][docker-compose] file for the python app to prepare us for running multiple containers.

A skeleton to run the service on port 8000 might look like this. What port do you need to map 8000 to for the service to work?

```docker
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

Rebuild the docker-compose stack and run it.

The milestone for this task is `07docker-compose-otel`.

[otel-compose]: https://github.com/signalfx/splunk-otel-collector/tree/main/examples/docker-compose

## Task 8: Monitor containerized service

The development team has started using other containerized services with docker compose. Switch to the provided milestone `08docker-compose-redis` with the instructions from "Getting Started".

Add the [redis monitor][redis-mon] to the OpenTelemetry Collector configuration in `collector.yaml` to get metrics from the [redis cache].

Rebuild the docker-compose stack and run it.

Check that you are getting data in the Redis dashboard:

![Redis dashboard](../images/redis-dashboard.png)

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

