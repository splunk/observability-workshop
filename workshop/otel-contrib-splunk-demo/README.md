# OpenTelemetry Astronomy Shop Demo Instructions

## Features available

- Kubernetes Navigator
- APM
- DB Query Performance (Redis & PostgreSQL)
- Logs
- Synthetics (no Synthetics to APM due to no `Server-Timing` header support upstream)

## Missing features

- Code Profiling
- RUM
- K8s SmartAgent monitors (no SmartAgent support for OTel)

## Splunk OpenTelemety Collector Configuration

The following configuration can be applied to a default O11y workshop Splunk Show instance. Remember to remove any existing OTel Collector configuration.

``` bash
helm delete splunk-otel-collector
```

### Deploy the OTel Contrib Collector

``` bash
cd ~/workshop/otel-contrib-splunk-demo
```

Edit `k8s_manifests/configmap-and-secrets.yaml` and configure `REALM`, `splunk_hec_url`, `k8s_cluster_name`, `deployment_environment`, `splunk_observability_access_token` and `splunk_hec_token`.

``` bash
kubectl apply -f k8s_manifests/
```

## OpenTelemetry Astronomy Shop configuration

The file `opentelemetry-demo-values.yaml` will be applied to the Helm chart and change the behaviour of the default configuration:

- Set `OTEL_COLLECTOR_NAME` to the host IP Address for Metrics, Traces and Logs
- Configure a load balancer for the `frontendProxy` server
- Disable native OTel Collector, Jaeger, Prometheus & Grafana

### Deploy the OpenTelemetry Astronomy Shop

``` text
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
```

``` text
helm install opentelemetry-demo open-telemetry/opentelemetry-demo --values opentelemetry-demo-values.yaml
```
