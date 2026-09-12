---
title: 1.6 Upload the configuration to Config Builder
linkTitle: 1.6 Upload config YAML
weight: 6
time: 7 minutes
---

Upload `agent_config.yaml` to see its components and pipelines before you
modify them.

{{% exercise title="Open agent_config.yaml in Config Builder" %}}

Make `agent_config.yaml` available on the computer running your browser.

{{< tabs id="config-builder-upload-file" >}}
{{% tab title="Same computer" %}}

Use `[WORKSHOP]/1-agent/agent_config.yaml`, which the setup script created on
your computer.

{{% /tab %}}
{{% tab title="Splunk Show instance" %}}

Open the
[OBS1184 example agent configuration](https://github.com/splunk/observability-workshop/blob/main/workshop/ninja/obs1184/agent_config.yaml).
On GitHub, select **Download raw file** and save `agent_config.yaml` on the
computer running your browser.

During the standard cloud-enabled Splunk Show setup, the setup script downloads
this same configuration to the instance. Downloading another copy directly to
your local computer gives Config Builder the expected file without an `scp`
transfer or its possible SSH connection and file-path issues.

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

{{% expand title="How this agent configuration works" %}}

The agent has eight pipelines for three signal types. Six come from the
version `0.157.0` default agent configuration in the Splunk Distribution of
the OpenTelemetry Collector. The two pipelines ending in `/workshop` are for
this workshop:

| Pipeline | Purpose | Export |
| --- | --- | --- |
| `traces` | Receives traces through Jaeger, OpenTelemetry Protocol (OTLP), and Zipkin | Debug output, `agent-traces.out`, and optional Splunk APM export |
| `metrics` | Collects host metrics every 10 seconds | Splunk Observability Cloud in cloud mode; `nop` in local mode |
| `metrics/internal` | Collects the Collector's internal metrics | Splunk Observability Cloud in cloud mode; `nop` in local mode |
| `logs/signalfx` | Collects process-list events | Splunk Observability Cloud in cloud mode; `nop` in local mode |
| `metrics/workshop` | Collects CPU at startup and then hourly | Debug and `agent-metrics.out` |
| `logs` | Retains the default OTLP and Fluent Forward path | `splunk_hec` and `splunk_hec/profiling`; HEC environment variables remain optional for the live lab |
| `logs/entities` | Sends entity data when discovery adds receivers | Splunk Observability Cloud entity endpoint |
| `logs/workshop` | Receives OTLP/HTTP and reads `quotes.log` | Debug and `agent-logs.out` |

The workshop pipelines write sample data to local files so you can complete
the exercises without sending workshop logs to another system. All eight
pipelines are in one `agent_config.yaml` file.

The separate `/workshop` pipelines preserve the Splunk distribution's default
pipelines while adding `debug` and `file` exporters for hands-on validation.
This lets you inspect the workshop data locally without changing how the
standard pipelines are intended to deliver production telemetry.

`health_check` provides the readiness endpoint on port `13133`.
`resource/add_mode` adds `otelcol.service.mode=agent` so you can identify data
processed by this agent.

{{% /expand %}}

Keep this Config Builder project open for Chapters 2 through 4.

{{% /exercise %}}

{{< checkpoint "The eight agent pipelines are visible in Config Builder." >}}
