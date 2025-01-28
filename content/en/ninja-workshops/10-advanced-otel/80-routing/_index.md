---
title: Routing
linkTitle: 8. Routing
time: 10 minutes
weight: 8
---

The routing connector in OpenTelemetry is a powerful feature that allows you to direct data (`traces`, `metrics`, or l`ogs`) to different pipelines based on specific criteria. This is especially useful in scenarios where you want to apply different processing or exporting logic to subsets of your telemetry data.

For example, you might want to send *production* data to one exporter while directing *test* or *development* data to another. Similarly, you could route certain spans based on their attributes, such as service name, environment, or span name, to apply custom processing or storage logic.

### Setup

In the `[WORKSHOP]` directory create a new subdirectory called `8-routing`, then copy `*.yaml`, `*.json` and your `log-gen` script from the `7-transform-data` folder.

{{% tab title="Initial Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
├── 6-sensitive-data
├── 7-transform-data
├── 8-routing
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── log-gen.sh (or .ps1)
│   ├── health.json
│   └── trace.json
└── otelcol
```

{{%/tab%}}

Open the `gateway.yaml` and add the following configuration:

{{% notice title="Exercise" style="green" icon="running" %}}

In this exercise, you will configure the `routing connector` in the `gateway.yaml` file. This setup will enable the `gateway` to route traces based on the `deployment.environment` attribute in the spans you send. By doing so, you can process and handle traces differently depending on their attributes.

- **Configure two `file:` Exporters**:
The `routing connector` requires different targets for routing. To achieve this, update the default `file/traces:` exporter and add a second file exporter called `file/security:`. This will allow the routing connector to direct data to the appropriate target based on the rules you define.

  ```yaml
    file/traces:                       # Exporter Type/Name
      path: "./gateway-traces-default.out"     # Path where trace data will be saved in OTLP json format
      append: false                    # Overwrite the file each time
    file/security:                     # Exporter Type/Name
    path: "./gateway-traces-security.out"     # Path where trace data will be saved in OTLP json format
      append: false                    # Overwrite the file each time
  ```

- **Add the `connectors:` section**:  
In OpenTelemetry configuration files, `connectors` have their own dedicated section, similar to receivers and processors. In the `gateway.yaml`file, insert the `connectors:` section below the receivers section and above the processors section.

  ```yaml
  connectors:       # Section to configure connectors

  processors:
    #memory_limiter:

  ```

- **Add the `routing` connector**:  
We are setting up a `resourceSpans` attribute rule. In this configuration, spans will be routed if the `deployment.environment` resourceSpan attribute matches `"security_applications"`.  
This approach can also be applied to `metrics` and `logs`, allowing you to route them based on attributes in `resourceMetrics` or `resourceLogs` in a similar manner.

  ```yaml
  routing:
      default_pipelines: [traces/standard] # Default pipeline to use if no matching rule
      error_mode: ignore                   # Ignore errors in the routing 
      table:                               # Array with routing rules
        # Connector will route any span to target pipeline if if the resourceSpn attribute matches this rule 
        - statement: route() where attributes["deployment.environment"] == "security_applications"
          pipelines: [traces/security]     # Target pipeline 
  ```

- **Add both the `standard` and `security traces` pipelines**:  
To enable routing we need to define two pipeline for traces:  

  1. **Standard** pipeline.  
  This pipeline will handle all spans that do not match the routing rule. Add it below the regular `traces:` pipeline, and leave the configuration unchanged for now.

  ```yaml
    pipelines:
      #traces:                 # Original traces pipeline
      traces/standard:         # Array of Trace Receivers
        receivers: [routing]   # Only receives spans from the routing connector 
        processors:
        - memory_limiter
        - batch
        - resourcedetection
        - resource/add_mode
        exporters: [file/standard] # Location for spans not matching rule
  ```

  - The Target pipeline, that will handle all spans that match the routing rule.

  ```yaml
    pipelines:
      #traces:                 # Original traces pipeline
      #traces/standard:         
      traces/security:         # Array of Trace Receivers
        receivers: [routing]   # Only receives spans from the routing connector 
        processors:
        - memory_limiter
        - batch
        - resourcedetection
        - resource/add_mode
        exporters: [file/security] # Location for spans matching rule
  ```

- **Update the `traces` pipeline to handle routing**:  
To enable `routing`, you need to update the original `traces` pipeline by adding `routing` as an exporter. This will send your span data through the `routing connector` for evaluation.

```yaml
  pipelines:
   traces:                        # Original traces pipeline
      receivers: [otlp]           # Array of Trace Receivers
      exporters: [routing, debug] # Array of Trace exporters
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

Keep in mind that any existing processors have been removed from this pipeline. They are now handled by either the standard pipeline or the target pipelines, depending on the routing rules.
{{% /notice %}}

{{%/notice%}}
 
![Routing Processor](../images/routing.png)

Lets' test our configuration