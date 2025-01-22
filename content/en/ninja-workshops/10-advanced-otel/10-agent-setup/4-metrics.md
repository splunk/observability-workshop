---
title: Adding the Hostmetric Receiver
linkTitle: 1.4 Hostmetric Receiver
weight: 4
---
### Setup

As a last exercise in this section, we are going to add a metric receiver that triggers at startup, then scrapes once every hour (to reduce spam):

 {{% notice title="Exercise" style="green" icon="running" %}}
 To show metrics flowing in, we are going to modify the agent.yaml some more:

- **Add** `hostmetrics:` **receiver:**

  ```yaml
    # otlp                           # Previous otlp receiver setup 
    hostmetrics:                     # Receiver Type
      collection_interval: 3600s.    # Sets the collection cycle to one hour 
      scrapers:                      # Array of Host Metric scrapers
        cpu:                         # Scraper for cpu metrics
  ```

- **Add** `hostmetrics` **receiver** to `metrics:` Pipeline

  ```yaml
      # Traces Pipeline section
    metrics:
      receivers: [otlp, hostmetrics]  # Array of Metric Receivers
      processors:                     # Array of Metric Processors
       - memory_limiter               # Handles memory limits for this Pipeline
       - resourcedetection            # Adds System Attributes to data  flowing through this pipeline 
       - resource/add_mode            # Adds Collectors mode to data flowing through this pipeline 
      exporters: [debug,file]         # Array of exporters 
      # Logs Pipeline section

  ```

{{% /notice %}}

Validate again with **[otelbin.io](https://www.otelbin.io/)**. Given we updated the `metrics:` pipeline your result should look like this:

![otelbin-a-1-4-metrics](../../images/agent-1-4-metrics.png?width=50vw)

 If **otelbin.io** complains about the scrapers entry, make sure you select the Splunk OpenTelemetry Collector from the validation target drop down at the top of the screen.

### Test & Validate

Delete the current agent.out, then restart the agent again using the agent.yaml. Based on the current config, the collector should write some metric lines to your agent.out at startup, then will repeat that every hour. The output from agent.out looks like this:

Note that we show the entries for **cpu1** only, you will get cpu entries for all the cpu's/cores present in your system.

Also note that in the `resourceMetrics` section you will find the same attributes added as with the trace we looked at earlier, these will help with corelating between traces and metrics.

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

```json
{"resourceMetrics":[{"resource":{"attributes":[{"key":"host.name","value":{"stringValue":"YOUR_HOST_NAME"}},{"key":"os.type","value":{"stringValue":"YOUR_OS"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeMetrics":[{"scope":{"name":"github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/cpuscraper","version":"v0.116.0"},"metrics":[{"name":"system.cpu.time","description":"Total seconds each logical CPU spent on each mode.","unit":"s","sum":{"dataPoints":[{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1028590.93},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":447490.75},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":553542.9},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu0"}},{"key":"state","value":{"stringValue":"interrupt"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":0},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"user"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":1029342.54},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"system"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":441906.19},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}},{"key":"state","value":{"stringValue":"idle"}}],"startTimeUnixNano":"1733753908000000000","timeUnixNano":"1736873595700306000","asDouble":558385.54},{"attributes":[{"key":"cpu","value":{"stringValue":"cpu1"}}]}]}}]}]}]}
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
              "stringValue": "agent"
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
                    "timeUnixNano": "1736873595700306000",
                    "asDouble": 1028590.93
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
                    "timeUnixNano": "1736873595700306000",
                    "asDouble": 447490.75
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
                    "timeUnixNano": "1736873595700306000",
                    "asDouble": 553542.9
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
                    ],
                    "startTimeUnixNano": "1733753908000000000",
                    "timeUnixNano": "1736873595700306000",
                    "asDouble": 0
                  },
                  {
                    "attributes": [
                      {
                        "key": "cpu",
                        "value": {
                          "stringValue": "cpu1"
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
                    "timeUnixNano": "1736873595700306000",
                    "asDouble": 1029342.54
                  },
                  {
                    "attributes": [
                      {
                        "key": "cpu",
                        "value": {
                          "stringValue": "cpu1"
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
                    "timeUnixNano": "1736873595700306000",
                    "asDouble": 441906.19
                  },
                  {
                    "attributes": [
                      {
                        "key": "cpu",
                        "value": {
                          "stringValue": "cpu1"
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
                    "timeUnixNano": "1736873595700306000",
                    "asDouble": 558385.54
                  },
                  {
                    "attributes": [
                      {
                        "key": "cpu",
                        "value": {
                          "stringValue": "cpu1"
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

Stop the agent for now using `Command-c/Ctrl-c`.
