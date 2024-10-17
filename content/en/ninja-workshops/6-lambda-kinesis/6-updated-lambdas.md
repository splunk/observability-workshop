---
title: Splunk APM, Lambda Functions and Traces, Again!
linkTitle: 6. Updated Lambdas in Splunk APM
weight: 6
---

In order to see the result of our context propagation outside of the logs, we'll once again consult the [Splunk APM UI](https://app.us1.signalfx.com/#/apm).

#### View your Lambda Functions in the Splunk APM Service Map
Let's take a look at the Service Map for our environment in APM once again.

In Splunk Observability Cloud:
- Click on the `APM` Button in the Main Menu.

- Select your APM Environment from the `Environment:` dropdown.

- Click the `Service Map` Button on the right side of the APM Overview page. This will take you to your Service Map view.

> [!NOTE]
> _Reminder: It may take a few minutes for your traces to appear in Splunk APM. Try hitting refresh on your browser until you find your environment name in the list of environments._

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Notice the difference?
{{% /notice %}}

- You should be able to see the `producer-lambda` and `consumer-lambda` functions linked by the propagated context this time!

![Splunk APM, Service Map](../images/09-Manual-ServiceMap.png)

#### Explore a Lambda Trace by Trace ID
Next, we will take another look at a trace related to our Environment.

- Paste the Trace ID you copied from the consumer function's logs into the `View Trace ID` search box under Traces and click `Go`

![Splunk APM, Trace Button](../images/10-Manual-TraceButton.png)

> [!NOTE]
> The Trace ID was a part of the trace context that we propagated.

You can read up on two of the most common propagation standards:
1. [W3C](https:///www.w3.org/TR/trace-context/#traceparent-header)
2. [B3](https://github.com/openzipkin/b3-propagation#overall-process)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Which one are we using?
 - _The Splunk Distribution of Opentelemetry JS, which supports our NodeJS functions, [defaults](https://docs.splunk.com/observability/en/gdi/get-data-in/application/nodejs/splunk-nodejs-otel-distribution.html#defaults-of-the-splunk-distribution-of-opentelemetry-js) to the `W3C` standard_
{{% /notice %}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Bonus Question: What happens if we mix and match the W3C and B3 headers?
{{% /notice %}}

![Splunk APM, Trace by ID](../images/11-Manual-TraceByID.png)

Click on the `consumer-lambda` span.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Can you find the attributes from your message?
{{% /notice %}}

![Splunk APM, Span Tags](../images/12-Manual-SpanTags.png)

### Clean Up
We are finally at the end of our workshop. Kindly clean up after yourself!

#### Kill the `send_message`
- If the `send_message.py` script is still running, stop it with the follwing commands:
  ```bash
  fg
  ```
  - This brings your background process to the foreground.
  - Next you can hit `[CONTROL-C]` to kill the process.

#### Destroy all AWS resources
Terraform is great at managing the state of our resources individually, and as a deployment. It can even update deployed resources with any changes to their definitions. But to start afresh, we will destroy the resources and redeploy them as part of the manual instrumentation portion of this workshop.

Please follow these steps to destroy your resources:
- Ensure you are in the `manual` directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/o11y-lambda-workshop/manual**_

- If you are not in the `manual` directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- Destroy the Lambda functions and other AWS resources you deployed earlier:
  ```bash
  terraform destroy
  ```
  - respond `yes` when you see the `Enter a value:` prompt
  - This will result in the resources being destroyed, leaving you with a clean environment
