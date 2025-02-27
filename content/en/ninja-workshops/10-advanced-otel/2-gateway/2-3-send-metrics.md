---
title: 2.3 Send metrics from the Agent to the Gateway
linkTitle: 2.3 Send Metrics
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Agent**: In the **Agent** terminal window start the agent with the updated configuration:

```sh { title="Agent" }
../otelcol --config=agent.yaml
```

**Verify CPU Metrics**:

1. Check that when the **Agent** starts, it immediately starts sending **CPU** metrics.
2. Both the **Agent** and the **Gateway** will display this activity in their debug output. The output should resemble the following snippet:

```text
<snip>
NumberDataPoints #37
Data point attributes:
    -> cpu: Str(cpu9)
    -> state: Str(system)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 9637.660000
```

At this stage, the **Agent** continues to collect **CPU** metrics once per hour or upon each restart and sends them to the gateway. The **OpenTelemetry Collector**, running in **Gateway** mode, processes these metrics and exports them to a file named `./gateway-metrics.out`. This file stores the exported metrics as part of the pipeline service.  

**Verify Data arrived at Gateway**:

1. Open the newly created `gateway-metrics.out` file.
2. Check that it contains **CPU** metrics.
3. The Metrics should include details similar to those shown below (We're only displaying the `resourceMetrics` section and the first set of **CPU** metrics):

{{% tabs %}}
{{% tab title="`cat ./gateway-metrics.out`" %}}

```json
{"resourceMetrics":[{"resource":{"attributes":[{"key":"host.name","value":{"stringValue":"YOUR_HOST_NAME"}},{"key":"os.type","value":{"stringValue":"YOUR_OS"}},{"key":"otelcol.service.mode","value":{"stringValue":"gateway"}}]},"scopeMetrics":[{"scope":{"name":"github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper","version":"v0.116.0"},"metrics":[{"name":"system.cpu.time","description":"Total seconds each logical CPU spent on each mode.","unit":"s","sum":{"dataPoints":[{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1737133726158376000","asDouble":1168005.59}]}}]}]}]}
```

{{% /tab %}}
{{% tab title="`cat ./gateway-metrics.out | jq`" %}}

```json
{
  "resourceMetrics": [
    {
      "resource": {
        "attributes": [
          {
            "key": "host.name",
            "value": {
              "stringValue": "YOUR_HOST_NAME"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "YOUR_OS"
            }
          },
          {
            "key": "otelcol.service.mode",
            "value": {
              "stringValue": "gateway"
            }
          }
        ]
      },
      "scopeMetrics": [
        {
          "scope": {
            "name": "github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper",
            "version": "v0.116.0"
          },
          "metrics": [
            {
              "name": "system.cpu.time",
              "description": "Total seconds each logical CPU spent on each mode.",
              "unit": "s",
              "sum": {
                "dataPoints": [
                  {
                    "attributes": [
                      {
                        "key": "cpu",
                        "value": {
                          "stringValue": "cpu0"
                        }
                      },
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "user"
                        }
                      }
                    ],
                    "startTimeUnixNano": "1733753908000000000",
                    "timeUnixNano": "1737133726158376000",
                    "asDouble": 1168005.59
                  },
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}
