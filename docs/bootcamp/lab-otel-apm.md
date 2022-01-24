# Lab: Application Performance Monitoring

## Goals

1. Understand GDI path for APM for common tech stacks (Docker, K8s).
1. Be able to instrument an app from scratch (traces, custom metadata).
1. Understand how distributed tracing works across tech stacks (header propagation, …)

## Task 10: Microservices Auto-instrumentation

The development team has broken up the monolithic service into microservices baesd on the `docker-compose` setup. Switch to the provided milestone `10microservices` with the instructions from "Getting Started".

Test the service with:

=== "Shell Command"

    ```bash
    curl -X POST http://127.0.0.1:8000/api -F text=@hamlet.txt
    ```

Add auto-instrumentation to the `public_api` microservice using the [Splunk distribution of OpenTelemetry Python][splunk-otel-python]. Review the [documentation][splunk-py-instrument] and the [getting Started][splunk-py-instrument] steps and apply it to `Dockerfile`.

Take into account the [trace exporter][otel-py-exporter] settings and add the required environment variables to the `.env` file for `docker-compose`. Use the configuration to send traces directly to Splunk  Observability Cloud.

The milestone for this task is `10microservices-autoi`. It has auto-instrumentation applied for *all* microservices.

[splunk-otel-python]: https://github.com/signalfx/splunk-otel-python
[getting-started]: https://github.com/signalfx/splunk-otel-python
[otel-py-exporter]: https://github.com/signalfx/splunk-otel-python/blob/main/docs/advanced-config.md#trace-exporters
[splunk-py-instrument]: https://docs.splunk.com/Observability/gdi/get-data-in/application/python/get-started.html#nav-Instrument-a-Python-application

## Task 11: Infrastructure Correlation

There is no task 11 (yet).

## Task 12: Instrumentation in Kubernetes

TODO Note on .env being overwritten

TODO change name of environment from YOURENV to something else.

The development team has started using Kubernetes for container orchestration. Switch to the provided milestone `12microservices-k8s` with the instructions from "Getting Started".

The Kubernetes manifests are located in the `k8s` folder. Add auto-instrumentation to the `public_api` microservice `deployment` by configuring the [Splunk distribution of OpenTelemetry Python][splunk-otel-python]. The `Dockerfile` has already been prepared.

Install the OpenTelemetry Collector to the environment using [Splunk's helm chart][splunk-otel-helm] and use the provided `values.yaml`:

=== "Shell Command"

    ```bash
    helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

    helm install my-splunk-otel-collector --set="splunkObservability.realm=${SPLUNK_REALM},splunkObservability.accessToken=${SPLUNK_ACCESS_TOKEN},clusterName=${CLUSTER_NAME}" splunk-otel-collector-chart/splunk-otel-collector -f values.yaml
    ```

Rebuild the container images for the private registry:

=== "Shell Command"

    ```bash
    docker-compose build
    ```

Push the images to the private registry:

=== "Shell Command"

    ```bash
    docker-compose push
    ```

Deploy to the cluster with

=== "Shell Command"

    ```bash
    kubectl apply -f k8s
    ```

Test the service with

=== "Shell Command"

    ```bash
    ENDPOINT=$(kubectl get service/public-api -o jsonpath='{.spec.clusterIP}')
    curl http://$ENDPOINT:8000/api -F text=@hamlet.txt
    ```

The milestone for this task is `12microservices-k8s-autoi`. It has auto-instrumentation applied for *all* microservices.

[splunk-otel-helm]: https://github.com/signalfx/splunk-otel-collector-chart

## Task 13: Using OpenTelemetry instrumentation

The business team want to add the service version, the customer profile that is defined by a color and the name of the analyzed file. Apply it to public-api.

Switch to the provided milestone `12microservices-k8s-autoi` with the instructions from "Getting Started".

The Kubernetes manifests are located in the `k8s` folder. Add the service version by configuring the OTEL ressources attribute [Splunk distribution of OpenTelemetry Python - Advanced Configuration](https://github.com/signalfx/splunk-otel-python/blob/main/docs/advanced-config.md#trace-configuration)

The customer profile and the file name can be variable for each execution. Create attributes and assign them to your current span thanks to [OTEL python](https://opentelemetry-python.readthedocs.io/en/stable/faq-and-cookbook.html). You can use random function to generate the customer profile (red, blue, green).

Note 1 : Don't use temporary variable to retrieve the current span. Use the trace directly.

Note 2 : Don't forget to import modules.


Rebuild the container images for the private registry:

=== "Shell Command"

    ```bash
    docker-compose build
    ```

Push the images to the private registry:

=== "Shell Command"

    ```bash
    docker-compose push
    ```
Delete the actual public-api deployment

=== "Shell Command"

    ```bash
    kubectl delete deploy public-api
    ```

Redeploy to the cluster with

=== "Shell Command"

    ```bash
    kubectl apply -f k8s
    ```

Test the service with

=== "Shell Command"

    ```bash
    ENDPOINT=$(kubectl get service/public-api -o jsonpath='{.spec.clusterIP}')
    curl http://$ENDPOINT:8000/api -F text=@hamlet.txt
    ```

Verify in your APM traces that you retrieve all the informations asked.

Now, Business team want to be able to compare the performance for each customer profile. [Index this span tag](https://docs.splunk.com/Observability/apm/span-tags/index-span-tags.html#index-a-new-span-tag) to be able to satisfy your Business team request.

The milestone for this task is `13custom-instr`. It add custom instrumentation.


## Future Tasks

TODO YOUR Idea here? Let us know!

TODO metrics method being traced - how to disable?

```python
from opentelemetry.context import attach, detach, set_value
token = attach(set_value("suppress_instrumentation", True))
```

TODO autodetect metrics with k8s labels: `prometheus.io/scrape: true` - run prometheus on separate port `9090`.

TODO [tracing examples][py-trace-ex]

[py-trace-ex]: https://github.com/open-telemetry/opentelemetry-python/blob/main/docs/examples/

