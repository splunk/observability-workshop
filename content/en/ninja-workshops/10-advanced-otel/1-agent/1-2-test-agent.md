---
title: 1.2 Test Agent Configuration
linkTitle: 1.2 Test Agent Configuration
weight: 2
---

You’re ready to start the OpenTelemetry Collector with the newly created `agent.yaml`. This exercise sets the foundation for understanding how data flows through the OpenTelemetry Collector.

{{% notice title="Exercise" style="green" icon="running" %}}

**Find your Agent terminal window**:

1. Change into the `[WORKSHOP]/1-agent` folder
2. Run the following command:

```sh { title="Agent" }
../otelcol --config=agent.yaml
```

In this workshop, we use **macOS/Linux** commands by default. If you’re using Windows, adjust the commands as needed i.e. use `./otelcol.exe`.

{{% /notice %}}

> [!note]
> On Windows, a dialog box may appear asking if you want to grant public and private network access to `otelcol.exe`. Click **"Allow"** to proceed.

{{% notice title="Exercise" style="green" icon="running" %}}

**Verify debug output**: If everything is set up correctly, the first and last lines of the output should display:

```text
2025/01/13T12:43:51 settings.go:478: Set config to [agent.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.117.0/service.go:261 Everything is ready. Begin running and processing data.
```

**Create a test span file**: Rather than instrumenting an application, we’ll simulate sending trace data to the OpenTelemetry Collector using **curl**. The JSON-formatted trace data mimics what an instrumentation library would generate, allowing us to test the Collector’s processing logic.

1. Open your **Tests Terminal** window and navigate to the `[WORKSHOP]/1-agent` directory.  
2. Create a new file named **trace.json** and paste the following span data into it:  

```json { title="trace.json" }
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"I'm a server span","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR>StarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}]}]}]}]}
```

This file enables testing how the OpenTelemetry Collector processes and sends spans as part of a trace—without requiring actual application instrumentation.

```text { title="Updated Directory Structure" }
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
│   └── trace.json  # Sample trace data
└── otelcol         # OpenTelemetry Collector binary
```

**Send a test span**: Run the following command to send a **span** to the agent:

{{% tabs %}}
{{% tab title="cURL Command" %}}

```sh
 curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

{{% /tab %}}
{{% tab title="cURL Response" %}}

```text
HTTP/1.1 200 OK
Content-Type: application/json
Date: Mon, 27 Jan 2025 09:51:02 GMT
Content-Length: 21

{"partialSuccess":{}}%
 ```

{{% /tab %}}
{{% /tabs %}}

{{% notice info %}}

1. `HTTP/1.1 200 OK`: Confirms the request was processed successfully.
2. `{"partialSuccess":{}}`: Indicates 100% success, as the field is empty. In case of a partial failure, this field will include details about any failed parts.

{{% /notice %}}
{{% /notice %}}

{{% notice note %}}
On Windows, you may encounter the following error:
{{% textcolor color="red" weight="bold" %}}Invoke-WebRequest : Cannot bind parameter 'Headers'. Cannot convert the "Content-Type: application/json" ...{{% /textcolor %}}
To resolve this, use `curl.exe` instead of just `curl`.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

**Verify Debug Output**:

1. Find the **Agent** terminal window and check the collector's debug output. You should see the Debug entries related to the span you just sent.  
2. We are showing the first and last lines of the debug log for that span. To get the full context, Use the **Complete Debug Output** Button to review.

```text
2025-02-03T12:46:25.675+0100    info ResourceSpans #0
<snip>
        {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

{{% expand title="{{% badge style=primary icon=scroll %}}Complete Debug Output{{% /badge %}}" %}}

```text
2025-02-03T12:46:25.675+0100    info ResourceSpans #0  
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
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.account_password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
        {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

{{% /expand %}}

{{% /notice %}}
