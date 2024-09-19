---
title: Manual Instrumentation
linkTitle: 4. Manual Instrumentation
weight: 4
---

## Manual Instrumentation

Navigate to the manual directory that contains manually instrumentated code.

{{< tabs >}} {{% tab title="Command" %}}

``` bash
cd ~/o11y-lambda-lab/manual
```

{{% /tab %}} {{< /tabs >}}

Inspect the contents of the files in this directory. Take a look at the serverless.yml template.

{{< tabs >}} {{% tab title="Command" %}}

``` bash
cat serverless.yml
```

{{% /tab %}} {{< /tabs >}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Do you see any difference from the same file in your auto directory?
{{% /notice %}}

You can try to compare them with a diff command:

{{< tabs >}} {{% tab title="Diff Command" %}}

``` bash
diff ~/o11y-lambda-lab/auto/serverless.yml ~/o11y-lambda-lab/manual/serverless.yml 
```

{{% /tab %}} {{% tab title="Expected Output" %}}

``` text
19c19
< #======================================    
---
> #======================================   
```

{{% /tab %}} {{< /tabs >}}

There is no difference! (Well, there shouldn't be. Ask your lab facilitator to assist you if there is)

Now compare handler.js it with the same file in auto directory using the diff command:

{{< tabs >}} {{% tab title="Diff Command" %}}

``` bash
diff ~/o11y-lambda-lab/auto/handler.js ~/o11y-lambda-lab/manual/handler.js 
```

{{% /tab %}} {{< /tabs >}}

Look at all these differences!

You may wish to view the entire file with `cat handler.js` command and examine its content.

Notice how we are now importing some OpenTelemetry libraries directly into our function to handle some of the manual instrumenation tasks we require.

``` js
const otelapi  = require('@opentelemetry/api');
const otelcore = require('@opentelemetry/core');
```

We are using [https://www.npmjs.com/package/@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) to manipulate the tracing logic in our functions. We are using [https://www.npmjs.com/package/@opentelemetry/core](https://www.npmjs.com/package/@opentelemetry/core) to access the Propagator objects that we will use to manually propagate our context with.

## Inject Trace Context in Producer Function

The below code executes the following steps inside the Producer function:

1. Get the current Active Span.
2. Create a Propagator.
3. Initialize a context carrier object.
4. Inject the context of the active span into the carrier object.
5. Modify the record we are about to put on our Kinesis stream to include the carrier that will carry the active span's context to the consumer.

```  js
const activeSpan = otelapi.trace.getSpan(otelapi.context.active());
const propagator = new otelcore.W3CTraceContextPropagator();
let carrier = {};
propagator.inject(otelapi.trace.setSpanContext(otelapi.ROOT_CONTEXT, activeSpan.spanContext()),
    carrier,
    otelapi.defaultTextMapSetter
  );
const data = "{\"tracecontext\": " + JSON.stringify(carrier) + ", \"record\":" + event.body + "}";
console.log(`Record with Trace Context added: 
  ${data}`);
```

## Extract Trace Context in Consumer Function

The bellow code executes the following steps inside the Consumer function:

1. Extract the context that we obtained from the Producer into a carrier object.
2. Create a Propagator.
3. Extract the context from the carrier object in Customer function's parent span context.
4. Start a new span with the parent span context.
5. Bonus: Add extra attributes to your span, including custom ones with the values from your message!
6. Once completed, end the span.

``` js
const carrier = JSON.parse( message ).tracecontext;
const propagator = new otelcore.W3CTraceContextPropagator();
const parentContext = propagator.extract(otelapi.ROOT_CONTEXT, carrier, otelapi.defaultTextMapGetter);
const tracer = otelapi.trace.getTracer(process.env.OTEL_SERVICE_NAME);
const span = tracer.startSpan("Kinesis.getRecord", undefined, parentContext);
                         
span.setAttribute("span.kind", "server");
const body = JSON.parse( message ).record;
if (body.name) {
    span.setAttribute("custom.tag.name", body.name);
}
 if (body.superpower) {
    span.setAttribute("custom.tag.superpower", body.superpower);
}
  --- function does some work
 span.end();
```

Now let's see the difference this makes.
