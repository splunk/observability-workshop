---
title: Test your Resilience Setup
linkTitle: 4.1 Testing the Setup
weight: 1
---

##### Setup Test environment

In this section we are going to simulate an outage on the network between teh `agent` and the `gateway` and see if our configuration helps the Collector recover from that issue:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Run the Gateway**:  
   Find your `Gateway` terminal window, and navigate to the `[WORKSHOP]/4-resilience` folder and start the gateway with the following command.

   ```bash
   ../otelcol --config gateway.yaml

   ```

   It should start up normally and state : `Everything is ready. Begin running and processing data.`

- **Run the Agent**:   
   Find your `Agent` terminal window, and navigate to the `[WORKSHOP]/4-resilience` folder and start the agent with the resilience configurations specified in the YAML file.

   ```bash
   ../otelcol --config agent.yaml
   ```

   It should also start up normally and state : `Everything is ready. Begin running and processing data.`

- **Send a Test Trace**:  
   Find your `Test` terminal window, and navigate to the `[WORKSHOP]/4-resilience` folder and start send our test trace to confirm everything is up and running and the gateway should generate an `./gateway-traces.out` again:

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

{{%/notice%}}

##### Testing the Resilience

To test the resilience built into the system we are going to send traces and see what happens if the Gateway iis unreachable.

1. **Make sure data is flowing across into the Gateway** Make sure the Debug screen of the gateway shows incoming traffic like:

1. **Simulate Network Failure:** Temporarily stop the Gateway.  
Now send  3 of 4 tracves wiht teh Cutl command. You should see the retry mechanism kicking in on the agent side , as the collector will attempt to resend the data.

2. **Check the Checkpoint Folder:** After a few retries, inspect the `./checkpoint-folder` directory. You should see checkpoint files stored there, which contain the serialized state of the queue.

3. **Restart the Agent:** Restart the OpenTelemetry Agent.  The collector will resume sending data from the last checkpointed state, without losing any data.

##### Conclusion

In this section, you learned how to improve the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, setting up retry mechanisms for the OTLP exporter, and using a file-backed sending queue to store data during temporary failures.

By leveraging file storage for checkpointing and queue persistence, you ensure that your telemetry pipeline can recover gracefully from short interruptions, making it more reliable for production environments.
