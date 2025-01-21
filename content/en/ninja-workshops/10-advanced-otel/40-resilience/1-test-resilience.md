---
title: Test your Resilience Setup
linkTitle: 4.1 Testing the Setup
weight: 1
---

##### Setup Test environment

In this section we are going to  simulate an outage on the network and see if our configuration  helps the Collector recover from that issue:

1. **Run the Gateway**: Start the gateway. This will receive the telemetry data from the agent and forward it to the OTLP receiver.

   ```bash
   ../otelcol --config gateway.yaml
   ```

2. **Run the Agent**: Start the agent with the resilience configurations specified in the YAML file.

   ```bash
   ../otelcol --config agent.yaml
   ```

3. **Run the log-gen script**: Start the Log Generator script to generate logs and send them to the agent.

   ```bash
   ./log-gen.sh 
   ```

##### Testing the Resilience

To test the resilience built into the system:

1. **Simulate Network Failure:** Temporarily stop the OTLP receiver or shut down the endpoint where the telemetry data is being sent. You should see the retry mechanism kicking in, as the collector will attempt to resend the data.

2. **Check the Checkpoint Folder:** After a few retries, inspect the `./checkpoint-folder` directory. You should see checkpoint files stored there, which contain the serialized state of the queue.

3. **Restart the Collector:** Restart the OpenTelemetry Collector after stopping the OTLP receiver. The collector will resume sending data from the last checkpointed state, without losing any data.

4. **Inspect Logs and Files:** Inspect the logs to see the retry attempts. The `debug` exporter will output detailed logs, which should show retry attempts and any failures.

##### Conclusion

In this section, you learned how to improve the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, setting up retry mechanisms for the OTLP exporter, and using a file-backed sending queue to store data during temporary failures.

By leveraging file storage for checkpointing and queue persistence, you ensure that your telemetry pipeline can recover gracefully from short interruptions, making it more reliable for production environments.
