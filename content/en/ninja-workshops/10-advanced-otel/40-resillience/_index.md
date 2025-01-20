---
title: Building Resilience in OpenTelemetry Collector Using the File Storage Extension
linkTitle: 4. Resilience
time: 10 minutes
weight: 4
---

In this section, you will learn how to you can add basic resilience to the OpenTelemetry Collector. This will have the collector create a local queue, and will use that to restart sending data when the connection is back.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
Note, this will only be useful if the connections fails for a short period like a couple of minutes.  
If the connection is down for longer periods, the backend will drop the data anyways because the timing's are to far out of synch.

Secondly, this will works for logs, but we wil introduce a more robust solution in one of the upcoming collector builds  

{{% /notice %}}

### Setup

Create a new sub directory called `4-resilience` and copy the contents from `3-filelog` across. Create the appropriate log generation script script for your operating system in the new directory (`log-gen.sh` on Mac or Linux or `log-gen.ps1` for Windows).

### Overview

In this section, we will walk through how to use OpenTelemetry Collector’s `file_storage` extension to build resilience into your telemetry pipeline. Specifically, we will demonstrate how to use the file storage extension for checkpointing, managing retries, and handling temporary failures effectively.

The goal is to show how this configuration allows your OpenTelemetry Collector to reliably store intermediate states on disk, ensuring that no data is lost during network failures, and that the collector can resume where it left off.

We will use the provided YAML configuration to cover the following key concepts:

1. **Checkpointing** with `file_storage/checkpoint` extension.
2. **Retries** with the `otlp/gateway` exporter.
3. **Queueing** with `sending_queue` and the integration of file storage for resilience.

---

### Step 1: Setting Up the OpenTelemetry Collector

Ensure you have the OpenTelemetry Collector installed and running in your environment. You can download it from the [official OpenTelemetry website](https://opentelemetry.io/docs/collector/). For the sake of this workshop, we will assume you have already set up the OpenTelemetry Collector.

### Step 2: Understand the Key Configuration Elements

Let’s break down the key elements in your provided configuration file and understand how they contribute to resilience.

#### 1. **File Storage Extension for Checkpointing**

The `file_storage/checkpoint` extension is used to ensure that the OpenTelemetry Collector can persist checkpoints to disk. This is especially useful in cases where there are network failures or restarts. This way, the collector can recover from where it left off without losing data.

```yaml
extensions:
  file_storage/checkpoint:
    directory: ./checkpoint-folder
    create_directory: true
    timeout: 1s
    compaction:
      on_start: true
      directory: ./checkpoint-folder
      max_transaction_size: 65_536
```

**Explanation:**

- `directory: ./checkpoint-folder`: Defines the folder where checkpoint files will be stored.
- `create_directory: true`: Ensures that the directory is created if it doesn’t already exist.
- `timeout: 1s`: Specifies a timeout for file operations related to the checkpointing.
- `compaction`: Ensures that old checkpoint data is compacted periodically. The `max_transaction_size` defines the size limit for checkpoint transactions before compaction occurs.

#### 2. **Receiver Configuration (OTLP)**

The OTLP receiver will be configured to listen for telemetry data over HTTP on port `4318`.

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"
```

You could also configure additional protocols like `filelog` to receive logs from a file, but for this workshop, we focus on OTLP.

#### 3. **Exporter Configuration**

The exporter sends collected telemetry data to its destination, such as a debug exporter, a file exporter, or an OTLP gateway exporter. Let’s focus on the `otlp/gateway` exporter, where retries and queueing are configured.

```yaml
exporters:
  otlp/gateway:
    endpoint: "localhost:5317"
    tls:
      insecure: true
    retry_on_failure:
      enabled: true
    sending_queue:
      enabled: true
      num_consumers: 10
      queue_size: 10000
      storage: file_storage/checkpoint
```

**Explanation:**

- `retry_on_failure.enabled: true`: Enables retrying when there is a failure in sending data to the OTLP gateway.
- `sending_queue`: Configures an internal queue to store data that couldn’t be sent. The `storage` option links the queue to the `file_storage/checkpoint` extension, ensuring resilience even in case of network failures.
  - `num_consumers: 10`: Specifies the number of consumers reading from the queue.
  - `queue_size: 10000`: The maximum size of the queue.
  - `storage: file_storage/checkpoint`: Specifies that the queue state will be backed up in the file system.

---

### Step 3: Running the OpenTelemetry Collector with the Configuration

1. **Create Checkpoint Folder:**
   Make sure that the folder `./checkpoint-folder` exists in your working directory. The OpenTelemetry Collector will use this folder to store checkpoint and transaction files.

2. **Save the Configuration:**
   Save the YAML configuration to a file, such as `otel-collector-config.yaml`.

3. **Run the Collector:**
   Now, run the OpenTelemetry Collector using the configuration file you just created. You can do this by executing the following command in your terminal:

   ```bash
   otelcontribcol --config otel-collector-config.yaml
   ```

   This will start the collector with the configurations specified in the YAML file.

### Step 4: Testing the Resilience

To test the resilience built into the system:

1. **Simulate Network Failure:**
   Temporarily stop the OTLP receiver or shut down the endpoint where the telemetry data is being sent. You should see the retry mechanism kicking in, as the collector will attempt to resend the data.

2. **Check the Checkpoint Folder:**
   After a few retries, inspect the `./checkpoint-folder` directory. You should see checkpoint files stored there, which contain the serialized state of the queue.

3. **Restart the Collector:**
   Restart the OpenTelemetry Collector after stopping the OTLP receiver. The collector will resume sending data from the last checkpointed state, without losing any data.

4. **Inspect Logs and Files:**
   Inspect the logs to see the retry attempts. The `debug` exporter will output detailed logs, which should show retry attempts and any failures.

---

### Step 5: Fine-Tuning the Configuration for Production

- **Timeouts and Interval Adjustments:**
   You may want to adjust the `retry_on_failure` parameters for different network environments. In high-latency environments, increasing the `max_interval` might reduce unnecessary retries.

   ```yaml
   retry_on_failure:
     enabled: true
     initial_interval: 1s
     max_interval: 5s
     max_elapsed_time: 20s
   ```

- **Compaction and Transaction Size:**
   Depending on your use case, adjust the `max_transaction_size` for checkpoint compaction. A smaller transaction size will make checkpoint files more frequent but smaller, while a larger size might reduce disk I/O but require more memory.

---

### Step 6: Monitoring and Maintenance

- **Monitoring the Collector:**
   Use Prometheus or other monitoring tools to collect metrics from the OpenTelemetry Collector. You can monitor retries, the state of the sending queue, and other performance metrics to ensure the collector is behaving as expected.

- **Log Rotation:**
   The `file` exporter has a built-in log rotation mechanism to ensure that logs do not fill up your disk.

   ```yaml
   exporters:
     file:
       path: ./agent.out
       rotation:
         max_megabytes: 2
         max_backups: 2
   ```

   This configuration rotates the log file when it reaches 2 MB, and keeps up to two backups.

---

### Conclusion

In this section, you learned how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage/checkpoint` extension, setting up retry mechanisms for the OTLP exporter, and using a sending queue backed by file storage for storing data during temporary failures.

By leveraging file storage for checkpointing and queue persistence, you can ensure that your telemetry pipeline can recover gracefully from failures, making it more reliable for production environments.
