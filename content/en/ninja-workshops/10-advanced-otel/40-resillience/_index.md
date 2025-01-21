---
title: Building Resilience in OpenTelemetry Collector Using the File Storage Extension
linkTitle: 4. Resilience
time: 10 minutes
weight: 4
---

We will walk through how to use OpenTelemetry Collector’s `file_storage` extension to build resilience into your telemetry pipeline. Specifically, we will demonstrate how to use the file storage extension for checkpointing, managing retries, and handling temporary failures effectively.

The goal is to show how this configuration allows your OpenTelemetry Collector to reliably store intermediate states on disk, ensuring that no data is lost during network failures, and that the collector can resume where it left off.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}

- This will only be useful if the connections fails for a short period like up to 15 minutes or so. If the connection is down for longer periods, the backend will drop the data anyways because the timing's are too far out of synch.
- This will works for logs, but we will introduce a more robust solution in one of the upcoming collector builds.

{{% /notice %}}

### Setup

Create a new sub directory called `4-resilience` and copy the content from `3-filelog` across and remove any *.out file. Your starting point for this exercise should be:

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── log-gen.sh
│   ├── quotes.log
│   └── trace.json
└── otelcol
```

In this exercise we are going to update the agent.yaml by adding an `extensions:` section.
This new section in an OpenTelemetry configuration YAML is used to define optional components that enhance or modify the behavior of the OpenTelemetry Collector. These components don’t handle telemetry data directly but provide additional capabilities or services to the Collector.
The first exercise will be providing **Checkpointing** with the  `file_storage` extension.  
The `file_storage` extension is used to ensure that the OpenTelemetry Collector can persist checkpoints to disk. This is especially useful in cases where there are network failures or restarts. This way, the collector can recover from where it left off without losing data.
<!--
2. **Retries** with the `otlp/gateway` exporter.
3. **Queueing** with `sending_queue` and the integration of file storage for resilience.
-->

{{% notice title="Exercise" style="green" icon="running" %}}

Let's add the extension part first:

1. **Add** `extensions:` **section**: Place this at the top of the `agent.yaml`.
2. **Add** `file_storage` **extension**: Under the **extensions** section. Name it `/checkpoint:`.
3. **Add** `directory:` **key**: under the `file_storage` extension and set it to a value of `"./checkpoint-folder"`
4. **Add** `create_directory:` **key**: Set the Value to `true`.
5. **Add** `timeout:` **key**: Set the value to `1s`.
6. **Add** `compaction:` **key** section.
7. **Add** `on_start:` **key**: Under the `compaction:` section, set the value to ``true`.
7. **Add** `directory:` **key**: Set the value to `./checkpoint-folder/tmp`.
8. **Add** `max_transaction_size:` **key**: Set it to a value of `65_536`

{{% /notice%}}

**Explanation:**

- `directory: ./checkpoint-folder`: Defines the folder where checkpoint files will be stored.
- `create_directory: true`: Ensures that the directory is created if it doesn’t already exist.
- `timeout: 1s`: Specifies a timeout for file operations related to the checkpointing.
- `compaction`: Ensures that old checkpoint data is compacted periodically.
  - `on_start: true` : Determines whether the compaction process begins immediately when the OpenTelemetry Collector starts.
  - `directory:` `./checkpoint-folder/tmp`: Specifies the directory used for compaction (as a midstep).
  - `max_transaction_size` defines the size limit for checkpoint transactions before compaction occurs.

The next exercise is modifying the `otlphttp:` exporter where retries and queueing are configured.

{{% notice title="Exercise" style="green" icon="running" %}}
We are going to extend the existing `otlphttp` exporter:

```yaml
exporters:
  otlphttp:
    endpoint: "localhost:5317"
    headers:
      X-SF-Token: "FAKE_SPLUNK_ACCESS_TOKEN" # or your own version of a token
```

**Steps:**

1. **Add** `tls:` **key**: Place at the same indent level as `headers:`.
2. **Add** `insecure:` **key**: Under the `tls:` key and set its value to `true`.
3. **Add** `retry_on_failure:` **key**: Place at the same indent level as `headers:`.
4. **Add** `enabled:` **key**: Under the `retry_on_failure:` key and set its value to `true`.
5. **Add** `sending_queue:` **key**:
6. **Add** `enabled:` **key**: Under the `sending_queue:` key and set its value to `true`.
7. **Add** `num_consumers:` **key**: Set its value to `10`
8. **Add** `queue_size:`  **key**: Set its value to `10000`
9. **Add** `storage:` **key**: Set its value to `file_storage/checkpoint`

{{% /notice%}}

**Explanation:**

- `retry_on_failure.enabled: true`: Enables retrying when there is a failure in sending data to the OTLP gateway.
- `sending_queue`: Configures an internal queue to store data that couldn’t be sent. The `storage` option links the queue to the `file_storage/checkpoint` extension, ensuring resilience even in case of network failures.
  - `num_consumers: 10`: Specifies the number of consumers reading from the queue.
  - `queue_size: 10000`: The maximum size of the queue.
  - `storage: file_storage/checkpoint`: Specifies that the queue state will be backed up in the file system.

Again, validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)** for spelling mistakes etc. Your `Logs:` pipeline should like this:

![logs from otelbin](../images/filelog-3-1-logs.png)

This setup ensures your OpenTelemetry Collector can handle network interruptions gracefully by storing telemetry data on disk and retrying failed transmissions. It combines checkpointing for recovery and queueing for efficient retries, making your pipeline more resilient and reliable. Now, let’s test this configuration!
