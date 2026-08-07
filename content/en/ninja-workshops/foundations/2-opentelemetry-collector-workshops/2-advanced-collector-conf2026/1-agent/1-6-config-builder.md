---
title: 1.6 Upload the Configuration to Config Builder
linkTitle: 1.6 Upload Config YAML
weight: 6
---

Upload `agent_config.yaml` to see its components and pipelines before you
modify them.

{{% exercise title="Open agent_config.yaml in Config Builder" %}}

Make `agent_config.yaml` available to the computer running your browser.

{{< tabs id="config-builder-upload-file" >}}
{{% tab title="Same computer" %}}

Select `[WORKSHOP]/1-agent/agent_config.yaml` when Config Builder opens the file
picker.

{{% /tab %}}
{{% tab title="Splunk Show instance" %}}

Copy the current file from the instance to your local computer. Replace
`workshop-user` and `workshop-host` with the supplied SSH details:

```bash
scp \
  workshop-user@workshop-host:~/advanced-otel-workshop/1-agent/agent_config.yaml \
  ~/Downloads/agent_config.yaml
```

This example uses standard SSH port 22. If your facilitator supplies a
different port or copy command, use those details instead.

{{% /tab %}}
{{< /tabs >}}

1. In Splunk Observability Cloud, open **Data Management > OTel Collector
   Config Builder**.
2. Upload or import `agent_config.yaml`.
3. Open **Component Inventory**, **Pipelines**, and **Collector YAML**.

{{% notice title="Keep credentials out of Config Builder" style="warning" %}}
Upload `agent_config.yaml`, not `workshop-env.sh`. The YAML contains environment
variable references; `workshop-env.sh` can contain your access token.
{{% /notice %}}

{{% expand title="How this Agent configuration works" %}}

The Agent has three signal types and eight pipelines. Six come from the
Splunk Distribution's default `v0.157.0` Agent configuration; the two names
ending in `/workshop` are added for this lab:

| Pipeline | Purpose | Export |
|---|---|---|
| `traces` | Retains the default Jaeger, OTLP, and Zipkin receivers; `loadgen` uses OTLP/HTTP | Debug, `agent-traces.out`, and optional APM export |
| `metrics` | Collects the normal host-metrics set every 10 seconds | SignalFx in cloud mode; `nop` when cloud export is skipped |
| `metrics/internal` | Scrapes the Collector's own Prometheus metrics | SignalFx in cloud mode; `nop` when cloud export is skipped |
| `logs/signalfx` | Collects the default process-list events | SignalFx in cloud mode; `nop` when cloud export is skipped |
| `metrics/workshop` | Collects CPU at startup and then hourly | Debug and `agent-metrics.out` |
| `logs` | Retains the default OTLP and Fluent Forward path | `splunk_hec` and `splunk_hec/profiling`; HEC environment variables remain optional for the live lab |
| `logs/entities` | Retains the discovery-mode entity path | Observability Cloud entity endpoint when discovery adds receivers |
| `logs/workshop` | Receives OTLP/HTTP and reads `quotes.log` | Debug and `agent-logs.out` |

The workshop-specific pipelines protect the normal destination paths from
exercise-only debug and file output. There is still only one
`agent_config.yaml`.

`health_check` provides the readiness endpoint on port `13133`.
`resource/add_mode` adds `otelcol.service.mode=agent` so processed data is easy
to identify.

{{% /expand %}}

Keep this Config Builder project open for Chapters 2 through 4.

{{% /exercise %}}

{{< checkpoint "The eight Agent pipelines are visible in Config Builder." >}}
