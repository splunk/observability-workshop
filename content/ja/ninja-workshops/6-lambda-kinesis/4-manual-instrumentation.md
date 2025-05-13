---
title: Manual Instrumentation
linkTitle: 4. Manual Instrumentation
weight: 4
---

The second part of our workshop will focus on demonstrating how manual instrumentation with OpenTelemetry empowers us to enhance telemetry collection. More specifically, in our case, it will enable us to propagate trace context data from the `producer-lambda` function to the `consumer-lambda` function, thus enabling us to see the relationship between the two functions, even across Kinesis Stream, which currently does not support automatic context propagation.

### The Manual Instrumentation Workshop Directory & Contents

Once again, we will first start by taking a look at our operating directory, and some of its files. This time, it will be `o11y-lambda-workshop/manual` directory. This is where all the content for the manual instrumentation portion of our workshop resides.

#### The `manual` directory

- Run the following command to get into the `o11y-lambda-workshop/manual` directory:

  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- Inspect the contents of this directory with the `ls` command:

  ```bash
  ls
  ```

  - _The output should include the following files and directories:_

    ```bash
    handler             outputs.tf          terraform.tf        variables.tf
    main.tf             send_message.py     terraform.tfvars
    ```

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Do you see any difference between this directory and the auto directory when you first started?
{{% /notice %}}

#### Compare `auto` and `manual` files

Let's make sure that all these files that LOOK the same, are actually the same.

- Compare the `main.tf` files in the `auto` and `manual` directories:

  ```bash
  diff ~/o11y-lambda-workshop/auto/main.tf ~/o11y-lambda-workshop/manual/main.tf
  ```

  - There is no difference! _(Well, there shouldn't be. Ask your workshop facilitator to assist you if there is)_

- Now, let's compare the `producer.mjs` files:

  ```bash
  diff ~/o11y-lambda-workshop/auto/handler/producer.mjs ~/o11y-lambda-workshop/manual/handler/producer.mjs
  ```

  - There's quite a few differences here!

- You may wish to view the entire file and examine its content

  ```bash
  cat ~/o11y-lambda-workshop/handler/producer.mjs
  ```

  - Notice how we are now importing some OpenTelemetry objects directly into our function to handle some of the manual instrumentation tasks we require.

  ```js
  import { context, propagation, trace, } from "@opentelemetry/api";
  ```

  - We are importing the following objects from [@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) to propagate our context in our producer function:
    - context
    - propagation
    - trace

- Finally, compare the `consumer.mjs` files:

  ```bash
  diff ~/o11y-lambda-workshop/auto/handler/consumer.mjs ~/o11y-lambda-workshop/manual/handler/consumer.mjs
  ```

  - Here also, there are a few differences of note. Let's take a closer look

    ```bash
    cat handler/consumer.mjs
    ```

    - In this file, we are importing the following [@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) objects:
      - propagation
      - trace
      - ROOT_CONTEXT
    - We use these to extract the trace context that was propagated from the producer function
    - Then to add new span attributes based on our `name` and `superpower` to the extracted trace context

#### Propagating the Trace Context from the Producer Function

The below code executes the following steps inside the producer function:

1. Get the tracer for this trace
2. Initialize a context carrier object
3. Inject the context of the active span into the carrier object
4. Modify the record we are about to pu on our Kinesis stream to include the carrier that will carry the active span's context to the consumer

```js
...
import { context, propagation, trace, } from "@opentelemetry/api";
...
const tracer = trace.getTracer('lambda-app');
...
  return tracer.startActiveSpan('put-record', async(span) => {
    let carrier = {};
    propagation.inject(context.active(), carrier);
    const eventBody = Buffer.from(event.body, 'base64').toString();
    const data = "{\"tracecontext\": " + JSON.stringify(carrier) + ", \"record\": " + eventBody + "}";
    console.log(
      `Record with Trace Context added:
      ${data}`
    );

    try {
      await kinesis.send(
        new PutRecordCommand({
          StreamName: streamName,
          PartitionKey: "1234",
          Data: data,
        }),
        message = `Message placed in the Event Stream: ${streamName}`
      )
...
    span.end();
```

#### Extracting Trace Context in the Consumer Function

The below code executes the following steps inside the consumer function:

1. Extract the context that we obtained from `producer-lambda` into a carrier object.
2. Extract the tracer from current context.
3. Start a new span with the tracer within the extracted context.
4. Bonus: Add extra attributes to your span, including custom ones with the values from your message!
5. Once completed, end the span.

```js
import { propagation, trace, ROOT_CONTEXT } from "@opentelemetry/api";
...
      const carrier = JSON.parse( message ).tracecontext;
      const parentContext = propagation.extract(ROOT_CONTEXT, carrier);
      const tracer = trace.getTracer(process.env.OTEL_SERVICE_NAME);
      const span = tracer.startSpan("Kinesis.getRecord", undefined, parentContext);

      span.setAttribute("span.kind", "server");
      const body = JSON.parse( message ).record;
      if (body.name) {
        span.setAttribute("custom.tag.name", body.name);
      }
      if (body.superpower) {
        span.setAttribute("custom.tag.superpower", body.superpower);
      }
...
      span.end();
```

Now let's see the different this makes!
