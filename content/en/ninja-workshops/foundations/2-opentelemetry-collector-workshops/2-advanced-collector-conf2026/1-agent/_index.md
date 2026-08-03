---
title: 1. Verify Agent Configuration
linkTitle: 1. Agent Configuration
time: 20 minutes
weight: 3
---

Welcome! In this section, we’ll begin with one fully functional OpenTelemetry
Collector running in **Agent** mode on the workshop host.

We’ll start by reviewing its configuration file to get familiar with the
overall structure and to highlight the sections that control the metrics,
traces, and logs pipelines.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Throughout the workshop, you’ll work with multiple terminal windows. To keep
things organized, give each terminal a unique name or color.

We will refer to these terminals as **Agent Console**, **Loadgen**, and
**Tests**.
{{% /notice %}}

{{% exercise title="Verify the Agent files" %}}

1. Open a terminal and name it **Loadgen**. Navigate to the directory created
   by the setup script:

   ```bash
   cd [WORKSHOP]/1-agent
   ls -l
   ```

2. You should see:

   ```text { title="Directory Structure" }
   .
   ├── agent_config.yaml
   ```

3. Open a second terminal and name it **Agent Console**. Start the portable
   Collector from the Agent directory:

   ```bash
   cd [WORKSHOP]/1-agent
   source ../workshop-env.sh
   ../otelcol --config=agent_config.yaml
   ```

   Keep this foreground process running. Its console is where you will inspect
   the detailed debug output. Press `Ctrl-C` when you need to stop the Agent.

{{% /exercise %}}

## Understanding the Agent configuration

Let’s review the workshop additions to `agent_config.yaml`. Step 1.5 provides a
complete inventory of the Splunk Distribution defaults. This workshop uses one
Agent and no Gateway.

### Workshop receivers

The Splunk default receivers are present. These three are used directly in the
first exercise.

* **Host Metrics Receiver**

  ```yaml
  host_metrics:
    collection_interval: 10s
    scrapers:
      cpu:
      disk:
      filesystem:
      load:
      memory:
      network:
      paging:
      processes:
  ```

  It collects telemetry about the Linux host or Apple Silicon Mac every 10
  seconds. The precise metrics available depend on the operating system.

* **OTLP Receiver using HTTP**

  ```yaml
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"
  ```

  It enables the Agent to receive OTLP metrics, traces, and logs over HTTP on
  port `4318`. The workshop load generator uses this receiver for traces.

* **FileLog Receiver**

  ```yaml
  file_log/quotes:
    include:
      - ./quotes.log
    start_at: beginning
    include_file_path: true
    resource:
      service.name: quote-generator
      com.splunk.source: ./quotes.log
      com.splunk.sourcetype: quotes
  ```

  It tails `quotes.log` and converts each line into an OpenTelemetry log
  record enriched with service, source, and sourcetype resource metadata.

### Workshop processing

The default memory limiting, batching, and resource detection remain enabled.
The workshop adds `resource/add_mode` so local output is clearly labeled as
Agent telemetry:

```yaml
processors:
  resource/add_mode:
    attributes:
      - action: upsert
        key: otelcol.service.mode
        value: agent
```

### Default and workshop exporters

Default exporters send traces and metrics to Splunk Observability Cloud when
valid credentials are supplied. The optional `splunk_hec` exporter targets the
HEC endpoint entered during setup. The workshop additionally keeps the
detailed debug exporter and per-signal file exporters:

```yaml
exporters:
  debug:
    verbosity: detailed
  file/traces:
    path: ./agent-traces.out
  file/metrics:
    path: ./agent-metrics.out
  file/logs:
    path: ./agent-logs.out
```

These local exporters provide visibility and troubleshooting throughout the
workshop, including on Apple Silicon and in local-only mode.

{{% notice title="Two validation paths" style="note" %}}
Local debug/file validation always applies. With valid credentials, the
default `otlp_http` and `signalfx` exporters also send traces and metrics to
Splunk Observability Cloud. If setup reported local-only mode, cloud exporter
errors can be ignored and Step 1.6 must be skipped.
{{% /notice %}}
