# OpenTelemetry Astronomy Shop Demo Instructions

## Features available

- Kubernetes Navigator
- APM
- DB Query Performance (Redis & PostgreSQL)
- Logs
- Synthetics (no Synthetics to APM due to no `Server-Timing` header support upstream)
- Redis Dashboard
- Kafka Dashboard (Partial)
- PostgreSQL Dashboard

## Missing features

- Code Profiling
- RUM

## Splunk OpenTelemety Collector Configuration

The following configuration can be applied to a default O11y workshop Splunk Show instance. Remember to remove any existing OTel Collector configuration.

``` bash
helm delete splunk-otel-collector
```

### Deploy the OTel Collector via Helm chart

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

``` bash
helm install splunk-otel-collector \
--set="operator.enabled=true" \
--set="certmanager.enabled=true" \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkObservability.logsEnabled=false" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f otel-demo-collector.yaml
```

## OpenTelemetry Astronomy Shop configuration

The file `otel-demo.yaml` will be applied to the Helm chart and change the behavior of the default configuration:

- Set `OTEL_COLLECTOR_NAME` to the host IP Address for Metrics, Traces and Logs
- Configure a load balancer for the `frontendProxy` server
- Customise Kafka configuration to expose metrics via JMX on port 5555
- Disable native OTel Collector, Jaeger, Prometheus & Grafana

### Deploy the OpenTelemetry Astronomy Shop

``` text
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
```

``` text
helm install opentelemetry-demo open-telemetry/opentelemetry-demo --values otel-demo.yaml
```

## Port forwarding

``` bash
kubectl port-forward svc/opentelemetry-demo-frontendproxy 8083:8080 --address="0.0.0.0"
```

### OpenTelemetry Redis receiver configuration

At the time of writing, there are no OOTB dashboards for OpenTelemetry receivers. You can still use these receivers and build out custom dashboards using the existing SmartAgent OOTB dashboards as templates. You can import `dashboard_REDIS INSTANCES (OTEL).json` as an example.

``` yaml
redis:
  rule: type == "pod" && name matches "redis"
  config:
    endpoint: '`endpoint`:6379'
```
