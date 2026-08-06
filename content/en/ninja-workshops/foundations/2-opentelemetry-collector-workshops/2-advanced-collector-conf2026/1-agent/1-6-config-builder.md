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
{{% tab title="Remote workshop instance" %}}

Copy the current file from the instance to your local computer:

```bash
scp -P 2222 \
  <workshop-user>@<workshop-host>:~/advanced-otel-workshop/1-agent/agent_config.yaml \
  ~/Downloads/agent_config.yaml
```

{{% /tab %}}
{{< /tabs >}}

1. In Splunk Observability Cloud, open **Data Management > OTel Collector
   Config Builder**.
2. Upload or import `agent_config.yaml`.
3. Open **Component Inventory**, **Pipelines**, and **Collector YAML**.

Button labels can change as Config Builder evolves. Use the action that imports
an existing Collector configuration.

![OTel Collector Config Builder component inventory](../images/otel-collector-config-builder.png)

{{% notice title="Keep credentials out of Config Builder" style="warning" %}}
Upload `agent_config.yaml`, not `workshop-env.sh`. The YAML contains environment
variable references; `workshop-env.sh` can contain your ingest token.
{{% /notice %}}

{{% expand title="How this Agent configuration works" %}}

The Agent has three input paths:

| Pipeline | Receives | Processes | Always exports locally |
|---|---|---|---|
| `traces` | OTLP/HTTP from `loadgen` | Memory limit, system resource detection, Agent label | Debug console and `agent-traces.out` |
| `metrics` | Hourly host CPU and OTLP/HTTP | Memory limit, system resource detection, Agent label | Debug console and `agent-metrics.out` |
| `logs` | OTLP/HTTP and `quotes.log` | Memory limit, system resource detection, Agent label | Debug console and `agent-logs.out` |

If cloud export was selected during setup, the same `traces` pipeline also
uses `otlp_http`, and the same `metrics` pipeline also uses `signalfx`. There
is no second local configuration or separate metrics pipeline.

`health_check` provides the readiness endpoint on port `13133`.
`resource/add_mode` adds `otelcol.service.mode=agent` so processed data is easy
to identify.

{{% /expand %}}

Keep this Config Builder project open for Chapters 2 through 4.

{{% /exercise %}}

{{< checkpoint "The three Agent pipelines are visible in Config Builder." >}}
