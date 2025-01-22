---
title: Test the gateway and prepare the agent
linkTitle: 2.1 Test Gateway & Configure Agent
weight: 1
---

## Test Gateway

Open a new terminal and navigateto the`[WORKSHOP]/2-gateway` folder and run the following command to test the gateway configuration:

```text
../otelcol --config=gateway.yaml
```

If everything is set up correctly, the first and last lines of the output should look like:

```text
2025/01/15 15:33:53 settings.go:478: Set config to [gateway.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

---

### Update agent configuration

Remaining in the `[WORKSHOP]/2-gateway` folder. Open the `agent.yaml` we copied earlier in your editor, and configure a `otlphttp` exporter (this is now the preferred exporter for Splunk Observability Cloud):

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configure the `otlphttp` exporter**: Ensure the `endpoint` is set to the gateway endpoint and add the `X-SF-Token` header with a Splunk Access Token.

  ```yaml
  exporters:
    otlphttp:
      endpoint: "http://localhost:5318" # Gateway endpoint
      headers:
        # Replace with a Splunk Access Token
        X-SF-Token: "FAKE_SPLUNK_ACCESS_TOKEN"
  ```

- **Update Pipelines**: Add the `otlphttp` exporter to the `traces`, `metrics`, and `logs` pipelines.

  ```yaml
  service:
  pipelines:
    traces:              # Traces Pipeline
      receivers: [otlp]  # Array of receivers in this pipeline
      processors:        # Array of Processors in thi pipeline
      - memory_limiter   # You also could use [memory_limiter]
      # Array of Exporters in this pipeline
      exporter: [otlphttp, file, debug]
  ```

{{% /notice %}}  
Again, validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. As example, here is the result for the `metrics` pipeline:

![otelbin-g-2-2-metrics](../../images/gateway-2-2-metrics.png)

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
The `otlphttp` exporter is now the default method for sending metrics and traces to the Splunk Observability Cloud.  

This exporter is included in the default configuration of the Splunk Distribution of the OpenTelemetry Collector when deployed in host monitoring (agent) mode.  

The older `sapm` and `signalfx` exporters are being phased out gradually.  

##### Key Details

- **Headers Configuration**:
  Use the `headers:` key with the subkey `X-SF-Token:` to pass an access token. This aligns with the OpenTelemetry approach for token-based authentication.

- **Passthrough Mode**:
  To enable passthrough mode, set `include_metadata:` to `true` in the `otlp` receiver configuration on the gateway. This ensures that headers received by the collector are forwarded with the data through the collector's pipeline.

- **Batch Processing**:
  Configure the `batch:` section with the key `X-SF-Token:` to group traces, metrics, and logs by the same access token. This helps the collector batch data efficiently before sending it to the backend, improving performance and reducing overhead.
{{% /notice %}}
