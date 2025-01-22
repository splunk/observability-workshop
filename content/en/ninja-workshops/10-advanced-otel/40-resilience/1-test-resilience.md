---
title: Test your Resilience Setup
linkTitle: 4.1 Testing the Setup
weight: 1
---

##### Setup Test environment

In this section we are going to  simulate an outage on the network and see if our configuration  helps the Collector recover from that issue:

1. **Run the Gateway**: Start the gateway. This will receive the telemetry data from the agent and forward it to the relevant .out file.

   ```bash
   ../otelcol --config gateway.yaml
   ```

2. **Run the Agent**: Start the agent with the resilience configurations specified in the YAML file.

   ```bash
   ../otelcol --config agent.yaml
   ```

At this point, the inital 
3. **Run the log-gen script**: Start the Log Generator script to generate logs and send them to the agent.

{{% tabs %}}
{{% tab title="Mac/Linux command" %}}

```bash
   ./log-gen.sh 
```

{{% /tab %}}
{{% tab title="Windows command" %}}

```bash
   ./log-gen.ps1 
```

{{% /tab %}}
{{% /tabs %}}

##### Testing the Resilience

To test the resilience built into the system:

1. **Make sure data is flowing across into the Gateway** Make sure the Debug screen of the gateway shows incoming traffic like:

```text
2025-01-18T21:25:01.806+0100    info    ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> com.splunk/source: Str(./quotes.log)
     -> host.name: (YOUR_HOST_NAME)
     -> os.type: Str(YOUR_OS)
     -> otelcol.service.mode: Str(agent)
ScopeLogs #0
ScopeLogs SchemaURL:
InstrumentationScope
LogRecord #0
ObservedTimestamp: 2025-01-18 20:25:01.7201606 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str(2025-01-18 21:25:01 [WARN] - Do or do not, there is no try.)
Attributes:
     -> log.file.path: Str(quotes.log)
Trace ID:
Span ID:
Flags: 0
        {"kind": "exporter", "data_type": "logs", "name": "debug"}
```

2. **Simulate Network Failure:** Temporarily stop the Gateway You should see the retry mechanism kicking in on the agent side , as the collector will attempt to resend the data.

2. **Check the Checkpoint Folder:** After a few retries, inspect the `./checkpoint-folder` directory. You should see checkpoint files stored there, which contain the serialized state of the queue.

4. **Stop the Log generating script**  Select the shell and use  `Command-c/Ctrl-c`.  This way... no new data is being handled by the agent if and when  the recovery 

3. **Restart the Agent:** Restart the OpenTelemetry Agent.  The collector will resume sending data from the last checkpointed state, without losing any data.



##### Conclusion

In this section, you learned how to improve the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, setting up retry mechanisms for the OTLP exporter, and using a file-backed sending queue to store data during temporary failures.

By leveraging file storage for checkpointing and queue persistence, you ensure that your telemetry pipeline can recover gracefully from short interruptions, making it more reliable for production environments.
