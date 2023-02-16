---
title: Build a Distributed Trace
linkTitle: Build a Distributed Trace
weight: 99
---

This lab will make a tracing superhero out of you!

In this lab you will learn how a distributed trace is constructed for a small serverless application that runs on [AWS Lambda](https://aws.amazon.com/lambda/), producing and consuming your message via [AWS Kinesis](https://aws.amazon.com/kinesis/).

![image](https://user-images.githubusercontent.com/5187861/219358330-50022c0d-7882-47a3-a047-c4edda81de0d.png)

## Pre-Requisites

You should already have the lab content available on your ec2 lab host.

Ensure that this lab's required folder `o11y-lambda-lab` is on your home directory:

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
cd ~ && ls
```

{{% /tab %}}
{{% tab name="Output" %}}
o11y-lambda-lab
{{% /tab %}}
{{< /tabs >}}

{{% notice style="note" %}}
If you don't see it, fetch the lab contents by running the following command:

``` bash
git clone https://github.com/kdroukman/o11y-lambda-lab.git
```

{{% /notice %}}

### 1. Set Environment Variables

In your Splunk Observability Cloud Organisation (Org) obtain your Access Token and Realm Values.

Please reset your environment variables from the earlier lab. Take care that for this lab we may be using different names - make sure to match the Environment Variable names bellow.

{{< tabs >}}
{{% tab name="Export Environment Variables" %}}

``` bash
export ACCESS_TOKEN=CHANGE_ME \
export REALM=CHANGE_ME \
export PREFIX=$(hostname)
```

{{% /tab %}}
{{< /tabs >}}

### 2. Update Auto-instrumentation serverless template

Update your auto-instrumentation Serverless template to include new values from the Enviornment variables.

{{< tabs >}}
{{% tab name="Substitute Environment Variables" %}}

```bash
cat ~/o11y-lambda-lab/auto/serverless_unset.yml | envsubst > ~/o11y-lambda-lab/auto/serverless.yml
```

{{% /tab %}}
{{< /tabs >}}

Examine the output of the updated serverless.yml contents (you may need to scroll up to the relevant section).

{{< tabs >}}
{{% tab name="Check file contents" %}}

``` bash
cat ~/o11y-lambda-lab/auto/serverless.yml
```

{{% /tab %}}
{{% tab name="Expected Content" %}}

``` text
# USER SET VALUES =====================              
custom: 
  accessToken: <updated to your Access Token>
  realm: <updated to your Realm>
  prefix: <updated to your Hostname>
#====================================== 
```

{{% /tab %}}
{{< /tabs >}}

### 3. Update Manual instrumentation template

Update your manual instrumentation Serverless template to include new values from the Enviornment variables.

{{< tabs >}}
{{% tab name="Substitute Environment Variables" %}}

``` bash
cat ~/o11y-lambda-lab/manual/serverless_unset.yml | envsubst > ~/o11y-lambda-lab/manual/serverless.yml
```

{{% /tab %}}
{{< /tabs >}}

Examine the output of the updated serverless.yml contents (you may need to scroll up to the relevant section).

{{< tabs >}}
{{% tab name="Check file contents" %}}

``` bash
cat ~/o11y-lambda-lab/manual/serverless.yml
```

{{% /tab %}}
{{% tab name="Expected Content" %}}

``` text
# USER SET VALUES =====================              
custom: 
  accessToken: <updated to your Access Token>
  realm: <updated to your Realm>
  prefix: <updated to your Hostname>
#====================================== 
```

{{% /tab %}}
{{< /tabs >}}

### 4. Set your AWS Credentials

You will be provided with AWS Access Key ID and AWS Secret Access Key values - substitue these values in place of `AWS_ACCESS_KEY_ID` and `AWS_ACCESS_KEY_SECRET` in the bellow command:

{{< tabs >}}
{{% tab name="Set AWS Credentials" %}}

``` bash
sls config credentials --provider aws --key AWS_ACCCESS_KEY_ID --secret AWS_ACCESS_KEY_SECRET
```

{{% /tab %}}
{{< /tabs >}}

This command will create a file `~/.aws/credentials` with your AWS Credentails populated.

Note that we are using `sls` here, which is a [Serverless](https://www.serverless.com/) framework for developing and deploying AWS Lambda functions. We will be using this command throughout the lab.

Now you are set up and ready go!

## Auto-Instrumentation

Navigate to the `auto` directory that contains auto-instrumentation code.

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
cd ~/o11y-lambda-lab/auto
```

{{% /tab %}}
{{< /tabs >}}

Inspect the contents of the files in this directory.
Take a look at the `serverless.yml` template.

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
cat serverless.yml
```

{{% /tab %}}
{{< /tabs >}}

1. Can you identify which AWS entities are being created by this template?
2. Can you identify where OpenTelemetry instrumentation is being set up?
3. Can you determine which instrumentation information is being provided by the Environment Variables?

You should see the Splunk OpenTelemetry Lambda layer being added to each fuction.

``` text
layers:
      - arn:aws:lambda:us-east-1:254067382080:layer:splunk-apm:70
```

You can see the relevant layer ARNs (Amazon Resource Name) and latest versions for each AWS region here: <https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md>

You should also see a section where the Environment variables that are being set.

``` text
 environment:
      AWS_LAMBDA_EXEC_WRAPPER: /opt/nodejs-otel-handler
      OTEL_RESOURCE_ATTRIBUTES: deployment.environment=${self:custom.prefix}-apm-lambda
      OTEL_SERVICE_NAME: consumer-lambda
      SPLUNK_ACCESS_TOKEN: ${self:custom.accessToken}
      SPLUNK_REALM: ${self:custom.realm}
```

Using the environment variables we are configuring and enriching our auto-instrumentation.

Here we provide minimum information, such as NodeJS wrapper location in the Splunk APM Layer, environment name, service name, and our Splunk Org credentials. We are sending trace data directly to Splunk Observability Cloud. You could alternatively export traces to an OpenTelemetry Collector set up in [Gateway](https://opentelemetry.io/docs/collector/deployment/#gateway) mode.

Take a look at the function code.

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
cat handler.js
```

{{% /tab %}}
{{< /tabs >}}

1. Can you identify the code for **producer** function?
2. Can you identify the code for **consumer** function?

Notice there is no mention of Splunk or OpenTelemetry in the code. We are adding the instrumentation using the Lambda layer and Environment Variables only.

### Deploy your Lambdas

Run the following command to deploy your Lambda Functions:

{{< tabs >}}
{{% tab name="Deploy Command" %}}

``` bash
sls deploy
```

{{% /tab %}}
{{% tab name="Expected Output" %}}

``` text
Deploying hostname-lambda-lab to stage dev (us-east-1)
...
...
endpoint: POST - https://randomstring.execute-api.us-east-1.amazonaws.com/dev/producer
functions:
  producer: hostname-lambda-lab-dev-producer (1.6 kB)
  consumer: hostname-lambda-lab-dev-consumer (1.6 kB)
```

{{% /tab %}}
{{< /tabs >}}

This command will follow the instructions in your `serverless.yml` template to create your Lambda functions and your Kinesis stream.
Note it may take a *1-2 minutes* to execute.

{{% notice style="note" %}}
`serverless.yml` is in fact a CloudFormation template. CloudFormation is an infrastructure as code service from AWS. You can read more about it here - <https://aws.amazon.com/cloudformation/>
{{% /notice %}}

Check the details of your serverless functions:

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
sls info
```

{{% /tab %}}
{{< /tabs >}}

Take note of your endpoint value:

![image](https://user-images.githubusercontent.com/5187861/219366650-2babbe19-8253-43a0-8521-f47c1dda7200.png)

### Send some Traffic

Use the `curl` command to send a payload to your **producer** function.
Note the command option `-d` is followed by your message payload.

Try changing the value of `name` to your name and telling the Lambda function about your `superpower`.
Replace `YOUR_ENDPOINT` with the endpoint from your previous step.

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
curl -d '{ "name": "CHANGE_ME", "superpower": "CHANGE_ME" }' YOUR_ENDPOINT
```

{{% /tab %}}
{{< /tabs >}}

For example:

``` text
curl -d '{ "name": "Kate", "superpower": "Distributed Tracing" }' https://xvq043lj45.execute-api.us-east-1.amazonaws.com/dev/producer
```

You should see the following output if your message is successful:

``` json
{"message":"Message placed in the Event Stream: hostname-eventSteam"}
```

If unsuccessful, you will see:

``` json
{"message": "Internal server error"}
```

If this occurs, ask one of the lab facilitators for assistance.

If you see a success message, generate more load: *re-send that messate **5+ times***.
You should keep seeing a success message after each send.

Check the lambda logs output.

#### Producer function logs

{{< tabs >}}
{{% tab name="Producer Function Logs" %}}

``` bash
sls logs -f producer
```

{{% /tab %}}
{{< /tabs >}}

#### Consumer function logs

{{< tabs >}}
{{% tab name="Consumer Function Logs" %}}

``` bash
sls logs -f consumer
```

{{% /tab %}}
{{< /tabs >}}

Examine the logs carefully. Do you see OpenTelemetry being loaded? Look out for lines with `splunk-extension-wrapper`.

### Find your Lambda data in Splunk APM

Now it's time to check how your Lambda traffic has been captured in Splunk APM.

Navigate to your [Splunk Observability Cloud](https://app.us1.signalfx.com)

Select APM from the Main Menu and then select your APM Environment. Your APM environment should be in the format `$(hostname)-apm-lambda` where the hostname value is a four letter name of your lab host. (Check it by looking at your command prompt, or by running `echo $(hostname)`)

{{% notice style="note" %}}
It may take a few minutes for you traces to appear in Splunk APM. Try hitting refresh on your browser until you find your environement name in the list of Envrionments
{{% /notice %}}

![image](https://user-images.githubusercontent.com/5187861/219368081-20a1522e-a908-40d8-b635-942bffdbb0bd.png)

Go to Explore the Service Map to see the Dependencies between your Lambda Functions.

![image](https://user-images.githubusercontent.com/5187861/219001784-a25e7c9f-981d-49b9-b6df-f39d2bff0975.png)

You should be able to see the `producer-lambda` and the call it is making to `Kinesis` service. What about your `consumer-lambda`?
![image](https://user-images.githubusercontent.com/5187861/219368350-5bebb65b-d658-42be-9895-5d39a8d60a2d.png)

Click into *Traces* and examine some traces that container **procuder** function calls and traces with **consumer** function calls.
![image](https://user-images.githubusercontent.com/5187861/219002535-d11afd2f-9134-4e1b-87fb-f3af47969372.png)

We can see the `producer-lambda` putting a Record on the Kinesis stream. But the action of `consumer-function` is disconnected!

This is because the **Trace Context** is not being propagated.

This is not something that is supported automatically Out-of-the-Box by Kinesis service at the time of this lab. Our Distributed Trace stops at *Kinesis* inferred service, and we can't see the propagation any further.

Not yet...

Let's see how we work around this in the next section of this lab.

## Manual Instrumentation

Navigate to the `manual` directory that contains manually instrumentated code.

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
cd ~/o11y-lambda-lab/manual
```

{{% /tab %}}
{{< /tabs >}}

Inspect the contents of the files in this directory.
Take a look at the `serverless.yml` template.

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
cat serverless.yml
```

{{% /tab %}}
{{< /tabs >}}

Do you see any difference from the same file in your `auto` directory?

You can try to compare them with a `diff` command:

{{< tabs >}}
{{% tab name="Diff Command" %}}

``` bash
diff ~/o11y-lambda-lab/auto/serverless.yml ~/o11y-lambda-lab/manual/serverless.yml 
```

{{% /tab %}}
{{% tab name="Expected Output" %}}

``` text
19c19
< #======================================    
---
> #======================================   
```

{{% /tab %}}
{{< /tabs >}}

There is no difference! *(Well, there shouldn't be. Ask your lab facilitator to assist you if there is)*

Now compare `handler.js` it with the same file in `auto` directory using the `diff` command:

{{< tabs >}}
{{% tab name="Diff Command" %}}

``` bash
diff ~/o11y-lambda-lab/auto/handler.js ~/o11y-lambda-lab/manual/handler.js 
```

{{% /tab %}}
{{< /tabs >}}

Look at all these differences!

*You may wish to view the entire file with `cat handler.js` command and examine its content.*

Notice how we are now importing some OpenTelemetry libraries directly into our function to handle some of the manual instrumenation tasks we require.

``` text
const otelapi  = require('@opentelemetry/api');
const otelcore = require('@opentelemetry/core');
```

We are using <https://www.npmjs.com/package/@opentelemetry/api> to manipulate the tracing logic in our functions.
We are using <https://www.npmjs.com/package/@opentelemetry/core> to access the **Propagator** objects that we will use to manually propagate our context with.

### Inject Trace Context in Producer Function

The bellow code executes the following steps inside the Producer function:

1. Get the current Active Span.
2. Create a Propagator.
3. Initialize a context carrier object.
4. Inject the context of the active span into the carrier object.
5. Modify the record we are about to put on our Kinesis stream to include the carrier that will carry the active span's context to the consumer.

``` text
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

#### Extract Trace Context in Consumer Function

The bellow code executes the following steps inside the Consumer function:

1. Extract the context that we obtained from the Producer into a carrier object.
2. Create a Propagator.
3. Extract the context from the carrier object in Customer function's parent span context.
4. Start a new span with the parent span context.
5. Bonus: Add extra attributes to your span, including custom ones with the values from your message!
6. Once completed, end the span.

``` text
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

### Re-deploy your Lambdas

While remaining in your `manual` directory, run the following commandd to re-deploy your Lambda Functions:

{{< tabs >}}
{{% tab name="Deploy Producer Code" %}}

``` bash
sls deploy -f producer
```

{{% /tab %}}
{{% tab name="Expected Output" %}}

``` text
Deploying function producer to stage dev (us-east-1)

✔ Function code deployed (6s)
Configuration did not change. Configuration update skipped. (6s)
```

{{% /tab %}}
{{< /tabs >}}

{{< tabs >}}
{{% tab name="Deploy Consumer Code" %}}

``` bash
sls deploy -f consumer
```

{{% /tab %}}
{{% tab name="Expected Output" %}}

``` text
Deploying function consumer to stage dev (us-east-1)

✔ Function code deployed (6s)
Configuration did not change. Configuration update skipped. (6s)
```

{{% /tab %}}
{{< /tabs >}}

Note that this deployment now only updates the code changes within the function. Our configuration remains the same.

Check the details of your serverless functions:

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
sls info
```

{{% /tab %}}
{{< /tabs >}}

You endpoint value should remain the same:

![image](https://user-images.githubusercontent.com/5187861/219371979-4e474746-2633-4824-9d7a-1b39d3d2ce3f.png)

### Send some Traffic again

Use the `curl` command to send a payload to your **producer** function.
Note the command option `-d` is followed by your message payload.

Try changing the value of `name` to your name and telling the Lambda function about your `superpower`.
Replace `YOUR_ENDPOINT` with the endpoint from your previous step.

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
curl -d '{ "name": "CHANGE_ME", "superpower": "CHANGE_ME" }' YOUR_ENDPOINT
```

{{% /tab %}}
{{< /tabs >}}

For example:

``` text
curl -d '{ "name": "Kate", "superpower": "Distributed Tracing" }' https://xvq043lj45.execute-api.us-east-1.amazonaws.com/dev/producer
```

You should see the following output if your message is successful:

``` json
{"message":"Message placed in the Event Stream: hostname-eventSteam"}
```

If unsuccessful, you will see:

``` json
{"message": "Internal server error"}
```

If this occurs, ask one of the lab facilitators for assistance.

If you see a success message, generate more load: *re-send that messate **5+ times***. You should keep seeing a success message after each send.

Check the lambda logs output.

{{< tabs >}}
{{% tab name="Producer Function Logs" %}}

``` bash
sls logs -f producer
```

{{% /tab %}}
{{< /tabs >}}

{{< tabs >}}
{{% tab name="Consumer Function Logs" %}}

``` bash
sls logs -f consumer
```

{{% /tab %}}
{{< /tabs >}}

Examine the logs carefully. Do you notice the difference?

Note that we are logging our Record together with the Trace context that we have added to it. Copy one of the underlined sub-sections of your trace parent context, and save it for later.

![image](https://user-images.githubusercontent.com/5187861/219372916-ed1afce5-176f-4baf-a9a3-0aae29e3f01b.png)

### Find your updated Lambda data in Splunk APM

Navigate back to APM in [Splunk Observabilty Cloud](https://app.us1.signalfx.com/#/apm)

Go back to your Service Dependency map. Notice the difference?

![image](https://user-images.githubusercontent.com/5187861/219373312-0d556475-9f27-4729-af38-ac94f0773c5c.png)

You should be able to see the **consumer-lambda** now clearly connected to the **producer-lambda**.

Remember the value you copied from your producer logs? You can run `sls logs -f consumer` command again on your EC2 lab host to fetch one.

Take that value, and paste it into trace search:

![image](https://user-images.githubusercontent.com/5187861/219373635-cc5a5841-5afb-49f9-baea-9d4d45aabfb6.png)

Click on *Go* and you should be able to find the logged Trace:

![image](https://user-images.githubusercontent.com/5187861/219374024-de32aa68-f34a-43eb-8f00-5cc698864b00.png)

Notice that the **Trace ID** is something that makes up the trace *context* that we propagated.

You can read up on the two common propagation standards:

1. W3C: <https://www.w3.org/TR/trace-context/#traceparent-header>
2. B3: <https://github.com/openzipkin/b3-propagation#overall-process>

Which one are we using? *It should be self-explanatory from the Propagator we are creating in the Functions*

**Bonus Question:** What happens if we mix and match the W3C and B3 headers?

Expand the **consumer-lambda** span. Can you find the attributes from your message?

![image](https://user-images.githubusercontent.com/5187861/219374303-d143515b-d1b1-46b4-bd03-0c4653ea08c0.png)

## Before you Go

Please kindly clean up your lab using the following command:

{{< tabs >}}
{{% tab name="Remove Functions" %}}

``` bash
sls remove
```

{{% /tab %}}
{{< /tabs >}}

## Conclusion

Congratuations on finishing the lab. You have seen how we complement auto-instrumentation with manual steps to force **Producer** function's context to be sent to **Consumer** function via a Record put on a Kinesis stream. This allowed us to build the expected Distributed Trace.

![image](https://user-images.githubusercontent.com/5187861/219375907-5a5e23ce-b9bb-4939-865d-7dbbaa668c53.png)

You can now built out a Trace manually by linking two different functions together. This is very powerful when your auto-instrumenation, or third-party systems, do not support context propagation out of the box.
