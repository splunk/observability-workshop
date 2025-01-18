---
title: Test the gateway and prepare the agent  
linkTitle: 2.1 Test Gateway, Setup Agent 
weight: 1
---

## Test Gateway

Start an other shell, make sure your in your [WORKSHOP]/2-gateway folder and run the following command in the new shell to test your gateway config.

```text
[WORKSHOP]/otelcol --config=gateway.yaml
```

If you have done everything correctly, the first and the last line of the output should be:

```text
2025/01/15 15:33:53 settings.go:478: Set config to [gateway.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

---

### Change agent config

Again, check if you in your [WORKSHOP]/2-gateway folder.  Open the agent.yaml we copied across earlier in your editor and let's add the `OTLP/HTTP` exporter to the agent.yaml - *This is the new preferred exporter for our o O11Y backend*:

{{% notice title="Exercise" style="green" icon="running" %}}

- Add `otlphttp:` under the `exporter:` key
  - Add `endpoint:` key and set it to a value of `"http://localhost:5318"`   *  note that we use the port of the gateway
  - Add `headers:` key
    - Add `X-SF-Token:` key and set it with a fake access token like `"FAKE_SPLUNK_ACCESS_TOKEN"`  

- Add this as the first exporter in all the `exporter` arrays of the pipelines.  (Replace `file` and leave debug in place)

{{% /notice %}}  
Again validate the configuration using **[otelbin.io](https://www.otelbin.io/)**, the results should look like this:

![otelbin-g-2-2-w](../../images/gateway-2-2w.png)

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}  
The use of the **otlphttp** exporter is now the default method to send metric and traces to Splunk Observability Cloud.  
This component is included in the default configuration of the Splunk Distribution of the OpenTelemetry Collector to send traces and metrics to Splunk Observability Cloud when deploying in host monitoring (agent) mode

The older *apm* and *signalfx* exporters you may be familiar with, will be phased out over time

The `headers:` key with its sub key `X-SF-Token:` is the OpenTelemetry way to pass a access token.

To enable the passthrough mode, we did set `include_metadata:` to `true` on the `otlp` receiver in the gateway. It’ll ensure that headers passed to the collector are passed along with the data down in the collector’s pipeline.
{{% /notice %}}
