---
title: 1.6 Upload the Configuration to Config Builder
linkTitle: 1.6 Upload Config YAML
weight: 6
---

The starter file begins with Splunk Distribution's default Agent configuration
and adds local components for this workshop. Use Config Builder to see how each
component participates in a pipeline before modifying it in later chapters.

The setup script downloads this workshop-maintained copy; it does not download
Splunk's file directly. The comparison in this step uses the
[Splunk Distribution 0.157.0 default `agent_config.yaml`](https://github.com/signalfx/splunk-otel-collector/blob/v0.157.0/cmd/otelcol/config/collector/agent_config.yaml),
matching the Collector binary used in the workshop.

{{% exercise title="Open agent_config.yaml in Config Builder" %}}

## Download `agent_config.yaml`

[Download the .conf26 `agent_config.yaml`](https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/agent_config.yaml)

Save it to your local computer as `agent_config.yaml`. You can also run:

```bash
curl -fL \
  https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/agent_config.yaml \
  -o agent_config.yaml
```

## Import it

1. Sign in to Splunk Observability Cloud.
2. Open **Data Management > OTel Collector Config Builder**.
3. Choose the action to upload or import an existing configuration.
4. Select `agent_config.yaml`.
5. Open the component inventory, pipeline view, and generated Collector YAML.

The precise button labels can change as Config Builder evolves. Use the action
that imports existing Collector YAML; do not start from an empty configuration.

![Illustrative OTel Collector Config Builder component inventory](../images/otel-collector-config-builder.png)

## Component inventory: default or workshop-specific?

The labels below compare the imported file with Splunk's pinned `0.157.0`
default. **Default** means the component definition exists upstream.
**Workshop** means this edition adds it. **Adjusted** means the component comes
from the default, but this file changes its name, settings, or pipeline use.
**Default-derived** means the workshop carries the default behavior and
settings under a different component ID.

### Extensions

All six extensions in the imported file come from Splunk's default Agent
configuration.

| Component | Origin | Purpose |
|---|---|---|
| `headers_setter` | Default | Supplies `X-SF-Token` to authenticated requests. |
| `health_check` | Default | Exposes the Collector health endpoint used in Step 1.1. |
| `http_forwarder` | Default | Forwards requests from the local API ingress to the Splunk API endpoint. |
| `http_forwarder/opamp_splunk_o11y` | Default | Forwards the local OpAMP ingress to the Splunk ingest endpoint. |
| `opamp/splunk_o11y` | Default | Defines Splunk OpAMP connectivity. Collector startup removes it unless the `splunk.opamp.enabled` feature gate is enabled. |
| `zpages` | Default | Provides diagnostic pages, including `expvar`. |

### Receivers

| Component | Origin | Purpose |
|---|---|---|
| `fluent_forward` | Default | Receives Fluent Forward log data. |
| `host_metrics` | Default | Collects CPU, disk, filesystem, memory, network, load, paging, and process-count metrics. |
| `jaeger` | Default | Receives Jaeger traces over the configured protocols. |
| `otlp` | Default | Receives OTLP telemetry over gRPC and HTTP. The load generator sends traces here. |
| `prometheus/internal` | Default, adjusted | Scrapes the Collector's own metrics. The workshop binds the scrape target to `127.0.0.1:8888` instead of the upstream `0.0.0.0:8888`. |
| `smartagent/processlist` | Default | Collects process-list data for the `logs/signalfx` support pipeline. |
| `zipkin` | Default | Receives Zipkin traces. |
| `nop` | Default | Provides the placeholder receiver for the entity pipeline populated by discovery mode. |
| `file_log/quotes` | Workshop | Reads the synthetic `quotes.log` file used in the log exercises. |

### Processors

| Component | Origin | Purpose |
|---|---|---|
| `memory_limiter` | Default | Protects the Collector from exceeding its configured memory limit. |
| `batch` | Default | Batches telemetry before export. |
| `resource_detection` | Default-derived, adjusted | Uses the default detectors and settings. Splunk's pinned file uses the component ID `resourcedetection`; the workshop copy uses `resource_detection`. |
| `resource/add_mode` | Workshop | Adds `otelcol.service.mode=agent` to telemetry passing through each pipeline, making Agent-processed data easy to identify locally. |

{{% notice title="Two different service-mode labels" style="note" %}}
Splunk's default file already sets `otelcol.service.mode=agent` under
`service.telemetry.resource.attributes`. That setting labels the Collector's
own internal telemetry. The workshop's `resource/add_mode` processor is
separate: it adds the same attribute to application and host telemetry flowing
through the pipelines.
{{% /notice %}}

### Exporters

| Component | Origin | Purpose |
|---|---|---|
| `otlp_http` | Default | Sends traces directly to Splunk APM. |
| `signalfx` | Default | Sends metrics, events, process-list data, and host metadata to Splunk Observability Cloud. |
| `otlp_http/entities` | Default | Sends entity events when discovery mode is enabled. |
| `splunk_hec` | Default | Sends regular logs to the separately configured Splunk Platform HEC endpoint. |
| `splunk_hec/profiling` | Default | Sends profiling data to the Splunk ingest endpoint. |
| `debug` | Default, adjusted | Exists in Splunk's default file but is not connected to its active Agent pipelines. The workshop connects it to `traces`, `metrics`, and `logs` for console validation. |
| `file/traces` | Workshop | Writes trace OTLP JSON to `agent-traces.out`. |
| `file/metrics` | Workshop | Writes metric OTLP JSON to `agent-metrics.out`. |
| `file/logs` | Workshop | Writes log OTLP JSON to `agent-logs.out`. |
| `otlp_grpc/gateway` | Default, intentionally omitted | Splunk's default file defines this optional exporter for a Gateway deployment. This single-Agent workshop removes it. |

### Pipelines

All six pipeline names come from the default Agent configuration. The
workshop preserves their Splunk exporters and adds or connects the components
shown below.

| Pipeline | Default path | Workshop additions |
|---|---|---|
| `traces` | Jaeger, OTLP, and Zipkin → default processors → `otlp_http` | Adds `resource/add_mode`, `debug`, and `file/traces`. |
| `metrics` | Host Metrics and OTLP → default processors → `signalfx` | Adds `resource/add_mode`, `debug`, and `file/metrics`. |
| `metrics/internal` | `prometheus/internal` → default processors → `signalfx` | Adds `resource/add_mode`; keeps the default Splunk exporter. |
| `logs/signalfx` | `smartagent/processlist` → default processors → `signalfx` | Adds `resource/add_mode`; keeps the default Splunk exporter. |
| `logs/entities` | `nop` → default processors → `otlp_http/entities` | Adds `resource/add_mode`; keeps the default Splunk exporter. |
| `logs` | Fluent Forward and OTLP → default processors → both Splunk HEC exporters | Adds `file_log/quotes`, `resource/add_mode`, `debug`, and `file/logs`. |

The active pipelines continue to export directly to the configured Splunk
backends; no telemetry is routed through a Gateway. The local `debug` and file
exporters provide a second validation path without replacing the default
Splunk exporters.

{{% notice title="Secrets stay outside Config Builder" style="warning" %}}
The YAML contains environment-variable references, not token values. Never
paste `workshop-env.sh` or a real access/HEC token into Config Builder.
{{% /notice %}}

Keep this Config Builder project open. You will modify this configuration in
Chapters 2, 3, and 4.

{{% /exercise %}}

{{< checkpoint "The default Splunk pipelines and workshop-only local components have been identified in Config Builder." >}}
