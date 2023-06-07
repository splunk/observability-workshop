---
title: Microservices Auto-instrumentation
weight: 5
---
The development team has broken up the monolithic service into microservices baesd on the `docker-compose` setup. Switch to the provided milestone `10microservices` with the instructions from "Getting Started".

Test the service with:

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` bash
curl -X POST http://127.0.0.1:8000/api -F text=@hamlet.txt
```

{{% /tab %}}
{{< /tabs >}}

Add auto-instrumentation to the `public_api` microservice using the [Splunk distribution of OpenTelemetry Python][splunk-otel-python]. Review the [documentation][splunk-py-instrument] and the [getting Started][splunk-py-instrument] steps and apply it to `Dockerfile`.

Take into account the [trace exporter][otel-py-exporter] settings and add the required environment variables to the `.env` file for `docker-compose`. Use the configuration to send traces directly to Splunk  Observability Cloud.

The milestone for this task is `10microservices-autoi`. It has auto-instrumentation applied for *all* microservices.

[splunk-otel-python]: https://github.com/signalfx/splunk-otel-python
[otel-py-exporter]: https://github.com/signalfx/splunk-otel-python/blob/main/docs/advanced-config.md#trace-exporters
[splunk-py-instrument]: https://docs.splunk.com/Observability/gdi/get-data-in/application/python/get-started.html#nav-Instrument-a-Python-application
