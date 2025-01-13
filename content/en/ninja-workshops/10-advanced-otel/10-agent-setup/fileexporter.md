---
title: Add a File exporter and Meta Data.
linkTitle: File exporter & Meta data
weight: 15
---
As we want to be able to see the output generated for the pipeline we are going to write the otlp data to files, so we can compare.

Let's run our second exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

* Add an **file** exporter, add a *path* entry, with a value of *"agent.out"* and add the exporter as the first exporter entry to all the pipelines (leaving debug in place)

{{% /notice %}}

Validate your new `agent.yaml` with [https://otelbin.io](https://otelbin.io), your pipelines should look like this:

![otelbin1](../images/agent-1-1.png)

---
Run the following command to  test your config (make sure you use the right otel collector you downloaded):

```text
otelcol_darwin_arm64 --config=agent.yaml
```

If you have done everything correctly the last line of the out put should be:

```text
2025-01-13T12:43:51.747+0100 info service@v0.115.0/service.go:261 Everything is ready. Begin running and processing data.
```

Now  start a new shell and create a file called **trace.json* and copy the following content:

```json
{
    "resourceSpans": [
      {
        "resource": {
          "attributes": [
            {
              "key": "service.name",
              "value": {
                "stringValue": "my.service"
              }
            },
            {
              "key": "deployment.environment",
              "value": {
                "stringValue": "my.environment"
              }
            }
          ]
        },
        "scopeSpans": [
          {
            "scope": {
              "name": "my.library",
              "version": "1.0.0",
              "attributes": [
                {
                  "key": "my.scope.attribute",
                  "value": {
                    "stringValue": "some scope attribute"
                  }
                }
              ]
            },
            "spans": [
              {
                "traceId": "5B8EFFF798038103D269B633813FC60C",
                "spanId": "EEE19B7EC3C1B174",
                "parentSpanId": "EEE19B7EC3C1B173",
                "name": "I'm a server span",
                "startTimeUnixNano": "1544712660000000000",
                "endTimeUnixNano": "1544712661000000000",
                "kind": 2,
                "attributes": [
                  {
                    "keytest": "my.span.attr",
                    "value": {
                      "stringValue": "some value"
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
```

In the second Shell, run the following command to test your setup:

```shell
curl -X POST -i http://localhost:4318/v1/traces \
-H "Content-Type: application/json" \
 -d @trace.json 
```

Your collector should show the following output:

 ```text
2025-01-13T13:26:13.502+0100 info Traces {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
2025-01-13T13:26:13.502+0100 info ResourceSpans #0
Resource SchemaURL:
Resource attributes:
    -> service.name: Str(my.service)
    -> deployment.environment: Str(my.environment)
ScopeSpans #0
ScopeSpans SchemaURL:
InstrumentationScope my.library 1.0.0
InstrumentationScope attributes:
    -> my.scope.attribute: Str(some scope attribute)
Span #0
    Trace ID       : 5b8efff798038103d269b633813fc60c
    Parent ID      : eee19b7ec3c1b173
    ID             : eee19b7ec3c1b174
    Name           : I'm a server span
    Kind           : Server
    Start time     : 2018-12-13 14:51:00 +0000 UTC
    End time       : 2018-12-13 14:51:01 +0000 UTC
    Status code    : Unset
    Status message :
Attributes:
    -> : Str(some value)
    {"kind": "exporter", "data_type": "traces", "name": "debug"}
```
