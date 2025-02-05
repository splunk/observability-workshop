---
title: 8.1 Configuring the Routing Connector
linkTitle: 8.1 Routing Configuration
weight: 1
---

In the following exercise, you will configure the `routing` connector in the `gateway.yaml` file. This setup will enable the **Gateway** to route traces based on the `deployment.environment` attribute in the spans you send. By doing so, you can process and handle traces differently depending on their attributes.

{{% notice title="Exercise" style="green" icon="running" %}}
Open the `gateway.yaml` and add the following configuration:

- **Add the `routing` connector**: In OpenTelemetry configuration files, `connectors` have their own dedicated section, similar to receivers and processors in the `gateway.yaml` file. This same approach can also be applied to `metrics` and `logs`, allowing you to route them based on attributes in `resourceMetrics` or `resourceLogs` similarly.
  
  Add the following below the `receivers:` section and above the `processors:` section:

  ```yaml
  connectors:
    routing:
      default_pipelines: [traces/standard] # Default pipeline to use if no matching rule
      error_mode: ignore                   # Ignore errors in the routing 
      table:                               # Array with routing rules
        # Connector will route any span to target pipeline if if the resourceSpn attribute matches this rule 
        - statement: route() where attributes["deployment.environment"] == "security_applications"
          pipelines: [traces/security]     # Target pipeline 
  ```

- **Configure two `file:` Exporters**:
The `routing` connector requires different targets for routing. Add a second and third file exporter called `file/traces/security:` and `file/traces/standard:` respectively. This will allow the routing connector to direct data to the appropriate target based on the rules you define:

  ```yaml
    file/traces/standard:              # Exporter Type/Name (For regular traces)
      # Path where trace data will be saved in OTLP json format 
      path: "./gateway-traces-standard.out" 
      append: false    # Overwrite the file each time
    file/traces/security:              # Exporter Type/Name (For security traces)
      # Path where trace data will be saved in OTLP json format
      path: "./gateway-traces-security.out" 
      append: false                    # Overwrite the file each time 
  ```

{{% /notice %}}

With the `routing` configuration complete, next we configure the `pipelines` to use the routing rules.
