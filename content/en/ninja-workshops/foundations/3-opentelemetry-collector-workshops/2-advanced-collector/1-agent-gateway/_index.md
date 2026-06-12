---
title: 1. Verify Agent Configuration
linkTitle: 1. Agent Configuration
time: 15 minutes
weight: 3
---
Welcome! In this section, we’ll begin with a fully functional OpenTelemetry setup that includes both an **Agent** and a **Gateway**.

We’ll start by quickly reviewing their configuration files to get familiar with the overall structure and to highlight key sections that control the telemetry pipeline.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Throughout the workshop, you’ll work with multiple terminal windows. To keep things organized, give each terminal a unique name or color. This will help you easily recognize and switch between them during the exercises.

We will refer to these terminals as: **Agent**, **Gateway**, **Loadgen**, and **Test**.
{{% /notice %}}

{{% exercise title="Verify the agent files" %}}

1. Create your first terminal window and name it **Agent**. Navigate to the directory for the first exercise `[WORKSHOP]/1-agent-gateway` and verify that the required files have been generated:

    ```bash
    cd 1-agent-gateway
    ls -l
    ```
  
2. You should see the following files in the directory. If not, re-run the `setup-workshop.sh` script as described in the **Pre-requisites** section:

    ```text { title="Directory Structure" }
    .
    ├── agent.yaml
    └── gateway.yaml
    ```

{{% /exercise %}}

## Understanding the Agent configuration

Let’s review the key components of the `agent.yaml` file used in this workshop. We’ve made some important additions to support metrics, traces, and logs.

### Receivers

The `receivers` section defines how the **Agent** ingests telemetry data. In this setup, three types of receivers have been configured:

* **Host Metrics Receiver**

  ```yaml
  hostmetrics:                         # Host Metrics Receiver
    collection_interval: 3600s         # Collection Interval (1hr)
    scrapers:
      cpu:                             # CPU Scraper
  ```

  Collects CPU usage from the local system every hour. We’ll use this to generate example metric data.

* **OTLP Receiver (HTTP protocol)**

  ```yaml
  otlp:                                # OTLP Receiver
    protocols:
      http:                            # Configure HTTP protocol
        endpoint: "0.0.0.0:4318"       # Endpoint to bind to
  ```

  Enables the agent to receive metrics, traces, and logs over HTTP on port `4318`.  This is used to send data to the collector in future exercises.

* **FileLog Receiver**

  ```yaml
  filelog/quotes:                      # Receiver Type/Name
    include: ./quotes.log              # The file to read log data from
    include_file_path: true            # Include file path in the log data
    include_file_name: false           # Exclude file name from the log data
    resource:                          # Add custom resource attributes
      com.splunk.source: ./quotes.log  # Source of the log data
      com.splunk.sourcetype: quotes    # Source type of the log data
  ```

  Enables the agent to tail a local log file (`quotes.log`) and convert it to structured log events, enriched with metadata such as `source` and `sourceType`.

### Exporters

* **Debug Exporter**

  ```yaml
    debug:                               # Exporter Type
      verbosity: detailed                # Enabled detailed debug output
  ```

* **OTLPHTTP Exporter**

  ```yaml
    otlphttp:                            # Exporter Type
      endpoint: "http://localhost:5318"  # Gateway OTLP endpoint  
  ```

  The `debug` exporter sends data to the console for visibility and debugging during the workshop while the `otlphttp` exporter forwards all telemetry to the local **Gateway** instance.

  **This dual-export strategy ensures you can see the raw data locally while also sending it downstream for further processing and export.**
