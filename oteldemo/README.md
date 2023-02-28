# OTel Demo Instructions

Edit the `otel-demo-collector.yaml` and set the REALM.

**otel-demo-collector.yaml**

``` yaml
agent:
  config:
    exporters:
      otlphttp:
        traces_endpoint: "https://ingest.{REALM}.signalfx.com/v2/trace/otlp"
        compression: gzip
        headers:
          "X-SF-Token": "${SPLUNK_OBSERVABILITY_ACCESS_TOKEN}"
      logging:
        loglevel: debug
    service:
      pipelines:
        traces:
          exporters:
          - sapm
          - signalfx
          - otlphttp
          - logging
          processors:
          - memory_limiter
          - k8sattributes
          - batch
          - resourcedetection
          - resource
          - resource/add_environment
          receivers:
          - otlp
          - jaeger
          - smartagent/signalfx-forwarder
          - zipkin
```

Using a standard workshop instance install Splunk Otel Collector

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

``` text
helm install splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$(hostname)-k3s-cluster" \
--set="splunkObservability.logsEnabled=true" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="environment=$(hostname)-apm-env" \
splunk-otel-collector-chart/splunk-otel-collector \
-f otel-demo-collector.yaml
```

Customise the OTel Demo deployment to not use Grafana, Jaeger, Prometheus and OTel Collector. Also, have the traces sent to the Splunk OTel Collector.

**otel-demo.yaml**

``` yaml
# Set the OTEL_COLLECTOR_NAME environment variable to the IP address of the node
default:
  envOverrides:
    - name: OTEL_COLLECTOR_NAME
      valueFrom:
        fieldRef:
          fieldPath: status.hostIP

# Configure the frontendProxy service to be of type LoadBalancer
components:
  frontendProxy:
    service:
      type: LoadBalancer

# Disable the observability components incl. the collector
observability:
  otelcol:
    enabled: false
  jaeger:
    enabled: false
  prometheus:
    enabled: false
  grafana:
    enabled: false
```

Deploy the OTel Demo

``` text
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
```

``` text
helm install my-otel-demo open-telemetry/opentelemetry-demo --values otel-demo.yaml
```

**NOTE:** There is no profiling, DB Query Performance or RUM support
