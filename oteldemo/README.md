# OpenTelemetry Astronomy Shop Demo Instructions

## Features available

- IM (Kubernetes)
- APM
- Network Explorer
- DB Query Performance (Redis only)
- Logs (using OTel Log Engine)
- Synthetics (no Synthetics to APM due to no `Server-Timing` header support in upstream)
- Redis Dashboard
- Kafka Dashboard
- PostgreSQL Dashboard

## Missing features

- Code Profiling
- DB Query Performance (PostgreSQL)
- RUM

## Configuration and installation

Edit the `otel-demo-collector.yaml` and set the REALM.

**otel-demo-collector.yaml**

``` yaml
agent:
  config:
    receivers:
      receiver_creator:
        receivers:
          smartagent/redis:
            rule: type == "pod" && name matches "redis"
            config:
              type: collectd/redis
              endpoint: '`endpoint`:6379'
          smartagent/kafka:
            rule: type == "pod" && name matches "kafka"
            config:
              type: collectd/kafka
              endpoint: '`endpoint`:5555'
              clusterName: otel-kafka
          smartagent/kafka_consumer:
            rule: type == "pod" && name matches "kafka"
            config:
              type: collectd/kafka
              endpoint: '`endpoint`:5555'
              clusterName: otel-kafka
          smartagent/kafka_producer:
            rule: type == "pod" && name matches "kafka"
            config:
              type: collectd/kafka
              endpoint: '`endpoint`:5555'
              clusterName: otel-kafka
          smartagent/postgres:
            rule: type == "pod" && name matches "ffspostgres"
            config:
              type: collectd/postgresql
              endpoint: '`endpoint`:5432'
              username: "ffs"
              password: "ffs"
              databases:
              - name : "ffs"
    exporters:
      otlphttp:
        traces_endpoint: "https://ingest.{REALM}.signalfx.com/v2/trace/otlp"
        compression: gzip
        headers:
          "X-SF-Token": "${SPLUNK_OBSERVABILITY_ACCESS_TOKEN}"
      logging:
        loglevel: info
    service:
      pipelines:
        metrics:
          exporters:
          - signalfx
          - logging
          processors:
          - memory_limiter
          - batch
          - resourcedetection
          - resource
          receivers:
          - hostmetrics
          - kubeletstats
          - otlp
          - receiver_creator
          - signalfx
        traces:
          exporters:
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
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="networkExplorer.enabled=true" \
--set="networkExplorer.podSecurityPolicy.enabled=false" \
--set="agent.enabled=true" \
--set="gateway.replicaCount=1" \
--set="gateway.resources.limits.cpu=500m" \
--set="gateway.resources.limits.memory=1Gi" \
--set="clusterReceiver.enabled=true" \
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
  kafka:
    enabled: true
    useDefault:
      env: true
    ports:
      - name: plaintext
        value: 9092
      - name: controller
        value: 9093
    env:
      - name: KAFKA_ADVERTISED_LISTENERS
        value: 'PLAINTEXT://{{ include "otel-demo.name" . }}-kafka:9092'
      - name: OTEL_EXPORTER_OTLP_ENDPOINT
        value: http://$(OTEL_COLLECTOR_NAME):4317
      - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
        value: cumulative
      - name: KAFKA_HEAP_OPTS
        value: "-Xmx400M -Xms400M"
      - name: KAFKA_OPTS
        value: "-javaagent:/tmp/opentelemetry-javaagent.jar -Dotel.jmx.target.system=kafka-broker -Dcom.sun.management.jmxremote.port=5555"        
    resources:
      limits:
        memory: 750Mi
    securityContext:
      runAsUser: 1000  # appuser
      runAsGroup: 1000
      runAsNonRoot: true

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
