---
title: Test your gateway  
linkTitle: 2.1 Test your Gateway 
weight: 1
---

## Test Gateway

Start an other shell, make sure your in your workhop folder and run the following command in the new shell to test your gateway config.

```text
[WORKSHOP]/otelcol --config=gateway.yaml
```

If you have done everything correctly, the first and the last line of the output should be:

```text
2025/01/15 15:33:53 settings.go:478: Set config to [gateway.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261	Everything is ready. Begin running and processing data.
```

---

### Change agent config

Open our agent.yaml in your editor and make the following changes:

{{% notice title="Exercise" style="green" icon="running" %}}

* Add the following exporter *This is the new preferred exporter for our backend*

```text
  otlphttp: exporter
    endpoint: entry, with a value of "http://localhost:5318"   * using the port of the gateway   
    headers: entry,
      X-SF-Token: entry, with a fake access token like "FAKE_SPLUNK_ACCESS_TOKEN"  
  ```

* Add this as the first exporter to all the sections of the pipelines.  (Remove file and leave debug in place)

{{% /notice %}}  
Again validate the configuration using **[otelbin.io](https://www.otelbin.io/)**, the results should look like this:

![otelbin-g-2-2-w](../../images/gateway-2-2w.png)

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}  
Use the **otlphttp** exporter as the default method to send traces to Splunk Observability Cloud.  
This component is now included in the default configuration of the Splunk Distribution of the OpenTelemetry Collector to send traces and metrics to Splunk Observability Cloud when deploying in host monitoring (agent) mode

The older *apm* and *signalfx* exporters you may be familiar with, will be phased out over time
{{% /notice %}}
