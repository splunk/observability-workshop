---
title: 2.1 Access Tokens
linkTitle: 2.1 Access Tokens
weight: 1
---


{{% notice title="Tip" style="primary" icon="lightbulb" %}}

## Introduction to the otlphttp Exporter

The `otlphttp` exporter is now the default method for sending metrics and traces to Splunk Observability Cloud. This exporter provides a standardized and efficient way to transmit telemetry data using the OpenTelemetry Protocol (OTLP) over HTTP.

When deploying the Splunk Distribution of the OpenTelemetry Collector in host monitoring (agent) mode, the `otlphttp` exporter is included by default. This replaces older exporters such as `sapm` and `signalfx`, which are gradually being phased out.

{{% /notice %}}

## Configuring Splunk Access Tokens

To authenticate and send data to Splunk Observability Cloud, you need to configure access tokens properly.
In OpenTelemetry, authentication is handled via HTTP headers. To pass an access token, use the `headers:` key with the sub-key `X-SF-Token:`. This configuration works in both agent and gateway mode.

Example:

```yaml
exporters:
  otlphttp:
    endpoint: "https://ingest.<realm>.signalfx.com"
    headers:
      X-SF-Token: "your-access-token"
```

### Pass-Through Mode

If you need to forward headers through the pipeline, enable pass-through mode by setting `include_metadata:` to `true` in the OTLP receiver configuration. This ensures that any authentication headers received by the collector are retained and forwarded along with the data.

Example:

```yaml
receivers:
  otlp:
    protocols:
      http:
        include_metadata: true
```

This is particularly useful in gateway mode, where data from multiple agents may pass through a centralized gateway before being sent to Splunk.

## Understanding Batch Processing

The Batch Processor is a key component in optimizing data transmission efficiency. It groups traces, metrics, and logs into batches before sending them to the backend. Batching improves performance by:

- Reducing the number of outgoing requests.
- Improving compression efficiency.
- Lowering network overhead.

### Configuring the Batch Processor

To enable batching, configure the `batch:` section and include the `X-SF-Token:` key. This ensures that data is grouped correctly before being sent to Splunk Observability Cloud.

Example:

```yaml
processors:
  batch:
    metadata_keys: [X-SF-Token]   # Array of metadata keys to batch 
    send_batch_size: 100
    timeout: 5s
```

### Best Practices for Batch Processing

For optimal performance, it is recommended to use the Batch Processor in every collector deployment. The best placement for the Batch Processor is **after the memory limiter and sampling processors**. This ensures that only necessary data is batched, avoiding unnecessary processing of dropped data.

### Gateway Configuration with Batch Processor

When deploying a gateway, ensure that the Batch Processor is included in the pipeline:

```yaml
service:
  pipelines:
    traces:
      processors: [memory_limiter, tail_sampling, batch]
```

## Conclusion

The `otlphttp` exporter is now the preferred method for sending telemetry data to Splunk Observability Cloud. Properly configuring Splunk Access Tokens ensures secure data transmission, while the Batch Processor helps optimize performance by reducing network overhead. By implementing these best practices, you can efficiently collect and transmit observability data at scale.
