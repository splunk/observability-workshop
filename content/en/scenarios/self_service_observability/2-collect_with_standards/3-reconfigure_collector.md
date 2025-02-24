---
title: Reconfigure Collector
linkTitle: 2.3 Reconfigure Collector
weight: 3
time: 10 minutes
---

## Reconfigure Collector

To reconfigure the collector we need to make these changes:

* In `agent_config.yaml`
  * We need to adjust the **signalfx** exporter to use the gateway
  * The **otlp** exporter is already there, so we leave it alone
  * We need to change the pipelines to use **otlp**
* In `splunk-otel-collector.conf`
  * We need to set the `SPLUNK_GATEWAY_URL` to the url provided by the instructor

See this [documentation page](https://docs.splunk.com/observability/en/gdi/opentelemetry/deployment-modes.html#agent-configuration) for more details.

The exporters will be the following:

``` yaml
exporters:
  # Metrics + Events
  signalfx:
    access_token: "${SPLUNK_ACCESS_TOKEN}"
    #api_url: "${SPLUNK_API_URL}"
    #ingest_url: "${SPLUNK_INGEST_URL}"
    # Use instead when sending to gateway
    api_url: "http://${SPLUNK_GATEWAY_URL}:6060"
    ingest_url: "http://${SPLUNK_GATEWAY_URL}:9943"
    sync_host_metadata: true
    correlation:
  # Send to gateway
  otlp:
    endpoint: "${SPLUNK_GATEWAY_URL}:4317"
    tls:
      insecure: true
```

The others you can leave as they are, but they won't be used, as you will see in the pipelines.

The pipeline changes (you can see the items commented out and uncommented out):

``` yaml
service:
  pipelines:
    traces:
      receivers: [jaeger, otlp, smartagent/signalfx-forwarder, zipkin]
      processors:
      - memory_limiter
      - batch
      - resourcedetection
      #- resource/add_environment
      #exporters: [sapm, signalfx]
      # Use instead when sending to gateway
      exporters: [otlp, signalfx]
    metrics:
      receivers: [hostmetrics, otlp, signalfx, smartagent/signalfx-forwarder]
      processors: [memory_limiter, batch, resourcedetection]
      #exporters: [signalfx]
      # Use instead when sending to gateway
      exporters: [otlp]
    metrics/internal:
      receivers: [prometheus/internal]
      processors: [memory_limiter, batch, resourcedetection]
      # When sending to gateway, at least one metrics pipeline needs
      # to use signalfx exporter so host metadata gets emitted
      exporters: [signalfx]
    logs/signalfx:
      receivers: [signalfx, smartagent/processlist]
      processors: [memory_limiter, batch, resourcedetection]
      exporters: [signalfx]
    logs:
      receivers: [fluentforward, otlp]
      processors:
      - memory_limiter
      - batch
      - resourcedetection
      #- resource/add_environment
      #exporters: [splunk_hec, splunk_hec/profiling]
      # Use instead when sending to gateway
      exporters: [otlp]
```

And finally we can add the `SPLUNK_GATEWAY_URL` in `splunk-otel-collector.conf`, for example:

``` conf
SPLUNK_GATEWAY_URL=gateway.splunk011y.com
```

Then we can restart the collector:

``` bash
sudo systemctl restart splunk-otel-collector.service
```

And check the status:

``` bash
sudo systemctl status splunk-otel-collector.service
```

And finally see the new dimension on the metrics:
![New Dimension](../images/gateway_dimension.png)
