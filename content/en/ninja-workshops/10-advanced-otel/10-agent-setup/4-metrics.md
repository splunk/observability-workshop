---
title: Adding the Hostmetric Receiver
linkTitle: 1.4 Hostmetric Receiver
weight: 4
---
### Setup

As a final exercise in this section, we’ll add the `hostmetric` receiver which is used to collect host-level metrics from the system where it is running. These metrics provide insights into the performance and health of the underlying infrastructure, such as CPU usage, memory consumption, disk activity, and network performance.

For this exercise we will only scrape the CPU metrics once every hour to minimize the amount of data generated.

 {{% notice title="Exercise" style="green" icon="running" %}}
 To show metrics flowing in, we are going to modify the agent.yaml some more:

- **Add the `hostmetrics:` receiver**: Add the following under the `receivers` section:

  ```yaml
    hostmetrics:                  # Receiver Type
      collection_interval: 3600s  # Scrape metrics every hour
      scrapers:                   # Array of hostmetric scrapers
        cpu:                      # Scraper for cpu metrics
  ```

- **Update the `metrics` pipeline**: Add the `hostmetrics` receiver to the `metrics` pipeline in the `service` section:  
(keep a version of the original, by commenting it out):

  ```yaml
    metrics:
      #receivers: [otlp]               # Array of Metric Receivers
      receivers: [otlp, hostmetrics]  # Array of Metric Receivers
     #processors:                     # Array of Metric Processors
  ```

{{% /notice %}}

Validate again with **[otelbin.io](https://www.otelbin.io/)**. Given we updated the `metrics:` pipeline your result should look like this:

![otelbin-a-1-4-metrics](../../images/agent-1-4-metrics.png?width=50vw)


### Validate Your Host Metric Changes

To validate the changes, delete the current `agent.out` file and restart the agent using the `agent.yaml` configuration in the `Agent` terminal window. When the agent restarts, the collector will write **cpu** metrics to agent.out. This process will repeat every hour as long as the agent continues running.

``` text
...
NumberDataPoints #38
Data point attributes:
     -> cpu: Str(cpu9)
     -> state: Str(idle)
StartTimestamp: 2025-01-27 08:51:03 +0000 UTC
Timestamp: 2025-01-27 10:58:05.111193 +0000 UTC
Value: 7509.620000
NumberDataPoints #39
Data point attributes:
     -> cpu: Str(cpu9)
     -> state: Str(interrupt)
StartTimestamp: 2025-01-27 08:51:03 +0000 UTC
Timestamp: 2025-01-27 10:58:05.111193 +0000 UTC
Value: 0.000000
    {"kind": "exporter", "data_type": "metrics", "name": "debug"}
```

The output in `agent.out` will also include metrics. The example provided below  focuses on **cpu0** only, but you will see entries for all CPUs/cores available on your system. Additionally, in the `'resourceMetrics` section, you will find the same attributes added by the 'processors' as those included in the traces we reviewed earlier. These attributes help match traces and metrics.

{{% tabs %}}
{{% tab title="Compact JSON" %}}

```json
{"resourceMetrics":[{"resource":{"attributes":[{"key":"host.name","value":{"stringValue":"YOUR_HOST_NAME"}},{"key":"os.type","value":{"stringValue":"YOUR_OS"}},{"key":"otelcol.service.mode","value":{"stringValue":"gateway"}}]},"scopeMetrics":[{"scope":{"name":"github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper","version":"v0.116.0"},"metrics":[{"name":"system.cpu.time","description":"Total seconds each logical CPU spent on each mode.","unit":"s","sum":{"dataPoints":[{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1737133726158376000","asDouble":1168005.59},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1737133726158376000","asDouble":504260.9},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1737133726158376000","asDouble":615648.75},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"interrupt"}}]}]}}]}]}]}
```

{{% /tab %}}
{{% tab title="Formatted JSON" %}}

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
                          "stringValue": "system"
                        }
                      }
                    ],
                    "startTimeUnixNano": "1733753908000000000",
                    "timeUnixNano": "1737133726158376000",
                    "asDouble": 504260.9
                  },
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
                          "stringValue": "idle"
                        }
                      }
                    ],
                    "startTimeUnixNano": "1733753908000000000",
                    "timeUnixNano": "1737133726158376000",
                    "asDouble": 615648.75
                  },
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
                          "stringValue": "interrupt"
                        }
                      }
                    ]
                  }
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

Stop the agent process by pressing `Ctrl-C` in the `Agent` terminal.
