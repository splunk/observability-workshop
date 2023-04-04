# OpenTelemetry Astronomy Shop Demo Instructions

## Features available

- Kubernetes Navigator
- APM
- Network Explorer
- DB Query Performance (Redis & PostgreSQL)
- Logs (using OTel Log Engine via Log Observer)
- Synthetics (no Synthetics to APM due to no `Server-Timing` header support in upstream)
- Redis Dashboard
- Kafka Dashboard (Partial)
- PostgreSQL Dashboard (Partial)

## Missing features

- Code Profiling
- RUM

## Splunk OpenTelemety Collector Configuration

The following configuration can be applied to a standard O11y workshop instance (EC2 or multipass).

**otel-demo-collector.yaml**

https://github.com/splunk/observability-workshop/blob/f5521963d9c4bb4a63745013f133c23db1b8ae2a/oteldemo/otel-demo-collector.yaml#L1-L82

### Deploy the OTel Collector via Helm chart

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

## OpenTelemetry Astronomy Shop configuration

Create `otel-demo.yaml`, this will be applied to the Helm chart and changes the default behaviour of a default install:

- Set `OTEL_COLLECTOR_NAME` to the host IP Address for Metrics, Traces and Logs
- Configure a load balancer for the `frontendProxy` server
- Customise Kafka configuration to expose metrics via JMX on port 5555
- Disable native OTel Collector, Jaeger, Prometheus & Grafana

**otel-demo.yaml**

https://github.com/splunk/observability-workshop/blob/387727f814714a65ffbac9f73e5f89f05760268b/workshop/oteldemo/otel-demo.yaml#L1-L50

### Deploy the OpenTelemetry Astronomy Shop

``` text
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
```

``` text
helm install my-otel-demo open-telemetry/opentelemetry-demo --values otel-demo.yaml
```

## OpenTelemetry Receivers

**OpenTelemetry Redis receiver configuration**

At the time of writing there are no OOTB dashboards for OpenTelemetry receivers. You can still use these receivers and build out custom dashboards using the existing SmartAgent OOTB dashboards as templates. You can import `dashboard_REDIS INSTANCES (OTEL).json` as an example.

``` yaml
redis:
  rule: type == "pod" && name matches "redis"
  config:
    endpoint: '`endpoint`:6379'
```

