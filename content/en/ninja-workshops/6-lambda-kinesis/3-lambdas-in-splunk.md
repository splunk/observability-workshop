---
title: Splunk APM, Lambda Functions & Traces
linkTitle: 3. Lambda Traces in Splunk APM
weight: 3
---

The Lambda functions should be generating a sizeable amount of trace data, which we would need to take a look at. Through the combination of environment variables and the OpenTelemetry Lambda layer configured in the resource definition for our Lambda functions, we should now be ready to view our functions and traces in Splunk APM.

#### View your Environment name in the Splunk APM Overview
Let's start by making sure that Splunk APM is aware of our `Environment` from the trace data it is receiving. This is the `deployment.name` we set as part of the `OTEL_RESOURCE_ATTRIBUTES` variable we set on our Lambda function definitions in `main.tf`.

In Splunk Observability Cloud:
- Click on the `APM` Button from the Main Menu on the left. This will take you to the Splunk APM Overview.

- Select your APM Environment from the `Environment:` dropdown.
  - _Your APM environment should be in the `PREFIX-lambda-shop` format, where the `PREFIX is obtained from the environment variable you set in the Prerequisites section_

> [!NOTE]
> It may take a few minutes for your traces to appear in Splunk APM. Try hitting refresh on your browser until you find your environment name in the list of environments.

![Splunk APM, Environment Name](../images/02-Auto-APM-EnvironmentName.png)

#### View your Environment's Service Map
Once you've selected your Environment name from the Environment drop down, you can take a look at the Service Map for your Lambda functions.

- Click the `Service Map` Button on the right side of the APM Overview page. This will take you to your Service Map view.

![Splunk APM, Service Map Button](../images/03-Auto-ServiceMapButton.png)

You should be able to see the `producer-lambda` function and the call it is making to the Kinesis Stream to put your record.

![Splunk APM, Service Map](../images/04-Auto-ServiceMap.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What about your `consumer-lambda` function?
{{% /notice %}}

#### Explore the Traces from your Lambda Functions

- Click the `Traces` button to view the Trace Analyzer.

![Splunk APM, Trace Button](../images/05-Auto-TraceButton.png)

On this page, we can see the traces that have been ingested from the OpenTelemetry Lambda layer of your `producer-lambda` function.

![Splunk APM, Trace Analyzer](../images/06-Auto-TraceAnalyzer.png)

- Select a trace from the list to examine by clicking on its hyperlinked `Trace ID`.

![Splunk APM, Trace and Spans](../images/07-Auto-TraceNSpans.png)

We can see that the `producer-lambda` function is putting a record into the Kinesis Stream. But the action of the `consumer-lambda` function is missing!

This is because the trace context is not being propagated. Trace context propagation is not supported out-of-the-box by Kinesis service at the time of this workshop. Our distributed trace stops at the Kinesis service, and we can't see the propagation any further.

Not yet, at least...

Let's see how we work around this in the next section of this workshop. But before that, let's clean up after ourselves!

### Clean Up
The resources we deployed as part of this auto-instrumenation exercise need to be cleaned. Likewise, the script that was generating traffice against our `producer-lambda` endpoint needs to be stopped, if it's still running. Follow the below steps to clean up.

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
- Ensure you are in the `auto` directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/o11y-lambda-workshop/auto**_

- If you are not in the `auto` directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- Destroy the Lambda functions and other AWS resources you deployed earlier:
  ```bash
  terraform destroy
  ```
  - respond `yes` when you see the `Enter a value:` prompt
  - This will result in the resources being destroyed, leaving you with a clean environment

This process will leave you with a few files and directories in the `auto` directory. Do not worry about those.
