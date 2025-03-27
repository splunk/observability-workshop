---
title: 4.4 Recovery
linkTitle: 4.4 Recovery
weight: 4
---

In this exercise, we’ll test how the **OpenTelemetry Collector** recovers from a network outage by restarting the **Gateway** collector. When the `gateway` becomes available again, the `agent` will resume sending data from its last checkpointed state, ensuring no data loss.

{{% notice title="Exercise" style="green" icon="running" %}}

**Restart the Gateway**: In the **Gateway terminal** window run:

```bash {title="Gateway"}
../otelcol --config=gateway.yaml
```

**Restart the Agent**: In the **Agent terminal** window run:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

{{% /notice %}}

After the `agent` is up and running, the **File_Storage** extension will detect buffered data in the checkpoint folder.  
It will start to dequeue the stored spans from the last checkpoint folder, ensuring no data is lost.

{{% notice title="Exercise" style="green" icon="running" %}}

**Verify the Agent Debug output**  
Note that the Agent Debug Screen does **NOT** change and still shows the following line indicating no new data is being exported.
  
  ```text
  2025-02-07T13:40:12.195+0100    info    service@v0.120.0/service.go:253 Everything is ready. Begin running and processing data.
  ```

**Watch the Gateway Debug output**  
You should see from the `gateway` debug screen, it has started receiving the previously missed traces without requiring any additional action on your part.  

  ```txt
  2025-02-07T12:44:32.651+0100    info    service@v0.120.0/service.go:253 Everything is ready. Begin running and processing data.
  2025-02-07T12:47:46.721+0100    info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 4, "spans": 4}
  2025-02-07T12:47:46.721+0100    info    ResourceSpans #0
  Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
  Resource attributes:
  ```

**Check the `gateway-traces.out` file**  
Using `jq`, count the number of traces in the recreated `gateway-traces.out`. It should match the number you send when the `gateway` was down.

{{% tabs %}}
{{% tab title="Check Gateway Traces Out File" %}}

```bash
jq '.resourceSpans | length | "\(.) resourceSpans found"' gateway-traces.out
```

{{% /tab %}}

{{% tab title="Example output" %}}

```text
"5 resourceSpans found"
```

{{% /tab %}}
{{% /tabs %}}

> [!IMPORTANT]
> Stop the `agent` and the `gateway` processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}

### Conclusion

This exercise demonstrated how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, enabling retry mechanisms for the `otlp` exporter, and using a file-backed queue for temporary data storage.

By implementing file-based checkpointing and queue persistence, you ensure the telemetry pipeline can gracefully recover from temporary interruptions, making it a more robust and reliable for production environments.
