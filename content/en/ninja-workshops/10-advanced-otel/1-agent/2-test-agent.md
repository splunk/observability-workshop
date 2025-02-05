---
title: 1.2 Test Configuration
linkTitle: 1.2 Test Configuration
weight: 2
---

Once you've updated the configuration, you’re ready to proceed to running the OpenTelemetry Collector with your new setup. This exercise sets the foundation for understanding how data flows through the OpenTelemetry Collector.

Start or reuse your initial terminal window, we will use this to run the `Agent`.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
To improve organization during the workshop, consider customizing your terminal windows or shells with unique names and colors. This will make it easier to identify and switch between them quickly.
{{% /notice %}}

Run the following command from the `1-agent` directory (ensure you’re using the correct OpenTelemetry Collector binary you downloaded):

```sh
../otelcol --config=agent.yaml
```

In this workshop, we use **macOS/Linux** commands by default. If you’re using Windows, adjust the commands as needed.

If everything is set up correctly, the first and last lines of the output should display:

```text
2025/01/13T12:43:51 settings.go:478: Set config to [agent.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.117.0/service.go:261 Everything is ready. Begin running and processing data.
```

{{% notice note %}}
On Windows, a dialog box may appear asking if you want to grant public and private network access to `otelcol.exe`. Click **"Allow"** to proceed.
{{%/ notice %}}

Instead of instrumenting an application, we will simulate sending trace data to the OpenTelemetry Collector using `cURL`. The trace data, formatted in JSON, represents what an instrumentation library would typically generate and send.

Open a second terminal window and navigate to the `[WORKSHOP]/1-agent` directory. In this new terminal (used for running `Tests`), create a new file named `trace.json` and copy the contents from one of the tabs below. Both tabs contain the same data, which includes a **span** that is part of a larger trace.

{{% tab title="trace.json" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"I'm a server span","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR>StarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}]}]}]}]}
```

{{% /tab %}}

This file will allow us to test how the OpenTelemetry Collector processes and send **spans** within a trace, without requiring actual application instrumentation.

{{% tab title="Updated Directory Structure" %}}

```text
[WORKSHOP]
├── 1-agent         # Module directory
│   └── agent.yaml  # OpenTelemetry Collector configuration file
│   └── trace.json  # Sample trace data
└── otelcol         # OpenTelemetry Collector binary
```

{{% /tab %}}

Execute the following command to send a **span** to the agent:

{{% tabs %}}
{{% tab title="cURL Command" %}}

```ps1
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

- `HTTP/1.1 200 OK`: Confirms the request was processed successfully.
- `{"partialSuccess":{}}`: Indicates 100% success, as the field is empty. In case of a partial failure, this field will include details about any failed parts.

{{% notice note %}}
On Windows, you may encounter the following error:
{{% textcolor color="red" weight="bold" %}}Invoke-WebRequest : Cannot bind parameter 'Headers'. Cannot convert the "Content-Type: application/json" ...{{% /textcolor %}}
To resolve this, use `curl.exe` instead of just `curl`.
{{% /notice %}}

Next, find the terminal window where your `Agent` is running and check the debug output. You should see log entries related to the span you just sent.  

Below, we've highlighted the first and last lines of the debug log for that span. To get the full context, review the complete debug output.

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
