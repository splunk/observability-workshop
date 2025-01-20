---
title: Using the OpenTelemetry Transform Processor
linkTitle: 7. Transform Data
time: 10 minutes
weight: 7
---

In this workshop, we will explore the **Transform Processor** in the OpenTelemetry Collector. This processor allows you to modify trace, metric, and log data at runtime by performing actions like adding, updating, or deleting attributes. It’s a powerful tool to reshape telemetry data before it is exported to the backend.

By the end of this workshop, you will learn how to:

- Use the **Transform Processor** to modify trace data.
- Apply transformations to attributes (e.g., renaming or deleting attributes).
- Update values in telemetry data dynamically.

---

## Overview of the Configuration

The **Transform Processor** allows you to perform a variety of modifications to incoming telemetry data, including:

- **Add or Update Attributes**: You can add or modify attribute values on traces, metrics, or logs.
- **Delete Attributes**: Remove unnecessary attributes to keep your telemetry data clean and efficient.
- **Rename Attributes**: Modify attribute keys for consistency across your observability pipeline.

### Example YAML Configuration for the Transform Processor

Here is an example configuration that demonstrates how to use the Transform Processor to modify trace data:

```yaml
processors:
  transform:
    traces:
      - action: update
        key: http.method
        value: POST
        condition: 'attributes["http.method"] == "GET"'
      - action: insert
        key: new_attribute
        value: "transformed_value"
      - action: delete
        key: old_attribute

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [transform]
      exporters: [otlp]
```

### Key Sections of the Configuration

1. **`transform` processor**: This is where the transformations on trace data are specified.
   - **`action: update`**: Update an attribute value based on a condition. In this case, the `http.method` attribute is updated from `GET` to `POST`.
   - **`action: insert`**: Insert a new attribute `new_attribute` with a fixed value `"transformed_value"`.
   - **`action: delete`**: Delete an existing attribute, here we remove `old_attribute`.

2. **Service pipelines**: The processor is applied as part of the `traces` pipeline, which receives traces from the `otlp` receiver and exports them to the `otlp` exporter.

## Step 1: Review the YAML Configuration

Let's break down the key sections of the YAML configuration that we will use in this workshop.

### 1.1 The Transform Processor

The **Transform Processor** is configured under the `processors` section. Here's how each transformation is specified:

#### Update Action

```yaml
- action: update
  key: http.method
  value: POST
  condition: 'attributes["http.method"] == "GET"'
```

This action updates the `http.method` attribute. It looks for traces where the `http.method` is `"GET"` and changes it to `"POST"`.

#### Insert Action

```yaml
- action: insert
  key: new_attribute
  value: "transformed_value"
```

This action inserts a new attribute, `new_attribute`, with a fixed value `"transformed_value"` to every trace processed.

#### Delete Action

```yaml
- action: delete
  key: old_attribute
```

This action deletes an attribute called `old_attribute` from the trace data.

### 1.2 Service Pipelines

In the **service** section, we define a pipeline that uses the `transform` processor.

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [transform]
      exporters: [otlp]
```

This pipeline receives traces via the `otlp` receiver, processes them through the `transform` processor, and then exports them using the `otlp` exporter.

## Step 2: Set Up the OpenTelemetry Collector

### 2.1 Save the Configuration

Save the YAML configuration to a file, e.g., `otel-collector-transform-config.yaml`.

### 2.2 Run the OpenTelemetry Collector

Start the OpenTelemetry Collector with your configuration:

```bash
otelcol --config=otel-collector-transform-config.yaml
```

This will start the OpenTelemetry Collector with the transformation configuration.

## Step 3: Simulate Trace Data

### 3.1 Generate Sample Trace Data

To test the transformation, you need to generate trace data with certain attributes.

- For example, a trace could include the `http.method` attribute set to `"GET"`, and you want the `http.method` to be transformed to `"POST"`.
- You can use any instrumented application that sends trace data to the OpenTelemetry Collector. Alternatively, use a trace simulator or generate trace data manually.

Make sure to include:

- A trace with the `http.method` attribute set to `"GET"`.
- A trace with an `old_attribute` that should be deleted.

### 3.2 Observe the Transformation

Once you send the trace data, you should see the following transformations:

- Any `http.method` attribute with the value `"GET"` will be updated to `"POST"`.
- The new attribute `new_attribute` will be added with the value `"transformed_value"`.
- The `old_attribute` will be removed from the trace.

You can view the transformed trace data in your exporter (e.g., Jaeger, Zipkin, or any other trace backend).

## Step 4: Debug and Monitor the Transformations

### 4.1 Monitor the Logs

To ensure the transformations are working correctly, check the OpenTelemetry Collector logs. Look for log entries related to the transformation processing.

### 4.2 Customize Your Transformations

You can modify the transformation actions to suit your needs. Here are some customization options:

- **Add multiple attributes**: Insert multiple attributes with different conditions.
- **Use conditions with complex expressions**: Combine conditions with logical operators to match more complex attribute patterns.
- **Apply transformations on specific trace types**: Use different transformations for different trace types by modifying the condition.

## Step 5: Extend the Transform Processor

### 5.1 Update Multiple Attributes Based on Conditions

You can update multiple attributes at once. For example, if you want to update the `http.status_code` and `http.method` attributes:

```yaml
- action: update
  key: http.status_code
  value: "200"
  condition: 'attributes["http.status_code"] == "404"'

- action: update
  key: http.method
  value: "POST"
  condition: 'attributes["http.method"] == "GET"'
```

### 5.2 Use Advanced Conditions

Conditions can be as complex as needed. Here’s an example of updating attributes based on a combination of conditions:

```yaml
- action: update
  key: user_id
  value: "redacted"
  condition: 'attributes["user_type"] == "admin" and attributes["http.status_code"] == "403"'
```

This transformation will only update the `user_id` attribute when the `user_type` is `"admin"` and the `http.status_code` is `"403"`.

### 5.3 Conditional Deletion

You can conditionally delete attributes based on specific criteria. For example:

```yaml
- action: delete
  key: sensitive_data
  condition: 'attributes["http.status_code"] == "500"'
```

This will delete the `sensitive_data` attribute from traces where the `http.status_code` is `"500"`.

---

## Conclusion

In this workshop, you have learned how to use the **Transform Processor** in the OpenTelemetry Collector to modify trace data dynamically. You’ve seen how to:

- Update existing attributes based on conditions.
- Insert new attributes.
- Delete unwanted attributes.

By leveraging the **Transform Processor**, you can efficiently modify telemetry data as it passes through the OpenTelemetry Collector, ensuring that only relevant and well-structured data is sent to your observability backends.

---

## Next Steps

- **Extend the Transform Processor**: Add more transformations based on different conditions.
- **Integrate with Different Backends**: Try exporting your transformed data to different observability backends like Prometheus, Jaeger, or Splunk.
- **Explore Other Processors**: Experiment with other processors like `batch`, `memory_limiter`, or `filter` to further enhance your telemetry processing pipeline.
