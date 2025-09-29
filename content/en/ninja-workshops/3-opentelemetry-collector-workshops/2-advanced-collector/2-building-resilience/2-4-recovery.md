---
title: 2.4 Recovery
linkTitle: 2.4 Recovery
weight: 4
---

In this exercise, we’ll test how the **OpenTelemetry Collector** recovers from a network outage by restarting the **Gateway** collector. When the **Gateway** becomes available again, the **Agent** will resume sending data from its last check-pointed state, ensuring no data loss.

{{% notice title="Exercise" style="green" icon="running" %}}

**Restart the Gateway**: In the **Gateway terminal** window run:

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

**Restart the Agent**: In the **Agent terminal** window run:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

> After the **Agent** is up and running, the **File_Storage** extension will detect buffered data in the checkpoint folder. It will start to dequeue the stored spans from the last checkpoint folder, ensuring no data is lost.

**Verify the Agent Debug output:** Note that the **Agent** debug output does **NOT** change and still shows the following line indicating no new data is being exported:
  
  ```text
  2025-07-11T08:31:58.176Z        info    service@v0.126.0/service.go:289 Everything is ready. Begin running and processing data.   {"resource": {}}
  ```

**Watch the Gateway Debug output**  
You should see from the **Gateway** debug screen, it has started receiving the previously missed traces without requiring any additional action on your part e.g.:

  ```txt
Attributes:
     -> user.name: Str(Luke Skywalker)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
     -> payment.amount: Double(75.75)
        {"resource": {}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
  ```

**Check the `gateway-traces.out` file:**  Using `jq`, count the number of traces in the recreated `gateway-traces.out`. It should match the number you send when the **Gateway** was down.

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

{{% /notice %}}

> [!IMPORTANT]
> Stop the **Agent** and the **Gateway** processes by pressing `Ctrl-C` in their respective terminals.

### Conclusion

This exercise demonstrated how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, enabling retry mechanisms for the `otlp` exporter, and using a file-backed queue for temporary data storage.

By implementing file-based check-pointing and queue persistence, you ensure the telemetry pipeline can gracefully recover from temporary interruptions, making it a more robust and reliable for production environments.
