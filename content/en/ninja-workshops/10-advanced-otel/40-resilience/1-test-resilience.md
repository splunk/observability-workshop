---
title: Test your Resilience Setup
linkTitle: 4.1 Testing the Setup
weight: 1
---

### Setup Test environment

In this section we are going to simulate an outage on the network between the `agent` and the `gateway` and see if our configuration helps the Collector recover from that issue:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Run the Gateway**:
   Find your `Gateway` terminal window, and navigate to the `[WORKSHOP]/4-resilience` folder and start the gateway with the following command.

   ```bash
   ../otelcol --config gateway.yaml

   ```

   It should start up normally and state : `Everything is ready. Begin running and processing data.`

- **Run the Agent**:
   Find your `Agent` terminal window and navigate to the `[WORKSHOP]/4-resilience` folder and start the agent with the resilience configurations specified in the YAML file.

   ```bash
   ../otelcol --config agent.yaml
   ```

   It should also start up normally and state : `Everything is ready. Begin running and processing data.`

- **Send a Test Trace**:  
   Find your `Test` terminal window, and navigate to the `[WORKSHOP]/4-resilience` folder and start send our test trace to confirm everything is up and running, and the gateway should generate a `./gateway-traces.out` again:

{{% tabs %}}
{{% tab title="cURL Command" %}}

   ```zsh
      curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
   ```

{{% /tab %}}
{{% tab title="Debug Output Agent/Gateway" %}}

```text
   2025-01-13T13:26:13.502+0100 info Traces {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
   2025-01-13T13:26:13.502+0100 info ResourceSpans #0
   Resource SchemaURL:
   Resource attributes:
   -> service.name: Str(my.service)
   -> deployment.environment: Str(my.environment)
   -> host.name: (YOUR_HOST_NAME)
   -> os.type: Str(YOUR_OS)
   -> otelcol.service.mode: Str(gateway)
   ScopeSpans #0
   ScopeSpans SchemaURL:
   InstrumentationScope my.library 1.0.0
   InstrumentationScope attributes:
   -> my.scope.attribute: Str(some scope attribute)
   Span #0
   Trace ID       : 5b8efff798038103d269b633813fc60c
   Parent ID      : eee19b7ec3c1b173
   ID             : eee19b7ec3c1b174
   Name           : I'm a server span
   Kind           : Server
   Start time     : 2018-12-13 14:51:00 +0000 UTC
   End time       : 2018-12-13 14:51:01 +0000 UTC
   Status code    : Unset
```

{{% /tab %}}
{{% /tabs %}}

- Both the agent and gateway should display debug information, including the trace we just sent. If this is working as expected, we can proceed to test the system’s resilience.

{{% /notice %}}

### Testing System Resilience

To evaluate the system's resilience, we'll simulate a scenario where the Gateway is temporarily unreachable and observe the system's behavior.

1. **Verify Data Flow to the Gateway**
   Ensure that data is successfully flowing into the Gateway. Open the Gateway's Debug screen and confirm that it displays data from the test trace.

2. **Simulate a Network Failure**
   - Temporarily stop the Gateway.
   - While the Gateway is stopped, send 3–4 traces using the `cURL` command.
   - Observe the agent's retry mechanism as it attempts to resend the data.

3. **Inspect the Checkpoint Folder**
   - After several retries, check the `./checkpoint-folder` directory.
   - Confirm that checkpoint files are created and stored there, representing the serialized state of the data queue.

4. **Stop the Agent**
   Stop the agent to halt its retry attempts. This will help in clearly observing the recovery process.

5. **Restart the Gateway**
   Start the Gateway again. It should initialize normally and be ready to receive data.

6. **Restart the Agent**
   When you restart the OpenTelemetry Agent, it should resume sending data from the last checkpointed state. This ensures no data loss, which should be visible on the Gateway as it begins receiving the previously missed traces.

---

### Conclusion

This exercise demonstrated how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, enabling retry mechanisms for the OTLP exporter, and using a file-backed queue for temporary data storage.

By implementing file-based checkpointing and queue persistence, you ensure the telemetry pipeline can gracefully recover from temporary interruptions, making it more robust and reliable for production environments.
