---
title: 5.2 Test Filter Processor
linkTitle: 5.2 Test Filter Processor
weight: 2
---

To test your configuration, you'll need to generate some trace data that includes a span named `"/_healthz"`.

{{% notice title="Exercise" style="green" icon="running" %}}

**Create "noisy" 'healthz' span**:

1. Create a new file called `health.json` in the `5-dropping-spans` directory.
2. Copy and paste the following JSON into the `health.json` file.
3. Note the span name is set to `{"name":"healthz"}` in the json.

```json { title="health.json" }
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"frontend"}}]},"scopeSpans":[{"scope":{"name":"healthz","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"/_healthz","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[]}]}]}]}
```

```text { title="Updated Directory Structure" }
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
│   ├───checkpoint-dir
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── health.json
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

**Start the Gateway**: In the **Gateway** terminal window navigate to the `[WORKSHOP]/5-dropping-spans` directory and run:

```sh { title="Gateway" }
../otelbin --config=gateway.yaml
```

**Start the Agent**: In the **Agent** terminal window navigate to the `[WORKSHOP]/5-dropping-spans` directory and run:

```sh { title="Agent" }
../otelbin --config=agent.yaml
```

**Send the new `health.json` payload:** In the **Test** terminal window navigate to the `[WORKSHOP]/5-dropping-spans` directory and run the `curl` command below. (**Windows use `curl.exe`**).
  
```sh { title="cURL command" }
curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@health.json"
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

The **Agent** has forward the span to the **Gateway**.
  
**Check the Gateway Debug output**:

1. The Gateway should **NOT** show any span data received. This is because the **Gateway** is configured with a filter to drop spans named `"/_healthz"`, so the span will be discarded/dropped and not processed further.
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

Stop the **Agent** and **Gateway** using `Ctrl-C`.
