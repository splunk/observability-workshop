---
title: Building Resilience in OpenTelemetry Collector Using the File Storage Extension
linkTitle: 4. Resilience
time: 10 minutes
weight: 4
---
we will walk through how to use OpenTelemetry Collector’s `file_storage` extension to build resilience into your telemetry pipeline. Specifically, we will demonstrate how to use the file storage extension for checkpointing, managing retries, and handling temporary failures effectively.

The goal is to show how this configuration allows your OpenTelemetry Collector to reliably store intermediate states on disk, ensuring that no data is lost during network failures, and that the collector can resume where it left off.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
Note, this will only be useful if the connections fails for a short period like up to 15 minutes or so.  
If the connection is down for longer periods, the backend will drop the data anyways because the timing's are too far out of synch.

Secondly, this will works for logs, but we will introduce a more robust solution in one of the upcoming collector builds.

{{% /notice %}}

### Setup

Create a new sub directory called `4-resilience` and copy the contents from `3-filelog` across.
We are going to update the agent.yaml we have by adding an `extensions:` section.  
This new section in an OpenTelemetry configuration YAML is used to define optional components that enhance or modify the behavior of the OpenTelemetry Collector. These components don’t handle telemetry data directly but provide additional capabilities or services to the Collector.
The first exercise will be providing **Checkpointing** with the  `file_storage` extension.  
The `file_storage` extension is used to ensure that the OpenTelemetry Collector can persist checkpoints to disk. This is especially useful in cases where there are network failures or restarts. This way, the collector can recover from where it left off without losing data.
<!--
2. **Retries** with the `otlp/gateway` exporter.
3. **Queueing** with `sending_queue` and the integration of file storage for resilience.
-->

{{% notice title="Exercise" style="green" icon="running" %}}

- Add the `extensions:` key at the top of the `agent.yaml` file
  - Add the`file_storage` key and name is `/checkpoint:`
    - Add the `directory:`key and set it to a value of `"./checkpoint-folder"`
    - Add the `create_directory:` key and set it to a value of `true`
    - Add the `timeout:` key and set it to a value of `1s`
    - Add the `compaction:` key
      - Add the `on_start:` key and set it to a value of `true`
      - Add the `directory:` key and set it to a value of `./checkpoint-folder`
      - Add the `max_transaction_size:` key and set it to a value of  `65_536`

{{% /notice%}}

**Explanation:**

- `directory: ./checkpoint-folder`: Defines the folder where checkpoint files will be stored.
- `create_directory: true`: Ensures that the directory is created if it doesn’t already exist.
- `timeout: 1s`: Specifies a timeout for file operations related to the checkpointing.
- `compaction`: Ensures that old checkpoint data is compacted periodically. The `max_transaction_size` defines the size limit for checkpoint transactions before compaction occurs.

The next exercise is modifying the `otlphttp:` exporter where retries and queueing are configured.

```yaml
exporters:
  otlphttp:
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
   Save the YAML configuration to a file, such as `agent.yaml`.

3. **Run the Collector:**
   Now, run the OpenTelemetry Collector using the configuration file you just created. You can do this by executing the following command in your terminal:

   ```bash
   otelcol --config agent.yaml
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
