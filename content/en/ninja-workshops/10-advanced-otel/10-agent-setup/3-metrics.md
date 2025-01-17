---
title: Adding the hostmetric reciever
linkTitle: 1.3 Adding a Metric Receiver
weight: 3
---
### Adding Metrics

As a last exercise in this section, we are going to add a metric receiver that triggers at startup, then scrapes once every hour (to reduce spam):

 {{% notice title="Exercise" style="green" icon="running" %}}

 - Add `hostmetrics:` under the `receiver:` key
    - Add `collection_interval:` key and set a value of `3600s` *(once every hour)
    - Add `scrapers:` key
      - add `cpu:` key

- Add the `hostmetrics` receiver to the receivers array in the `metrics:`  pipeline (leaving `otlp` as the first one )

{{% /notice %}}

Validate again with **[otelbin.io](https://www.otelbin.io/)**, your result should look like this:
![otelbin-a-1-4-w](../../images/agent-1-4w.png)

 (if **otelbin.io** complains about the scrapers entry, make sure you select the Splunk OpenTelemetry Collector from the validation target drop down at the top of the screen)

### Metric Test & Validate

Restart the agent again using the agent.yaml and tail the agent.out, the collector  should  write metric lines to your agent.out every 10 seconds that looks like this:

Note that we show the entries for **cpu1** only, you will get cpu entries for all the cpu's/cores present in your system.  
Also note that in the resourceMetrics section, you find the same attributes added as with the trace we looked at earlier, these will help with corelating between traces and metrics.

{{% tabs %}}
{{% tab title="Compact JSON" %}}

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

Stop the agent for now using `CTRL-C`.
