---
title: Test your Resilience Setup
linkTitle: 4.1 Testing the Setup
weight: 1
---
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

### Conclusion

In this section, you learned how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage/checkpoint` extension, setting up retry mechanisms for the OTLP exporter, and using a sending queue backed by file storage for storing data during temporary failures.

By leveraging file storage for checkpointing and queue persistence, you can ensure that your telemetry pipeline can recover gracefully from failures, making it more reliable for production environments.
