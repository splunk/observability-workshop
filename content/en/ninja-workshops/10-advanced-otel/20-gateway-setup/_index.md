---
title: Route data though a gateway  
linkTitle: 2. Gateway Setup
time: 10 minutes
weight: 20
---

### Gateway Setup

In the location where you are running the workshop on your machine, create a sub directory called **2-gateway**, then copy the last version of the agent.yaml across to the new directory.  
Move into the *[WORKSHOP]/2-gateway* directory and create a file called **gateway.yaml**  and copy the following starting config in it.

``` text
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:5318" # Note, the port number is 1000 higher then the regular port number since we going to run two collectors on the same machine
processors:
  memory_limiter:
    check_interval: 2s
    limit_mib: 512

exporters:
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors:
        - memory_limiter
      exporters: [ debug]
    metrics:
      receivers: [otlp]
      processors:
        - memory_limiter
      exporters: [ debug]
    logs:
      receivers: [otlp]
      processors:
        - memory_limiter
      exporters: [ debug]
```

Let's start with our next exercise:

{{% notice title="Exercise" style="green" icon="running" %}}

* Add the following exporter

```text
  file: exporter, name it /traces: 
    path: entry, with a value of "./gateway-trace.out"
```

* Configure file size constrains. Add the following to the file exporter:

```text
    rotation: section
      max_megabytes: entry with a value of 2    * This set the max size for the file exporter output
      max_backups: entry also with a value of 2 * This will set the max number rotational backups 
```

* Add it as the first exporter in the **traces:** pipeline.
* Repeat this two more time, name them */metrics* and */logs*, with path being *./gateway-metrics.out* and *gateway-logs.out* respectively and add them to the relevant pipeline

{{% /notice %}}

Verify your gateway.yaml with [https://www.otelbin.io/](https://www.otelbin.io/). If done correctly your view should look like this:

![otelbin1](../images/gateway-2-1.png)

---

### Test Gateway

Start an other Shell, make sure your in your workhop folder and run the following command  in the new shell to test your gateway config.

```text
[LOCATION_OF_OTELCOLLECTOR]/otelcol --config=gateway.yaml
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

* Add the following exporter

```text
  otlphttp: exporter
    endpoint: entry, with a value of "http://localhost:5318"   * using the port of the gateway   
    headers: entry,
      "X-SF-Token": entry, with a fake access token "FAKE_SPLUNK_ACCESS_TOKEN"  
  ```

* Add this as the first exporter to all the sections of the pipelines.  (Remove file and leave debug in place) 

{{% /notice %}}  
  Again validate it with 

![otelbingw2](../images/gateway-2-2.png)
---

### Validate setup

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
