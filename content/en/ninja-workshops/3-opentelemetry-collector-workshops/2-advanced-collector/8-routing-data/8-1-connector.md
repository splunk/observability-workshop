---
title: 8.1 Configure the Routing Connector
linkTitle: 8.1 Routing Configuration
weight: 1
---

In this exercise, you will configure the **Routing Connector** in the `gateway.yaml` file. This setup enables the `gateway` to route traces based on the `deployment.environment` attribute in the spans you send. By implementing this, you can process and handle traces differently depending on their attributes.

{{% notice title="Exercise" style="green" icon="running" %}}

In OpenTelemetry configuration files, `connectors` have their own dedicated section, similar to receivers and processors.

**Add the `routing` connector**:
In the **Gateway terminal** window edit `gateway.yaml` and add the following below the `connectors:` section:

```yaml
  routing:
    default_pipelines: [traces/standard] # Default pipeline if no rule matches
    error_mode: ignore                   # Ignore errors in routing
    table:                               # Define routing rules
      # Routes spans to a target pipeline if the resourceSpan attribute matches the rule
      - statement: route() where attributes["deployment.environment"] == "security-applications"
        pipelines: [traces/security]     # Target pipeline 
```

The rules above apply to traces, but this approach also applies to `metrics` and `logs`, allowing them to be routed based on attributes in `resourceMetrics` or `resourceLogs`.

**Configure `file:` exporters**: The `routing` connector requires separate targets for routing. Add two file exporters, `file/traces/security` and `file/traces/standard`, to ensure data is directed correctly.

```yaml
  file/traces/standard:                    # Exporter for regular traces
    path: "./gateway-traces-standard.out"  # Path for saving trace data
    append: false                          # Overwrite the file each time
  file/traces/security:                    # Exporter for security traces
    path: "./gateway-traces-security.out"  # Path for saving trace data
    append: false                          # Overwrite the file each time 
```

{{% /notice %}}

With the `routing` configuration complete, the next step is to configure the `pipelines` to apply these routing rules.
