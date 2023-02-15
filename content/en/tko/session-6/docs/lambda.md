---
title: Observability Lambda Lab
linkTitle: Observability Lambda Lab
weight: 99
---

Welcome to Observability Lambda Lab. This lab will make a tracing superhero out of you! Follow the steps bellow to set up and get started.

## Pre-Requisites

You should already have the lab content available on your ec2 lab host. You will need to update custom settings to your environment. Please follow the steps bellow to achieve that.

Ensure that your working lab folder is on your home directory:

``` bash
ls
```

Expected output:
You should see the directory `o11y-lambda-lab` in the list.

*Note:* If you don't see the directory, fetch the contents of this repository by running the following command:

``` bash
git clone -b master https://github.com/kdroukman/o11y-lambda-lab.git
```

In your Splunk Observability Cloud lab Organisation (Org) obtain your Access Token and Realm Values.

### 1. Set Environment Variables

Set the bellow environment variables:

``` bash
export ACCESS_TOKEN=<CHANGE_ME> \
export REALM=<CHANGE_ME> \
export PREFIX=$(hostname)
```

### 2. Update Auto-instrumentation template

Update your auto-instrumentation Serverless template.

```bash
cat ~/o11y-lambda-lab/auto/serverless_unset.yml | envsubst > ~/o11y-lambda-lab/auto/serverless.yml
```

Examine the output of the updated serverless.yml contents (you may need to scroll up to the relevant section).

``` bash
cat ~/o11y-lambda-lab/auto/serverless.yml
```

Locate the following section and confirm that the parameters have been set:
![image](https://user-images.githubusercontent.com/5187861/219005735-a494c35a-41c4-4350-930a-b9ce7e1f64ea.png)

### 3. Update Manual-instrumentation template

Update your manual-instrumentation Serverless template.

``` bash
cat ~/o11y-lambda-lab/manual/serverless_unset.yml | envsubst > ~/o11y-lambda-lab/manual/serverless.yml
```

Examine the output of the updated serverless.yml contents (you may need to scroll up to the relevant section).

``` bash
cat ~/o11y-lambda-lab/manual/serverless.yml
```

Locate the following section and confirm that the parameters have been set:
![image](https://user-images.githubusercontent.com/5187861/219005735-a494c35a-41c4-4350-930a-b9ce7e1f64ea.png)

### 4. Set your AWS Credentials

Add your credntials file and populate it with your provided AWS Access Key ID and AWS Secret Access Key values.

``` bash
mkdir ~/.aws & vi ~/.aws/credentials
```

In `vi` editor paste the bellow and change to your Access Key values. (Hint: Hit letter `i` to set your Vi editor to Insert/Edit mode)

``` text
[default]
aws_access_key_id=<CHANGE ME>
aws_secret_access_key=<CHANGE ME>
```

Save your `credentials` file:

1. Hit `Esc` button to exit Insert mode in your Vi Editor
2. Press column `:` - this will give you access to command prompt within your Vi Editor
3. Key in `wq` and press `Enter`. This will write and quit your Vi Editor. i.e. Save.

Now you are set up and ready for this Lab.

## Auto-Instrumentation

Navigate to the `auto` directory that contains auto-instrumentation code.

``` bash
cd ~/o11y-lambda-lab/auto
```

Inspect the contents of the files in this directory.
Take a look at the `serverless.yml` template.

``` bash
cat serverless.yml
```

1. Can you identify which AWS entities are being created by this template?
2. Can you identify where OpenTelemetry instrumentation is being set up?
3. Can you determine which instrumentation information is being provided by the Environment Variables?

You should see the Splunk OpenTelemetry Lambda layer being added to each fuction.

![image](https://user-images.githubusercontent.com/5187861/219007839-fd96d1bb-c53d-4cfa-9533-c7982262459d.png)

You can see the relevant layer ARNs (Amazon Resource Name) and latest versions for each AWS region here: <https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md>

You should also see in the Environment variables that are being set.
![image](https://user-images.githubusercontent.com/5187861/219012413-fddbea72-3f5a-418f-9f8f-83cf2305d976.png)

Using the environment variables we are specifying to use the NodeJS function wrapper, since our Lambda is written in NodeJS. We are also providing APM service name and environment name, as well as Access token and Realm details.
You should also see in the Environment variables that are being set. Using the environment variables we are specifying to use the NodeJS function wrapper, since our Lambda is written in NodeJS. We are also providing APM service name and environment name, as well as Access token and Realm details.

Take a look at the function code.

``` bash
cat handler.js
```

1. Can you identify the code for producer function?
2. Can you identify the code for consumer function?

Note that there is no mention of Splunk or OpenTelemetry in the code. We are adding the instrumentation using the Lambda layer and Environment Variables only.

### Deploy your Lambdas

Run the following command to deploy your Lambda Functions:

``` bash
serverless deploy
```

This command will follow the instructions in your `serverless.yml` template to create your Lambda functions and your Kinesis stream. Note it may take a couple of minutes to execute.

Expected output:

``` text
Deploying hostname-lambda-lab to stage dev (us-east-1)
...
...
endpoint: POST - https://randomstring.execute-api.us-east-1.amazonaws.com/dev/producer
functions:
  producer: hostname-lambda-lab-dev-producer (1.6 kB)
  consumer: hostname-lambda-lab-dev-consumer (1.6 kB)
```

{{% notice style="note" %}}
`serverless.yml` is in fact a CloudFormation template. CloudFormation is an infrastructure as code service from AWS. You can read more about it here - <https://aws.amazon.com/cloudformation/>
{{% /notice %}}

Check the details of your serverless functions:

``` bash
serverless info
```

Take note of your endpoint value:

![image](https://user-images.githubusercontent.com/5187861/219013249-bfa87ba1-f719-4287-8124-f95d87df83f5.png)

### Send some Traffic

Use the `curl` command to send a payload to your producer function. Note that the flat `-d` is followed by your payload. Try changing the value of `name` to your name and telling the Lambda function about your `superpower`.
Replace `YOUR_ENDPOINT` with the endpoint from your previous step.

``` bash
curl -d '{ "name": "CHANGE_ME", "superpower": "CHANGE_ME" }' YOUR_ENDPOINT
```

For example:
![image](https://user-images.githubusercontent.com/5187861/219024684-cd1853cf-8d9d-4fbb-af2f-96ba518622e3.png)

You should see the following output if your message is successful:

``` json
{"message":"Message planced in the Event Stream: hostname-eventSteam"}
```

If unsuccessful, you will see:

``` json
{"message": "Internal server error"}
```

Ask one of the lab facilitators for assistance.

If you see a success message, generate more load: re-send that messate 5+ times. You should keep seeing a success message after each send.

Now check the lambda logs output.

#### Producer function logs

``` bash
serverless logs -f producer
```

#### Consumer function logs

``` bash
serverless logs -f consumer
```

Examine the logs carefully. Do you see OpenTelemetry being loaded? Look out for lines with `splunk-extension-wrapper`.

### Find your Lambda data in Splunk APM

Now it's time to check how your Lambda traffic has been captured in Splunk APM.

Navigate to your Lab Organisation at [https://app.us1.signalfx.com]

Select APM from the Main Menu and then select your APM Environment. Your APM environment should be in the format `$(hostname)-lambda-lab` where the hostname value is a four letter name of your lab host. (Check it by looking at your command prompt, or by running `echo $(hostname)`)

{{% notice style="note" %}}
It may take a few minutes for you traces to appear in Splunk APM. Try hitting refresh on your browser until you find your environement name in the list of Envrionments
{{% /notice %}}

![image](https://user-images.githubusercontent.com/5187861/218997315-e3e5f6e1-fd7f-4267-8113-79ca748b9d77.png)

You should see your lambda function and Kinesis service show up in the map.

Go to Explore the service map for a better view.

![image](https://user-images.githubusercontent.com/5187861/219001784-a25e7c9f-981d-49b9-b6df-f39d2bff0975.png)

You should be able to see the `producer-lambda` and the call it is making to `Kinesis` service.
![image](https://user-images.githubusercontent.com/5187861/219001985-fbf431ac-010a-4b1b-a9b0-3bad6825c5b6.png)

What about your `consumer-lambda`? Where is it?

Click into *Traces* and examine one of the traces generated.
![image](https://user-images.githubusercontent.com/5187861/219002535-d11afd2f-9134-4e1b-87fb-f3af47969372.png)

We can see the `producer-lambda` putting a Record on the Kinesis stream. But we can't see the `consumer-function` consuming that record.

This is because the *Context* is not being propagated - this is not something that is supported automatically Out-of-the-Box for Kinesis service at the time of this lab. Our Distributed Trace stops at *Kinesis* inferred service and we can't see the propagation any further.

Not yet...

Let's see how we work around this in the next section of this lab.

## Manual Instrumentation

Navigate to the `manual` directory that contains manually instrumentated code.

``` bash
cd ~/o11y-lambda-lab/manual
```

Inspect the contents of the files in this directory.
Take a look at the `serverless.yml` template.

``` bash
cat serverless.yml
```

Do you see any difference from the same file in your `auto` directory?
You can try to compare them with a `diff` command:

``` bash
diff ~/o11y-lambda-lab/auto/serverless.yml ~/o11y-lambda-lab/manual/serverless.yml 
```

There is no difference! *(Well, there shouldn't be. Get a lab assistant to help you if there is)*

![image](https://user-images.githubusercontent.com/5187861/219018152-6b21a172-9447-4e36-9ce5-814438c5d427.png)

Take a look at the function code.

``` bash
cat handler.js
```

Compare it with the same file in `auto` directory using the `diff` command:

``` bash
diff ~/o11y-lambda-lab/auto/handler.js ~/o11y-lambda-lab/manual/handler.js 
```

Look at all these differences!

Notice how we are now importing some OpenTelemetry libraries directly into our function to handle some of the manual instrumenation tasks we require.

We are using <https://www.npmjs.com/package/@opentelemetry/api> to manipulate the tracing logic in our functions.
We are using <https://www.npmjs.com/package/@opentelemetry/core> to access the **Propagator** objects that we will use to manually propagate our context with.

The bellow code executes the following steps inside the Producer function:

1. Get the current Active Span.
2. Create a Propagator.
3. Initialize a context carrier object.
4. Inject the context of the active span into the carrier object.
5. Modify the record we are about to put on our Kinesis stream to include the carrier that will carry the active span's context to the consumer.

![image](https://user-images.githubusercontent.com/5187861/219020209-33a3b24a-b3a7-4d80-865f-fbf3a8d8754a.png)

The bellow code executes the following steps inside the Consumer function:

1. Extract the context that we obtained from the Producer into a carrier object.
2. Create a Propagator.
3. Extract the context from the carrier object in Customer function's parent span context.
4. Start a new span with the parent span context.
5. Bonus: Add extra attributes to your span, including custom ones with the values from your message!
6. Once completed, end the span.

![image](https://user-images.githubusercontent.com/5187861/219020986-0ed2f8b9-8842-47cb-ac30-fdf9851015e6.png)

Now let's see the difference this makes.

### Re-deploy your Lambdas

While remaining in your `manual` directory, run the following command to deploy your Lambda Functions:

``` bash
serverless deploy
```

This command will follow the instructions in your `serverless.yml` template to update your Lambda functions with new `handler.js` code.

Expected output:

``` text
Deploying hostname-lambda-lab to stage dev (us-east-1)
...
...
endpoint: POST - https://randomstring.execute-api.us-east-1.amazonaws.com/dev/producer
functions:
  producer: hostname-lambda-lab-dev-producer (1.6 kB)
  consumer: hostname-lambda-lab-dev-consumer (1.6 kB)
```

Check the details of your serverless functions:

``` bash
serverless info
```

Take note of your endpoint value. It should remain the same:

![image](https://user-images.githubusercontent.com/5187861/219013249-bfa87ba1-f719-4287-8124-f95d87df83f5.png)

### Send some Traffic again

Use the `curl` command to send a payload to your producer function. Note that the flat `-d` is followed by your payload. Try changing the value of `name` to your name and telling the Lambda function about your `superpower`.
Replace `YOUR_ENDPOINT` with the endpoint from your previous step.

``` bash
curl -d '{ "name": "CHANGE_ME", "superpower": "CHANGE_ME" }' YOUR_ENDPOINT
```

For example:
![image](https://user-images.githubusercontent.com/5187861/219024684-cd1853cf-8d9d-4fbb-af2f-96ba518622e3.png)

You should see the following output if your message is successful:

``` json
{"message":"Message planced in the Event Stream: hostname-eventSteam"}
```

If unsuccessful, you will see:

``` json
{"message": "Internal server error"}
```

Ask one of the lab facilitators for assistance.

If you see a success message, generate more load: re-send that messate 5+ times. You should keep seeing a success message after each send.

Now check the lambda logs output.

{{< tabs >}}
{{% tab name="Producer function logs" %}}

``` bash
serverless logs -f producer
```

{{% /tab %}}
{{< /tabs >}}

{{< tabs >}}
{{% tab name="Consumer function logs" %}}

``` bash
serverless logs -f consumer
```

{{% /tab %}}
{{< /tabs >}}

Examine the logs carefully. Do you notice the difference?

Note that we are logging our Record value built inside the Producer function. Copy one of the underlined sub-sections of your trace parent context, and save it for later.

![image](https://user-images.githubusercontent.com/5187861/219031025-61ae5852-dabb-4c86-a215-aead651ab9c7.png)

### Find your updated Lambda data in Splunk APM

Navigate back to APM in Splunk Observabilty Cloud - <https://app.us1.signalfx.com/#/apm>

Navigate to Explore the Service Dependency Map again.

![image](https://user-images.githubusercontent.com/5187861/219030534-9dc94124-16e1-4350-b63f-0a4e4c8aa640.png)

You should be able to see the *consumer-lambda* now clearly connected to the *producer-lambda*.

Remember the value you copied from your producer logs? You can run `serverless logs -f producer` command again on your EC2 lab host to fetch one.

Take that value, and paste it into trace search:

![image](https://user-images.githubusercontent.com/5187861/219031728-c926f2e4-78c7-438f-ad38-98f6facbad66.png)

Click on *Go* and you should be able to find the logged Trace:

![image](https://user-images.githubusercontent.com/5187861/219032326-becba400-c08d-4762-93b5-ba3f2c2322cb.png)

Note how the *Trace ID* is something that makes up the trace *context* that we propagated.

You can read up on the two common propagation standards:

1. W3C: <https://www.w3.org/TR/trace-context/#traceparent-header>
2. B3: <https://github.com/openzipkin/b3-propagation#overall-process>

Which one are we using? *It should be self-explanatory from the Propagator we are creating in the Functions*

**Bonus Question:** What happens if we mix and match the W3C and B3 headers?

Expand the `consumer-lambda` span. Can you find the attributes from your message?

![image](https://user-images.githubusercontent.com/5187861/219032913-70dfc212-f5d7-4468-bda8-5041ea3e21e0.png)

## Conclusion

Congratuations on finishing the lab. You can now built out a Trace manually by linking two different functions together. This is very powerful, when auto-instrumenation, or third-party systems do not support context propagation out of the box.

Notice in the lab we used a combination of auto-instrumenation with some extra manual steps to do what we need to, in order to connect the trace. This is a common way to instrument, and workaround any instrumentation challenges you may face.
