---
title: 2.1 Access Tokens
linkTitle: 2.1 Access Tokens
weight: 1
---

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
The `otlphttp` exporter is now the default method for sending metrics and traces to the Splunk Observability Cloud.  

This exporter is included in the default configuration of the Splunk Distribution of the OpenTelemetry Collector when deployed in host monitoring (agent) mode.  

The use of older `sapm` and `signalfx` exporters are being phased out gradually.  

#### Additional info on how to use Splunk Access Tokens

- **Headers Configuration**:
  Use the `headers:` key with the sub-key `X-SF-Token:` to pass an access token. This aligns with the OpenTelemetry approach for token-based authentication.  
  This works both in `agent` as in `gateway` mode.

- **Pass-through Mode**:
  To enable pass-through mode, set `include_metadata:` to `true` in the `otlp` receiver configuration on the gateway. This ensures that headers received by the collector are forwarded with the data through the collector's pipeline.

- **Batch Processing**:
  Configure the `batch:` section with the key `X-SF-Token:` to group traces, metrics, and logs by the same access token. This helps the collector batch data efficiently before sending it to the backend, improving performance and reducing overhead. This works both in `agent` as in `gateway` mode.

{{% /notice %}}
