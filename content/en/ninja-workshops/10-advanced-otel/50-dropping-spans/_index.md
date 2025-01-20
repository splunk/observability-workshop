---
title: Using a Filter to Drop Spans in OpenTelemetry Collector
linkTitle: 5. Dropping Spans
time: 10 minutes
weight: 5
---

In this section, we will explore how to use the filter processor in the OpenTelemetry Collector to selectively drop spans based on certain conditions. Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces.

By the end of this workshop, you'll know how to configure the OpenTelemetry Collector to:

Filter out unwanted spans.

- Use the filter processor to drop spans based on span names.
- Understand and customize error handling in the filter processor.

Overview of the Configuration
The main processor we'll be working with in this workshop is the filter processor. The filter processor allows you to filter out telemetry data (traces, metrics, logs) based on conditions like span names, attributes, or other criteria. This is useful in scenarios where you want to remove noise (such as health check requests) or prevent processing of unimportant traces.

Key Configuration Overview:
Here’s the key section of the YAML configuration that defines the filter processor:

```yaml
processors:
  batch:
    metadata_keys:
      - X-SF-Token

  memory_limiter:
    check_interval: 2s
    limit_mib: 512

  resource/add_mode:
    attributes:
      - action: upsert
        value: "gateway"
        key: otelcol.service.mode

  filter:
    error_mode: ignore
    traces:
      span:
        - 'name == "/_healthz"'
```

Filter Processor: The filter processor is the core of this workshop. It is configured to drop spans based on a specific condition. In this case, we are filtering out spans whose name is "/_healthz", typically associated with health check requests.

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'name == "/_healthz"'
```

- error_mode: ignore: When the filter processor encounters an error in its configuration or processing, it will ignore it and continue processing other traces.
- traces: This section defines the conditions for filtering traces.
- span: We specify that we want to drop spans with the name "/_healthz", which is common for health check requests in microservices.

### Step 1: Review the YAML Configuration

First, we’ll take a closer look at the YAML configuration used in the OpenTelemetry Collector. This configuration defines how we process and filter telemetry data:

yaml
Copy
processors:
  batch:
    metadata_keys:
      - X-SF-Token

  memory_limiter:
    check_interval: 2s
    limit_mib: 512

  resource/add_mode:
    attributes:
      - action: upsert
        value: "gateway"
        key: otelcol.service.mode

  filter:
    error_mode: ignore
    traces:
      span:
        - 'name == "/_healthz"'

### Step 2: Apply the Configuration

#### 2.1 Save the Configuration

Save the above YAML configuration to a file called otel-collector-config.yaml.

#### 2.2 Run the OpenTelemetry Collector

Now, start the OpenTelemetry Collector with your configuration:

```bash
otelcol --config=otel-collector-config.yaml
```

This will launch the OpenTelemetry Collector and apply your filter configuration to incoming telemetry data.

### Step 3: Simulate Trace Data

#### 3.1 Send Sample Data to the Collector

To test your configuration, you'll need to generate some trace data that includes a span named "/_healthz". This is typically seen in health check requests that many services send to verify their status.

You can use an instrumented application to generate trace data with the span name "/_healthz".
Alternatively, you can simulate trace data manually if you're using a test environment.
Ensure that you send some traces with the span name "/_healthz" to confirm that they are filtered out.

#### 3.2 Observe the Filter in Action

Once the data is sent, the OpenTelemetry Collector should process it and drop any spans with the name "/_healthz". You can confirm this by checking the trace data in the destination where it is exported (e.g., Jaeger, Zipkin, or any other trace backend).

Expected Outcome:

- Traces with the span name "/_healthz" should not appear in the exported trace data.
- Other spans should be processed normally and appear in the backend.

### Step 4: Monitor and Debug the Filter Processor

#### 4.1 Error Mode Handling

If the filter processor encounters any issues, the error_mode: ignore setting will ensure that the processing continues even if there's an error. However, it’s useful to set up logging and monitoring to ensure that the filter configuration is working as expected.

For example, check the logs of the OpenTelemetry Collector for messages related to trace filtering.

#### 4.2 Debugging Your Filter Configuration

If the filter isn’t working as expected, ensure that:

The span names are correctly matched.
The filter condition is correctly specified in the YAML file.
You can also adjust the log verbosity of the OpenTelemetry Collector to get more insight into its operations.

### Step 5: Customize the Filter

#### 5.1 Modify the Filter Condition

You can customize the filter condition to drop spans based on other criteria. For example, you might want to drop spans that have a specific tag or attribute.

Example of dropping spans based on an attribute:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'attributes["deployment.environment"] == "testing"'
```

This filter would drop spans where the deployment.environment attribute is set to "testing".

#### 5.2 Filter Multiple Spans

You can filter out multiple span names by extending the span list:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'name == "/_healthz"'
      - 'name == "/internal/metrics"'
```

This will drop spans with the names "/_healthz" and "/internal/metrics".

### Conclusion

Congratulations! You have successfully configured the OpenTelemetry Collector to filter and drop unwanted spans. This configuration allows you to ignore internal or irrelevant traces, such as health check requests, which can help reduce noise in your telemetry data.

You can further extend this configuration to filter out spans based on different attributes, tags, or other criteria, making the OpenTelemetry Collector more customizable and efficient for your observability needs.

Feel free to experiment with different filter conditions and explore the other processor types available in OpenTelemetry to enhance your observability pipeline.

### Next Steps

- **Extend Filtering**: Add more filtering conditions based on span attributes or other metadata.
- **Explore More Processors**: Learn about other processors like attributes, batch, or memory_limiter for more advanced use cases.
- **Integrate with Backends**: Try integrating this filtered data with a backend like Jaeger, Prometheus, or any other observability platform.
