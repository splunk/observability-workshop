---
title: Route data though a gateway  
linkTitle: 2. Gateway Setup
time: 10 minutes
weight: 20
---

### Gateway Setup

In the location where you are running the workshop on your machine, create a sub directory called **2-gateway**, the copy the last version of the agent.yaml acrooss toe the new directory. 
Move into the *[WORKSHOP]/2-gateway* directory and create a file called **gateway.yaml**  and copy the following starting config in it.

``` text
receivers:

exporters:
    
processors:
  memory_limiter:
    check_interval: 2s
    limit_mib: 512
  
service:
  pipelines:
    traces:
    metrics:
    logs:
```

Let's start with our first exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

* Add the following as a receiver:

```text
  otlp: receiver
    protocols: section
      HTTP: entry, with an endpoint of "0.0.0.0:4318"
```

* Add the receiver to all the *receiver:* sections in the pipelines
* Enable the **memory_limiter:** processor by adding it in all the *processor:* sections of the pipelines

```text
  - memory_limiter or [memory_limiter] array
```

* Add the following exporter:

```text
  debug: exporter
    verbosity: entry, set to detailed
```

Add it as an exporter in all *exporter:* sections of the pipelines

{{% /notice %}}

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
 Note that in the exercise above we give you all key elements in yaml format, you just need to correct them yourself.
 Pay attention to the format as the configuration of the agent is yaml based.

{{% /notice %}}

By using [https://www.otelbin.io/](https://www.otelbin.io/) to validate your agent.yaml, you can catch spelling and or configuration errors.  
If done correctly your configuration should look like this:

![otelbin1](../images/agent-1-1.png)

---

### Test & Validate

Run the following command to  test your config (make sure you use the right otel collector you downloaded):

```text
[LOCATION_OF_OTELCOLLECTOR]/otelcol --config=agent.yaml
```

If you have done everything correctly, the last line of the output should be :

```text
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261	Everything is ready. Begin running and processing data.
```

Now  start a new shell and create a file called **trace.json* and copy the following content:

```text
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

```text
curl -X POST -i http://localhost:4318/v1/traces \
-H "Content-Type: application/json" \
 -d @trace.json 
```

Your collector should show the following output:

 ```text
 2025-01-13T13:26:13.502+0100	info	Traces	{"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
2025-01-13T13:26:13.502+0100	info	ResourceSpans #0
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

Let's move on to adding a file exporter and use that to mimic our backend
