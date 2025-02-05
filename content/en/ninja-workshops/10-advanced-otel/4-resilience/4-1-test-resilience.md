---
title: 4.1 Test Resilience
linkTitle: 4.1 Test File Storage Extension
weight: 1
---

### Setup Test environment

In this section we are going to simulate an outage on the network between the **Agent** and the **Gateway** and see if our configuration helps the Collector recover from that issue:

{{% notice title="Exercise" style="green" icon="running" %}}

**Run the Gateway**:
Find your **Gateway** terminal window, and navigate to the `[WORKSHOP]/4-resilience` directory and restart the gateway.

It should start up normally and state : `Everything is ready. Begin running and processing data.`

**Run the Agent**:
Find your **Agent** terminal window and navigate to the `[WORKSHOP]/4-resilience` directory and restart the agent with the resilience configurations specified in the YAML file.

It should also start up normally and state : `Everything is ready. Begin running and processing data.`

**Send a Test Trace**:  
Find your `Test` terminal window and navigate to the `[WORKSHOP]/4-resilience` directory. From there, send a test trace to confirm that communication is functioning as expected.

Both the agent and gateway should display debug information, including the trace you just sent. Additionally, the gateway should generate a new `./gateway-traces.out` file.

If everything is working as expected, we can move on to testing the system’s resilience.

{{% /notice %}}

### Testing System Resilience

To evaluate the system’s resilience, we’ll simulate a scenario where the **Gateway** becomes temporarily unreachable by stopping it and observing how the system responds. First, we’ll generate traffic to the agent by sending some traces. Since the **Gateway** is down, the agent will enter retry mode.  Once we restart the agent, it will recover the traces from the persistent queue and successfully send them to the Gateway. Without the persistent queue, these traces would have been lost permanently.

{{% notice title="Exercise" style="green" icon="running" %}}
Let's start our "network failure":

**Simulate a Network Failure**:
Stop the **Gateway** with `Ctrl-C` and wait until the gateway console shows that it has stopped:

```text
2025-01-28T13:24:32.785+0100  info  service@v0.116.0/service.go:309  Shutdown complete.
```

**Create Traffic during the "Network Failure"**:  
While the **Gateway** is stopped, send 3–4 traces using the cURL command we used earlier.

Notice that the agent’s retry mechanism is activated as it continuously attempts to resend the data. In the agent’s console output, you will see repeated messages similar to the following:

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Stop the Agent**:  
Use 'Ctrl-C' to stop the agent. Wait until the agent’s console confirms it has stopped.

```text
2025-01-28T14:40:28.702+0100  info  extensions/extensions.go:66  Stopping extensions...
2025-01-28T14:40:28.702+0100  info  service@v0.116.0/service.go:309  Shutdown complete.
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Stopping the agent will halt its retry attempts and prevent any future retry activity.

If the agent runs for too long without successfully delivering data, it may begin dropping traces, depending on the retry configuration, to conserve memory. By stopping the agent, any metrics, traces, or logs currently stored in memory are lost before being dropped, ensuring they remain available for recovery.

This step is essential for clearly observing the recovery process when the agent is restarted.
{{% /notice %}}

**Simulate Network Recovery**:  
Restart the Gateway. It should initialize as expected and be ready and waiting to receive data.

**Restart the Agent**
Once the **Gateway** is up and running, restart the **Agent**. It will resume sending data from the last checkpointed state, ensuring no data is lost. You should see the **Gateway** begin receiving the previously missed traces without requiring any additional action on your part.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Note that only the **Gateway** will show that the checkpointed traces have arrived. The agent will not display any indication that data new or old has been sent.
{{% /notice %}}
{{% /notice %}}

### Conclusion

This exercise demonstrated how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, enabling retry mechanisms for the OTLP exporter, and using a file-backed queue for temporary data storage.

By implementing file-based checkpointing and queue persistence, you ensure the telemetry pipeline can gracefully recover from temporary interruptions, making it a more robust and reliable for production environments.

If you want to know more about the `FileStorage` extension, you can find it [**here**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage).

Stop the **Agent** and **Gateway** using `Ctrl-C`.
