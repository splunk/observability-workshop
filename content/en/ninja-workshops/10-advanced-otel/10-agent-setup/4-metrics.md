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

  ```yaml
    metrics:
      receivers: [otlp, hostmetrics]  # Array of Metric Receivers
     #processors:                     # Array of Metric Processors
  ```

{{% /notice %}}

Validate again with **[otelbin.io](https://www.otelbin.io/)**. Given we updated the `metrics:` pipeline your result should look like this:

![otelbin-a-1-4-metrics](../../images/agent-1-4-metrics.png?width=50vw)

 If **otelbin.io** complains about the scrapers entry, make sure you select the Splunk OpenTelemetry Collector from the validation target drop down at the top of the screen.

### Test & Validate

Delete the current agent.out, then restart the agent again using the agent.yaml. Based on the current config, the collector should write some metric lines to your agent.out at startup, then will repeat that every hour. The output from agent.out looks like this:

Note that we show the entries for **cpu0** only, you will get cpu entries for all the cpu's/cores present in your system.

Also note that in the `resourceMetrics` section you will find the same attributes added as with the trace we looked at earlier, these will help with corelating between traces and metrics.


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

<<<<<<< HEAD
Stop the Agent and Gateway processes by pressing `Command-C` (macOS) or `Ctrl-C` (Windows/Linux) in their respective terminals.
=======
Stop the Agent processes by pressing `Command-C` (macOS) or `Ctrl-C` (Windows/Linux) in their respective terminals.
>>>>>>> 191263721 ( checked  terminal window naming, and reduced cpu metric to cpu0 only till end of  gateway)
