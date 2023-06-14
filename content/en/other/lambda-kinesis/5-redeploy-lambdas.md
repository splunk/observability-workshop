---
title: Redeploy Lambdas
linkTitle: 5. Redeploy Lambdas
weight: 5
---

## Re-deploy your Lambdas

While remaining in your manual directory, run the following commandd to re-deploy your Lambda Functions:

{{< tabs >}} {{% tab title="Deploy Producer Code" %}}

``` bash
sls deploy -f producer
```

{{% /tab %}} {{% tab title="Expected Output" %}}

``` text
Deploying function producer to stage dev (us-east-1)

✔ Function code deployed (6s)
Configuration did not change. Configuration update skipped. (6s)
```

{{% /tab %}} {{< /tabs >}}

{{< tabs >}} {{% tab title="Deploy Consumer Code" %}}

``` bash
sls deploy -f consumer
```

{{% /tab %}} {{% tab title="Expected Output" %}}

``` text
Deploying function consumer to stage dev (us-east-1)

✔ Function code deployed (6s)
Configuration did not change. Configuration update skipped. (6s)
```

{{% /tab %}} {{< /tabs >}}

Note that this deployment now only updates the code changes within the function. Our configuration remains the same.

Check the details of your serverless functions:

{{< tabs >}} {{% tab title="Command" %}}

``` bash
sls info
```

{{% /tab %}} {{< /tabs >}}

You endpoint value should remain the same:

![5-redeploy-1-endpoint-value](../images/5-redeploy-1-endpoint-value.png)

## Send some Traffic again

Use the `curl` command to send a payload to your producer function. Note the command option `-d` is followed by your message payload.

Try changing the value of name to your name and telling the Lambda function about your superpower. Replace `YOUR_ENDPOINT` with the endpoint from your previous step.

{{< tabs >}} {{% tab title="Command" %}}

``` bash
curl -d '{ "name": "CHANGE_ME", "superpower": "CHANGE_ME" }' YOUR_ENDPOINT
```

{{% /tab %}} {{< /tabs >}}

For example:

``` bash
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

If you see a success message, generate more load: re-send that messate 5+ times. You should keep seeing a success message after each send.

Check the lambda logs output:

{{< tabs >}} {{% tab title="Producer Function Logs" %}}

``` bash
sls logs -f producer
```

{{% /tab %}} {{< /tabs >}}

{{< tabs >}} {{% tab title="Consumer Function Logs" %}}

``` bash
sls logs -f consumer
```

{{% /tab %}} {{< /tabs >}}

Examine the logs carefully.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Do you notice the difference?
{{% /notice %}}

Note that we are logging our Record together with the Trace context that we have added to it. Copy one of the underlined sub-sections of your trace parent context, and save it for later.

![5-redeploy-2-logs](../images/5-redeploy-2-logs.png)
