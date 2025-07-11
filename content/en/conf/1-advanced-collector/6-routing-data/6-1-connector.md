---
title: 6.1 Configure the Routing Connector
linkTitle: 6.1 Routing Configuration
weight: 1
---

In this exercise, you will configure the **Routing Connector** in the `gateway.yaml`. While the Routing Connector can route metrics, traces, and logs based on any attributes, we will focus exclusively on trace routing.

This setup enables the Gateway to route traces based on the `deployment.environment` attribute (though any span attribute can be used).

{{% notice title="Exercise" style="green" icon="running" %}}

**Configure `file` exporters**: The `routing` connector requires separate targets for routing. Create two new file exporters, `file/traces/route1` and `file/traces/route2`, to ensure data is directed correctly in the `exporters` section of the `gateway.yaml`:

```yaml
  file/traces/route1:                    # Exporter for regular traces
    path: "./gateway-traces-route1.out"  # Path for saving trace data
    append: false                        # Overwrite the file each time
  file/traces/route2:                    # Exporter for security traces
    path: "./gateway-traces-route2.out"  # Path for saving trace data
    append: false                        # Overwrite the file each time 
```

In OpenTelemetry configuration files, `connectors` have their own dedicated section, similar to receivers and processors.

**Add the `routing` connector**:
In the **Gateway terminal** window, edit `gateway.yaml` and uncomment the `#connectors:` section. Then, add the following below the `connectors:` section:

```yaml
  routing:
    default_pipelines: [traces/route1]   # Default pipeline if no rule matches
    error_mode: ignore                   # Ignore errors in routing
    table:                               # Define routing rules
      # Routes spans to a target pipeline if the resourceSpan attribute matches the rule
      - statement: route() where attributes["deployment.environment"] == "security-applications"
        pipelines: [traces/route2]       # Target pipeline 
```

{{% /notice %}}

With the `routing` configuration complete, the next step is to configure the `pipelines` to apply these routing rules.
