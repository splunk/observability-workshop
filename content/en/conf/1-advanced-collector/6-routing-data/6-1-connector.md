---
title: 6.1 Configure the Routing Connector
linkTitle: 6.1 Routing Configuration
weight: 1
---

In this exercise, you will configure the **Routing Connector** in the `gateway.yaml`. The Routing Connector can route metrics, traces, and logs based on any attributes, we will focus exclusively on trace routing based on the `deployment.environment` attribute (though any span/log/metirc attribute can be used).

{{% notice title="Exercise" style="green" icon="running" %}}

**Add new `file` exporters**: The `routing` connector requires different targets for routing. Create two new file exporters, `file/traces/route1-regular` and `file/traces/route2-security`, to ensure data is directed correctly in the `exporters` section of the `gateway.yaml`:

```yaml
  file/traces/route1-regular:                     # Exporter for regular traces
    path: "./gateway-traces-route1-regular.out"   # Path for saving trace data
    append: false                                 # Overwrite the file each time
  file/traces/route2-security:                    # Exporter for security traces
    path: "./gateway-traces-route2-security.out"  # Path for saving trace data
    append: false                                 # Overwrite the file each time 
```

**Enable Routing** by adding the `routing` connector. In OpenTelemetry configuration files, `connectors` have their own dedicated section, similar to receivers and processors.

In the **Gateway terminal** window, edit `gateway.yaml` and  find and uncomment the `#connectors:` section. Then, add the following below the `connectors:` section:

```yaml
  routing:
    default_pipelines: [traces/route1-regular]  # Default pipeline if no rule matches
    error_mode: ignore                          # Ignore errors in routing
    table:                                      # Define routing rules
      # Routes spans to a target pipeline if the resourceSpan attribute matches the rule
      - statement: route() where attributes["deployment.environment"] == "security-applications"
        pipelines: [traces/route2-security]     # Security target pipeline 
```

{{% /notice %}}

The default pipeline in the configuration file  works at a Catch all. It will be the  routing target for any data (spans in our case) that does match a rule in the routing rules table, In this table you find the pipeline that is the target for any span that matches the following rule: "[deployment.environment"] == "security-applications"


With the `routing` configuration complete, the next step is to configure the `pipelines` to apply these routing rules.
