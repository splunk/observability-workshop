---
title: Test your Resilience Setup
linkTitle: 4.1 Testing the Setup
weight: 1
---

### Step 1: Setup Test environment

In this section we are going to  simulate an out age on the network and see if our configuration  helps the Collector recover from that issue:

1. **Run the Gateway**
   Now, run the OpenTelemetry Collector using the existing gateway configuration file. You can do this by executing the following command in your terminal:

   ```bash
   ../otelcol --config gateway.yaml
   ```

2. **Run the Agent**
   Next, run the OpenTelemetry Collector using the configuration file you just created. You can do this by executing the following command in your terminal:

   ```bash
   ../otelcol --config agent.yaml
   ```

   This will start the collector with the resilience configurations specified in the YAML file.

3. **Run the log-gen script**
To generate traffic, we going to start our Log generating script:  

   ```bash
   ./log-gen.sh 
   ```

### Step 2: Testing the Resilience

To test the resilience built into the system:

1. **Simulate Network Failure:**
   Temporarily stop the OTLP receiver or shut down the endpoint where the telemetry data is being sent. You should see the retry mechanism kicking in, as the collector will attempt to resend the data.

2. **Check the Checkpoint Folder:**
   After a few retries, inspect the `./checkpoint-folder` directory. You should see checkpoint files stored there, which contain the serialized state of the queue.

3. **Restart the Collector:**
   Restart the OpenTelemetry Collector after stopping the OTLP receiver. The collector will resume sending data from the last checkpointed state, without losing any data.

4. **Inspect Logs and Files:**
   Inspect the logs to see the retry attempts. The `debug` exporter will output detailed logs, which should show retry attempts and any failures.

### Conclusion

In this section, you learned how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage/checkpoint` extension, setting up retry mechanisms for the OTLP exporter, and using a sending queue backed by file storage for storing data during temporary failures.

By leveraging file storage for checkpointing and queue persistence, you can ensure that your telemetry pipeline can recover gracefully from failures, making it more reliable for  short interruptions for production environments.
