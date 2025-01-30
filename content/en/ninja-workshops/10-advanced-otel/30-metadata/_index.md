---
title: Adding Resource Metadata
linkTitle: 3. Resource Metadata
weight: 3
---

So far, we’ve essentially exported a direct copy of the `span` sent through the OpenTelemetry Collector. Now, let’s enhance the base `span` by adding metadata using `processors`. This additional information can be valuable for troubleshooting and for enabling features like `Related Content`.

{{% notice title="Exercise" style="green" icon="running" %}}
We will enhance the data flowing through our pipelines by making the following changes to the `agent.yaml`:  

- **Add the `resourcedetection` Processor**: The [**Resource Detection Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md) can be used to detect resource information from the host and append or override the resource value in telemetry data with this information.

  ```yaml
    # Processor Type
    resourcedetection:
      # Array of resource detectors (e.g., system, cloud providers)
      detectors: [system]
      # Overwrites existing attributes in the data
      override: true
  ```

- **Add `resource` Processor (`add_mode`)**: The Resource Processor can be used to apply changes on resource attributes.

  ```yaml
    resource/add_mode:             # Processor Type/Name
      attributes:                  # Array of attributes and modifications
      - action: insert             # Action is to insert a key
        key: otelcol.service.mode  # Key name
        value: "agent"             # Key value
  ```

- **Update All Pipelines**: Add both processors (`resourcedetection` and `resource/add_mode`) to the `processors` array in **all pipelines** (traces, metrics, and logs). Ensure `memory_limiter` remains the first processor.

  ```yaml
    traces:                     # Traces Pipeline
      receivers: [otlp]         # Array of trace receivers
      processors:               # Array of trace processors
        - memory_limiter        # Handles memory limits for this pipeline
        - resourcedetection     # Adds system attributes to the data
        - resource/add_mode     # Adds collector mode metadata
      exporters: [debug, file]  # Array of trace exporters
    #metrics:
    #logs:
  ```

{{% /notice %}}

By adding these processors, we enrich the data with system metadata and the agent’s operational mode, which aids in troubleshooting and provides useful context for related content.

Validate your updated `agent.yaml` with [**otelbin.io**](https://www.otelbin.io/):

![otelbin-a-1-3-logs](../images/agent-1-3-logs.png?width=50vw)
