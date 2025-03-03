---
title: 5.2 Test Filter Processor
linkTitle: 5.2 Test Filter Processor
weight: 2
---

To test your configuration, you'll need to generate some trace data that includes a span named `"/_healthz"`.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In the **Gateway terminal** window navigate to the `[WORKSHOP]/5-dropping-spans` directory and run:

```sh { title="Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent terminal** window navigate to the `[WORKSHOP]/5-dropping-spans` directory and run:

```sh { title="Agent" }
../otelcol --config=agent.yaml
```

**Send the new `health.json` payload:** In the **Spans terminal** window navigate to the `[WORKSHOP]/5-dropping-spans` directory and run the `loadgen`:
  
```sh { title="Loadgen" }
../loadgen -health
```

**Verify Agent Debug output shows the `healthz` span**: Confirm that the span `span` payload is sent, Check the agent’s debug output to see the span data like the snippet below:

```text { title="Debug Output" }
<snip>
Span #0
    Trace ID       : 5b8efff798038103d269b633813fc60c
    Parent ID      : eee19b7ec3c1b173
    ID             : eee19b7ec3c1b174
    Name           : /_healthz
    Kind           : Server
<snip>
```

The `agent` has forward the span to the **Gateway**.
  
**Check the Gateway Debug output**:

1. The Gateway should **NOT** show any span data received. This is because the `gateway` is configured with a filter to drop spans named `"/_healthz"`, so the span will be discarded/dropped and not processed further.
2. Confirm normal span are processed by using the cURL command with the `trace.json` file again. This time, you should see both the agent and gateway process the spans successfully.
{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

When using the `Filter` processor make sure you understand the look of your incoming data and test the configuration thoroughly. In general, use **as specific a configuration as possible** to lower the risk of the wrong data being dropped.
{{% /notice %}}
<!--
---
The following excises can be done in your own time after the workshop.

**(Optional) Modify the Filter Condition**:

If you’d like, you can customize the filter condition to drop spans based on different criteria. This step is optional and can be explored later. For example, you might configure the filter to drop spans that include a specific tag or attribute.

Here’s an example of dropping spans based on an attribute:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'attributes["service.name"] == "frontend"'
```

This filter would drop spans where the `service.name` attribute is set to `frontend`.

**(Optional) Filter Multiple Spans**:

You can filter out multiple span names by extending the span list:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'name == "/_healthz"'
      - 'name == "/internal/metrics"'
```

This will drop spans with the names `"/_healthz"` and `"/internal/metrics"`.
-->
You can further extend this configuration to filter out spans based on different attributes, tags, or other criteria, making the OpenTelemetry Collector more customizable and efficient for your observability needs.

Stop the `agent` and `gateway` using `Ctrl-C`.
