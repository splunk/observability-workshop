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

{{% /tab %}}

Open the `gateway.yaml` and add the following configuration:

{{% notice title="Exercise" style="green" icon="running" %}}

In this exercise, you will configure the `routing connector` in the `gateway.yaml` file. This setup will enable the `gateway` to route traces based on the `deployment.environment` attribute in the spans you send. By doing so, you can process and handle traces differently depending on their attributes.

- **Add the `connectors:` section**:  
In OpenTelemetry configuration files, `connectors` have their own dedicated section, similar to receivers and processors. In the `gateway.yaml`file, insert the `connectors:` section below the receivers section and above the processors section.

  ```yaml
  connectors:       # Section to configure connectors

  processors:
    #memory_limiter:

  ```

- **Add the `routing` connector**:  
We are setting up a `resourceSpans` attribute rule. In this configuration, spans will be routed if the `deployment.environment` resourceSpan attribute matches `"security_applications"`.  
This same approach can also be applied to `metrics` and `logs`, allowing you to route them based on attributes in `resourceMetrics` or `resourceLogs` in a similar way. Add the following under the `connectors:` section:

  ```yaml
    routing:
      default_pipelines: [traces/standard] # Default pipeline to use if no matching rule
      error_mode: ignore                   # Ignore errors in the routing 
      table:                               # Array with routing rules
        # Connector will route any span to target pipeline if if the resourceSpn attribute matches this rule 
        - statement: route() where attributes["deployment.environment"] == "security_applications"
          pipelines: [traces/security]     # Target pipeline 
  ```

- **Configure two `file:` Exporters**:
The `routing connector` requires different targets for routing. To achieve this, update the default `file/traces:` exporter and name it `file/traces/default` and add a second file exporter called `file/traces/security:`. This will allow the routing connector to direct data to the appropriate target based on the rules you define.

  ```yaml
    file/traces/default:               # Exporter Type/Name (For regular traces)
      # Path where trace data will be saved in OTLP json format 
      path: "./gateway-traces-default.out" 
      append: false    # Overwrite the file each time
    file/traces/security:              # Exporter Type/Name (For security traces)
      # Path where trace data will be saved in OTLP json format
      path: "./gateway-traces-security.out" 
      append: false                    # Overwrite the file each time 
  ```

- **Add both the `standard` and `security traces` pipelines**:
To enable routing we need to define two pipelines for traces:

  1. **Standard** pipeline.  
  This pipeline will handle all spans that do not match the routing rule. Add it below the regular `traces:` pipeline, and leave the configuration unchanged for now.

  ```yaml
    pipelines:
      #traces:               
      traces/standard:         # Array of Trace Receivers
        receivers: [routing]   # Only receives spans from the routing connector 
        processors:
        - memory_limiter
        - batch
        - resource/add_mode
        exporters: [file/traces/default] # Location for spans not matching rule
  ```

  - The Target pipeline, that will handle all spans that match the routing rule.

  ```yaml
    pipelines:
      #traces:                 
      #traces/standard:         
      traces/security:         # Array of Trace Receivers
        receivers: [routing]   # Only receives spans from the routing connector 
        processors:
        - memory_limiter
        - batch
        - resource/add_mode
        exporters: [file/traces/security] # Location for spans matching rule
      #metrics:  
  ```

- **Update the `traces` pipeline to handle routing**:  
To enable `routing`, you need to update the original `traces` pipeline by adding `routing` as an exporter. This will send your span data through the `routing connector` for evaluation.

```yaml
  pipelines:
    traces:                       # Original traces pipeline
      receivers: [otlp]           # Array of Trace Receivers
      exporters: [routing, debug] # Array of Trace exporters
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

Keep in mind that any existing processors have been removed from this pipeline. They are now handled by either the standard pipeline or the target pipelines, depending on the routing rules.
{{% /notice %}}

- **Create a trace for different Environments**
To test your configuration, you’ll need to generate some trace data that includes a span named

Copy the following JSON and save to a file called security.json in the 8-routing directory:

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"password_check"}},{"key":"deployment.environment","value":{"stringValue":"security_applications"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"I'm a server span","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[{"keytest":"my.span.attr","value":{"stringValue":"some value"}}]}]}]}]}
```

{{% /tab %}}
{{% tab title="Formatted JSON" %}}

```json
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": {
              "stringValue": "password_check"
            }
          },
          {
            "key": "deployment.environment",
            "value": {
              "stringValue": "security_applications"
            }
          }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "my.library",
            "version": "1.0.0",
            "attributes": [
              {
                "key": "my.scope.attribute",
                "value": {
                  "stringValue": "some scope attribute"
                }
              }
            ]
          },
          "spans": [
            {
              "traceId": "5B8EFFF798038103D269B633813FC60C",
              "spanId": "EEE19B7EC3C1B174",
              "parentSpanId": "EEE19B7EC3C1B173",
              "name": "I'm a server span",
              "startTimeUnixNano": "1544712660000000000",
              "endTimeUnixNano": "1544712661000000000",
              "kind": 2,
              "attributes": [
                {
                  "keytest": "my.span.attr",
                  "value": {
                    "stringValue": "some value"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

Save the security.json file.

{{% /notice %}}

![Routing Processor](../images/routing.png)

Lets' test our configuration!
