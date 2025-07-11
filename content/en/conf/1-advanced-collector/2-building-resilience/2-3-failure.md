---
title: 2.3 Simulate Failure
linkTitle: 2.3 Simulate Failure
weight: 3
---

To assess the **Agent's** resilience, we'll simulate a temporary **Gateway** outage and observe how the **Agent** handles it:

{{% notice title="Exercise" style="green" icon="running" %}}

**Simulate a network failure**: In the **Gateway terminal** stop the **Gateway** with `Ctrl-C` and wait until the gateway console shows that it has stopped. The **Agent** will continue running, but it will not be able to send data to the gateway. The output in the **Gateway terminal** should look similar to this:

```text
2025-07-09T10:22:37.941Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

**Send traces**: In the **Loadgen terminal** window send five more traces using the `loadgen`.

```bash { title="Start Load Generator" }
../loadgen -count 5
```

Notice that the agent’s retry mechanism is activated as it continuously attempts to resend the data. In the agent’s console output, you will see repeated messages similar to the following:

```text
2025-01-28T14:22:47.020+0100  info  internal/retry_sender.go:126  Exporting failed. Will retry the request after interval.  {"kind": "exporter", "data_type": "traces", "name": "otlphttp", "error": "failed to make an HTTP request: Post \"http://localhost:5318/v1/traces\": dial tcp 127.0.0.1:5318: connect: connection refused", "interval": "9.471474933s"}
```

**Stop the Agent**: In the **Agent terminal** window, use `Ctrl-C` to stop the agent. Wait until the agent’s console confirms it has stopped:

```text
2025-07-09T10:25:59.344Z        info    service@v0.126.0/service.go:345 Shutdown complete.      {"resource": {}}
```

{{% /notice %}}

When you stop the agent, any metrics, traces, or logs held in memory for retry will be lost. However, because we have configured the FileStorage Extension, all telemetry that has not yet been accepted by the target endpoint are safely checkpointed on disk. 

Stopping the agent is a crucial step to clearly demonstrate how the system recovers when the agent is restarted.
