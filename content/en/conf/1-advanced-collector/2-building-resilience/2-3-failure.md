---
title: 2.3 Simulate Failure
linkTitle: 2.3 Simulate Failure
weight: 3
---

To assess the **Agent's** resilience, we'll simulate a temporary **Gateway** outage and observe how the **Agent** handles it:

**Summary**:

1. **Send Traces to the Agent** – Generate traffic by sending traces to the **Agent**.
2. **Stop the Gateway** – This will trigger the **Agent** to enter retry mode.
3. **Restart the Gateway** – The **Agent** will recover traces from its persistent queue and forward them successfully. Without the persistent queue, these traces would have been lost permanently.

{{% notice title="Exercise" style="green" icon="running" %}}

**Simulate a network failure**: In the **Gateway terminal** stop the **Gateway** with `Ctrl-C` and wait until the gateway console shows that it has stopped:

```text
2025-01-28T13:24:32.785+0100  info  service@v0.120.0/service.go:309  Shutdown complete.
```

**Send traces**: In the **Spans terminal** window send five more traces using the `loadgen`.

Notice that the agent’s retry mechanism is activated as it continuously attempts to resend the data. In the agent’s console output, you will see repeated messages similar to the following:

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Stop the Agent**: In the **Agent terminal** window, use `Ctrl-C` to stop the agent. Wait until the agent’s console confirms it has stopped:

```text
2025-01-28T14:40:28.702+0100  info  extensions/extensions.go:66  Stopping extensions...
2025-01-28T14:40:28.702+0100  info  service@v0.120.0/service.go:309  Shutdown complete.
```

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Stopping the agent will halt its retry attempts and prevent any future retry activity.

If the agent runs for too long without successfully delivering data, it may begin dropping traces, depending on the retry configuration, to conserve memory. By stopping the agent, any metrics, traces, or logs currently stored in memory are lost before being dropped, ensuring they remain available for recovery.

This step is essential for clearly observing the recovery process when the agent is restarted.
{{% /notice %}}
