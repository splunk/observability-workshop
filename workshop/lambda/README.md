# Lambda Tracing Workshop

## Intro
This workshop will equip you to build a distributed trace for a small serverless application that runs on AWS Lambda, producing and consuming a message via AWS Kinesis.

First, we will see how OpenTelemetry's auto-instrumentation captures traces and exports them to your target of choice.

Then, we will see how we can enable context propagation with manual instrumentation.

For this workshop Splunk has prepared an Ubuntu Linux instance in AWS/EC2 all pre-configured for you. To get access to the instance that you will be using in the workshop, please visit the URL provided by the workshop leader

![Lambda application, not yet manually instrumented](/images/01-Architecture.png)
---
## Prerequisites

### Splunk Observability Workshop Instance, Access Token, Realm
The Observability Workshop is most often completed on a Splunk-issued and preconfigured EC2 instance running Ubuntu.

Your workshop instructor will provide you with the credentials to your assigned workshop instance.

Your instance should have the following environment variables already set:
- **ACCESS_TOKEN**
- **REALM**
  - _These are the Splunk Observability Cloud **Access Token** and **Realm** for your workshop._
  - _They will be used by the OpenTelemetry Collector to forward your data to the correct Splunk Observability Cloud organization._

> [!NOTE]
> _Alternatively, you can deploy a local observability workshop instance using Multipass._

### AWS Command Line Interface (awscli)
The AWS Command Line Interface, or **awscli**, is an API used to interact with AWS resources. In this workshop, it is used by certain scripts to interact with the resource you'll deploy.

Your Splunk-issued workshop instance should already have the **awscli** installed.

- Check if the **aws** command is installed on your instance with the following command:
  ```bash
  which aws
  ```
    - _The expected output would be **/usr/local/bin/aws**_

- If the **aws** command is not installed on your instance, run the following command:
  ```bash
  sudo apt install awscli
  ```

### Terraform
Terraform is an Infrastructure as Code (IaC) platform, used to deploy, manage and destroy resource by defining them in configuration files. Terraform employs HCL to define those resources, and supports multiple providers for various platforms and technologies.

We will be using Terraform at the command line in this workshop to deploy the following resources:
1. AWS API Gateway
2. Lambda Functions
3. Kinesis Stream
4. CloudWatch Log Groups
5. S3 Bucket
    - _and other supporting resources_
  
Your Splunk-issued workshop instance should already have **terraform** installed.

- Check if the **terraform** command is installed on your instance:
  ```bash
  which terraform
  ```
    - _The expected output would be **/usr/local/bin/terraform**_

- If the **terraform** command is not installed on your instance, follow Terraform's recommended installation commands listed below:
  ```bash
  wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

  sudo apt update && sudo apt install terraform
  ```

### Workshop Directory (o11y-lambda-workshop)
The Workshop Directory **o11y-lambda-workshop** is a repository that contains all the configuration files and scripts to complete both the auto-instrumentation and manual instrumentation of the example Lambda-based application we will be using today.

- Confirm you have the workshop directory in your home directory:
  ```bash
  cd && ls
  ```
    - _The expected output would include **o11y-lambda-workshop**_

- If the **o11y-lambda-workshop** directory is not in your home directory, clone it with the following command:
  ```bash
  git clone https://github.com/gkono-splunk/o11y-lambda-workshop.git
  ```

### AWS & Terraform Variables

#### AWS
The AWS CLI requires that you have credentials to be able to access and manage resources deployed by their services. Both Terraform and the Python scripts in this workshop require these variables to perform their tasks.

- Configure the **awscli** with the _**access key ID**_, _**secret access key**_ and _**region**_ for this workshop:
  ```bash
  aws configure
  ```
    - _This command should provide a prompt similar to the one below:_
      ```bash
      AWS Access Key ID [None]: XXXXXXXXXXXXXXXX
      AWS Secret Acces Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      Default region name [None]: us-east-1
      Default outoput format [None]:
      ```

- If the **awscli** is not configured on your instance, run the following command and provide the values your instructor would provide you with.
  ```bash
  aws configure
  ```

#### Terraform
Terraform supports the passing of variables to ensure sensitive or dynamic data is not hard-coded in your .tf configuration files, as well as to make those values reusable throughout your resource definitions.

In our workshop, Terraform requires variables necessary for deploying the Lambda functions with the right values for the OpenTelemetry Lambda layer; For the ingest values for Splunk Observability Cloud; And to make your environment and resources unique and immediatley recognizable.

Terraform variables are defined in the following manner:
- Define the variables in your _**main.tf**_ file or a _**variables.tf**_
- Set the values for those variables in either of the following ways:
  - setting environment variables at the host level, with the same variable names as in their definition, and with _**TF_VAR**__ as a prefix
  - setting the values for your variables in a _**terraform.tfvars**_ file
  - passing the values as arguments when running terraform apply
 
We will be using a combination of _**variables.tf**_ and _**terraform.tfvars**_ files to set our variables in this workshop.

- Using either **vi** or **nano**, open the _**terraform.tfvars**_ file in either the **auto** or **manual** directory
  ```bash
  vi ~/o11y-lambda-workshop/auto/terraform.tfvars
  ```
- Set the variables with their values. Replace the **CHANGEME** placeholders with those provided by your instructor.
  ```bash
  o11y_access_token = "CHANGEME"
  o11y_realm        = "CHANGEME"
  otel_lambda_layer = ["CHANGEME"]
  prefix            = "CHANGEME"
  ```
  - _Ensure you change only the placeholders, leaving the quotes and brackets intact, where applicable._
  - _The _**prefix**_ is a unique identifier you can choose for yourself, to make your resources distinct from other participants' resources. We suggest using a short form of your name, for example._
  - _Also, please only lowercase letters for the **prefix**. Certain resouces in AWS, such as S3, would through an error if you use uppercase letters._
- Save your file and exit the editor.
- Finally, copy the _**terraform.tfvars**_ file you just edited to the other directory.
  ```bash
  cp ~/o11y-lambda-workshop/auto/terraform.tfvars ~/o11y-lambda-workshop/manual
  ```
  - _We do this as we will be using the same values for both the autoinstrumentation and manual instrumentation protions of the workshop_
 
### File Permissions
While all other files are fine as they are, the **send_message.py** script in both the `auto` and `manual` will have to be executed as part of our workshop. As a result, it needs to have the appropriate permissions to run as expected. Follow these instructions to set them.

- First, ensure you are in the `o11y-lambda-workshop` directory:
  ```bash
  cd ~/o11y-lambda-workshop
  ```

- Next, run the following command to set executable permissions on the `send_message.py` script:
  ```bash
  sudo chmod 755 auto/send_message.py manual/send_message.py
  ```

Now that we've squared off the prerequisites, we can get started with the workshop!

---

## Auto-Instrumentation
The first part of our workshop will demonstrate how auto-instrumentation with OpenTelemetry allows the OpenTelemetry Collector to auto-detect what language your function is written in, and start capturing traces for those functions.

### The Auto-Instrumentation Workshop Directory & Contents
First, let us take a look at the **o11y-lambda-workshop/auto** directory, and some of its files. This is where all the content for the auto-instrumentation portion of our workshop resides.

#### The **auto** Directory
- Run the following command to get into the **o11y-lambda-workshop/auto** directory:
  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- Inspect the contents of this directory:
  ```bash
  ls
  ```
  - _The output should include the following files and directories:_
    ```bash
    handler             outputs.tf          terraform.tf        variables.tf
    main.tf             send_message.py     terraform.tfvars
    ```

#### The **main.tf** file
- Take a closer look at the **main.tf** file:
  ```bash
  cat main.tf
  ```

{{% notice title="Workshop Questions" style="tip" icon="question" %}}
- Can you identify which AWS resources are being created by this template?
- Can you identify where OpenTelemetry instrumentation is being set up?
  - _Hint: study the lambda function definitions_
- Can you determine which instrumentation information is being provided by the environment variables we set earlier?
{{% /notice %}}

You should see a section where the environment variables for each lambda function are being set.
  ```bash
  environment {
    variables = {
      SPLUNK_ACCESS_TOKEN = var.o11y_access_token
      SPLUNK_REALM = var.o11y_realm
      OTEL_SERVICE_NAME = "${var.prefix}-producer-lambda"
      OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
      AWS_LAMBDA_EXEC_WRAPPER = "/opt/nodejs-otel-handler"
      KINESIS_STREAM = aws_kinesis_stream.lambda_streamer.name
    }
  }
  ```

By using these environment variables, we are configuring our auto-instrumentation in a few ways:
- We are setting environment variables to inform the OpenTelemetry collector of which Splunk Observability Cloud organization we would like to have our data exported to.
  ```bash
  SPLUNK_ACCESS_TOKEN = var.o11y_access_token
  SPLUNK_ACCESS_TOKEN = var.o11y_realm
  ```

- We are also setting variables that help OpenTelemetry identify our function/service, as well as the environment/application it is a part of.
  ```bash
  OTEL_SERVICE_NAME = "producer-lambda" # consumer-lambda in the case of the consumer function
  OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
  ```

- We are setting an environment variable that lets OpenTelemetry know what wrappers it needs to apply to our function's handler so as to capture trace data automatically, based on our code language.
  ```bash
  AWS_LAMBDA_EXEC_WRAPPER - "/opt/nodejs-otel-handler"
  ```

- In the case of the **producer-lambda** function, we are setting an environment variable to let the function know what Kinesis Stream to put our record to.
  ```bash
  KINESIS_STREAM = aws_kinesis_stream.lambda_streamer.name
  ```

- These values are sourced from the variables we set in the **Prerequisites** section, as well as resources that will be deployed as a result of executing this Terraform configuration file.

You should also see an argument for setting the Splunk OpenTelemetry Lambda layer on each function
  ```bash
  layers = var.otel_lambda_layer
  ```
- The OpenTelemetry Lambda layer is a package that contains the libraries and dependencies necessary to collector, process and export telemetry data for Lambda functions at the moment of invocation.

- While there is a general OTel Lambda layer that has all the libraries and dependencies for all OpenTelemetry-supported languages, there are also language-specific Lambda layers, to help make your function even more lightweight.
  - _You can see the relevant Splunk OpenTelemetry Lambda layer ARNs (Amazon Resource Name) and latest versions for each AWS region [HERE](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md)_

#### The **producer.mjs** file
Next, let's take a look at the **producer-lambda** function code:

- Run the following command to view the contents of the **producer.mjs** file:
  ```bash
  cat ~/o11y-lambda-workshop/auto/handler/producer.mjs
  ```
  - This NodeJS module contains the code for the producer function.
  - Essentially, this function receives a message, and puts that message as a record to the targeted Kinesis Stream

### Deploying the Lambda Functions & Generating Trace Data
Now that we are familiar with the contents of our **auto** directory, we can deploy the resources for our workshop, and generate some trace data from our Lambda functions.

#### Initialize Terraform in the **auto** directory
In order to deploy the resources defined in the **main.tf** file, you first need to make sure that Terraform is initialized in the same directory as that file.

- Ensure you are in the **auto** directory:
  ```bash
  pwd
  ```
    - _The expected output would be **~/o11y-lambda-workshop/auto**_

- If you are not in the **auto** directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- Run the following command to initialize Terraform in this directory
  ```bash
  terraform init
  ```
  - This command will create a number of elements in the same directory:
    - **.terraform.lock.hcl** file: to record the providers it will use to provide resources
    - **.terraform** directory: to store the provider configurations

  - In addition to the above files, when terraform is run using the **apply** subcommand, the **terraform.tfstate** file will be created to track the state of your deployed resources.

  - These enable Terraform to manage the creation, state and destruction of resources, as defined within the **main.tf** file of the **auto** directory

#### Deploy the Lambda functions and other AWS resources
Once we've initialized Terraform in this directory, we can go ahead and deploy our resources.

- First, run the **terraform plan** command to ensure that Terraform will be able to create your resources without encountering any issues.
  ```bash
  terraform plan
  ```
  - _This will result in a plan to deploy resources and output some data, which you can review to ensure everything will work as intended._
  - _Do note that a number of the values shown in the plan will be known post-creation, or are masked for security purposes._

- Next, run the **terraform apply** command to deploy the Lambda functions and other supporting resources from the **main.tf** file:
  ```bash
  terraform apply
  ```
  - _Respond **yes** when you see the **Enter a value:** prompt_

  - This will result in the following outputs:
    ```bash
    Outputs:

    base_url = "https://______.amazonaws.com/serverless_stage/producer"
    consumer_function_name = "_____-consumer"
    consumer_log_group_arn = "arn:aws:logs:us-east-1:############:log-group:/aws/lambda/______-consumer"
    consumer_log_group_name = "/aws/lambda/______-consumer"
    environment = "______-lambda-shop"
    lambda_bucket_name = "lambda-shop-______-______"
    producer_function_name = "______-producer"
    producer_log_group_arn = "arn:aws:logs:us-east-1:############:log-group:/aws/lambda/______-producer"
    producer_log_group_name = "/aws/lambda/______-producer"
    ```
    - _Terraform outputs are defined in the **outputs.tf** file._
    - _These outputs will be used programmatically in other parts of our workshop, as well._

#### Send some traffic to the **producer-lambda** URL (**base_url**)
To start getting some traces from our deployed Lambda functions, we would need to generate some traffic. We will send a message to our **producer-lambda** function's endpoint, which should be put as a record into our Kinesis Stream, and then pulled from the Stream by the **consumer-lambda** function.

- Ensure you are in the **auto** directory:
  ```bash
  pwd
  ```
    - _The expected output would be **~/o11y-lambda-workshop/auto**_

- If you are not in the **auto** directory, run the following command
```bash
cd ~/o11y-lambda-workshop/auto
```

The **send_message.py** script is a Python script that will take input at the command line, add it to a JSON dictionary, and send it to your **producer-lambda** function's endpoint repeatedly, as part of a while loop set to run 1000x by default.

In addition to that, the **send_message.py** script will also get the logs for your producer and consumer functions from their respective CloudWatch log groups, and add them to local files, for easy viewing.

- Run the **send_message.py** script as a background process
  - _It requires the **--name** and **--superpower** arguments_
  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```
  - You should see an output similar to the following if your message is successful
    ```bash
    [1] 79829
    user@host manual % appending output to nohup.out
    ```
    - _The two most import bits of information here are:_
      - _The process ID on the first line (**79829** in the case of my example), and_
      - _The **appending output to nohup.out** message_
    
    - _The **nohup** command ensures the script will not hang up when sent to the background. It also captures the curl output from our command in a nohup.out file in the same directory as the one you're currently in._

    - _The **&** tells our shell process to run this process in the background, thus freeing our shell to run other commands._

- Next, check the contents of the **response.logs** file, to ensure your output confirms your requests to your **producer-lambda** endpoint are successful:
  ```bash
  cat response.logs
  ```
  - You should see the following output among the lines printed to your screen if your message is successful:
    ```bash
    {"message": "Message placed in the Event Stream: {prefix}-lambda_stream"}
    ```

  - If unsuccessful, you will see:
    ```bash
    {"message": "Internal server error"}
    ```

> [!IMPORTANT]
> If this occurs, ask one of the workshop facilitators for assistance.

#### View the Lambda Function Logs
Next, let's take a look at the logs for our Lambda functions.

- To view your **producer-lambda** logs, check the **producer.logs** file:
  ```bash
  cat producer.logs
  ```

- To view your **consumer-lambda** logs, check the **consumer.logs** file:
  ```bash
  cat consumer.logs
  ```

Examine the logs carefully.

##### _Workshop Question_
> Do you see OpenTelemetry being loaded? Look out for the lines with **splunk-extension-wrapper**.

- _Consider running `head -n 50 producer.logs` or `head -n 50 consumer.logs` to see the **splunk-extension-wrapper** being loaded._

<!-- Add an image here of the logs for either producer-lambda or consumer-lambda, showing the splunk-extension-wrapper-->

### Splunk APM, Lambda Functions & Traces
The Lambda functions should be generating a sizeable amount of trace data, which we would need to take a look at. Through the combination of environment variables and the OpenTelemetry Lambda layer configured in the resource definition for our Lambda functions, we should now be ready to view our functions and traces in Splunk APM.

#### View your Environment name in the Splunk APM Overview
Let's start by making sure that Splunk APM is aware of our **Environment** from the trace data it is receiving. This is the **deployment.name** we set as part of the **OTEL_RESOURCE_ATTRIBUTES** variable we set on our Lambda function definitions in **main.tf**. It was also one of the outputs from the **terraform apply** command we ran earlier.

In Splunk Observability Cloud:
- Click on the **APM** Button from the Main Menu on the left. This will take you to the Splunk APM Overview.

- Select your APM Environment from the **Environment:** dropdown.
  - _Your APM environment should be in the **PREFIX-lambda-shop** format, where the **PREFIX** is obtained from the environment variable you set in the Prerequisites section_

> [!NOTE]
> _It may take a few minutes for your traces to appear in Splunk APM. Try hitting refresh on your browser until you find your environment name in the list of environments._

![Splunk APM, Environment Name](/images/02-Auto-APM-EnvironmentName.png)

#### View your Environment's Service Map
Once you've selected your Environment name from the Environment drop down, you can take a look at the Service Map for your Lambda functions.

- Click the **Service Map** Button on the right side of the APM Overview page. This will take you to your Service Map view.

![Splunk APM, Service Map Button](/images/03-Auto-ServiceMapButton.png)

You should be able to see the **producer-lambda** function and the call it is making to the Kinesis Stream to put your record.

![Splunk APM, Service Map](/images/04-Auto-ServiceMap.png)

##### _Workshop Question_
> _What about your **consumer-lambda** function?_

#### Explore the Traces from your Lambda Functions

- Click the **Traces** button to view the Trace Analyzer.

![Splunk APM, Trace Button](/images/05-Auto-TraceButton.png)

On this page, we can see the traces that have been ingested from the OpenTelemetry Lambda layer of your **producer-lambda** function.

![Splunk APM, Trace Analyzer](/images/06-Auto-TraceAnalyzer.png)

- Select a trace from the list to examine by clicking on its hyperlinked **Trace ID**.

![Splunk APM, Trace and Spans](/images/07-Auto-TraceNSpans.png)

We can see that the **producer-lambda** function is putting a record into the Kinesis Stream. But the action of the **consumer-lambda** function is missing!

This is because the trace context is not being propagated. Trace context propagation is not supported out-of-the-box by Kinesis service at the time of this workshop. Our distributed trace stops at the Kinesis service, and because its context isn't automatically propagated through the stream, we can't see any further.

Not yet, at least...

Let's see how we work around this in the next section of this workshop. But before that, let's clean up after ourselves!

### Clean Up
The resources we deployed as part of this auto-instrumenation exercise need to be cleaned. Likewise, the script that was generating traffice against our **producer-lambda** endpoint needs to be stopped, if it's still running. Follow the below steps to clean up.

#### Kill the **send_message**
- If the **send_message.py** script is still running, stop it with the follwing commands:
  ```bash
  fg
  ```
  - This brings your background process to the foreground.
  - Next you can hit **[Control-C]** to kill the process.

#### Destroy all AWS resources
Terraform is great at managing the state of our resources individually, and as a deployment. It can even update deployed resources with any changes to their definitions. But to start afresh, we will destroy the resources and redeploy them as part of the manual instrumentation portion of this workshop.

Please follow these steps to destroy your resources:
- Ensure you are in the **auto** directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/o11y-lambda-workshop/auto**_

- If you are not in the **auto** directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- Destroy the Lambda functions and other AWS resources you deployed earlier:
  ```bash
  terraform destroy
  ```
  - respond **yes** when you see the **Enter a value:** prompt
  - This will result in the resources being destroyed, leaving you with a clean environment

This process will leave you with the files and directories created as a result of our activity. Do not worry about those.

---

## Manual Instrumentation
The second part of our workshop will focus on demonstrating how manual instrumentation with OpenTelemetry empowers us to enhance telemetry collection. More specifically, in our case, it will enable us to propagate trace context data from the **producer-lambda** function to the **consumer-lambda** function, thus enabling us to see the relationship between the two functions, even across Kinesis Stream, which currently does not support automatic context propagation.

### The Manual Instrumentation Workshop Directory & Contents
Once again, we will first start by taking a look at our operating directory, and some of its files. This time, it will be **o11y-lambda-workshop/manual** directory. This is where all the content for the manual instrumentation portion of our workshop resides.

#### The **manual** directory
- Run the following command to get into the **o11y-lambda-workshop/manual** directory:
  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

Inspect the contents of this directory with the **ls** command:
  ```bash
  ls
  ```
  - _The output should include the following files and directories:_
    ```bash
    handler             outputs.tf          terraform.tf        variables.tf
    main.tf             send_message.py     terraform.tfvars
    ```

##### _Workshop Question_
> _Do you see any difference between this directory and the auto directory when you first started?_

#### Compare **auto** and **manual** files
Let's make sure that all these files that LOOK the same, are actually the same.

- Compare the **main.tf** files in the **auto** and **manual** directories:
  ```bash
  diff ~/o11y-lambda-workshop/auto/main.tf ~/o11y-lambda-workshop/manual/main.tf
  ```
  - There is no difference! _(Well, there shouldn't be. Ask your workshop facilitator to assist you if there is)_

- Now, let's compare the **producer.mjs** files:
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

- Finally, compare the **consumer.mjs** files:
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
    - Then to add new span attributes based on our **name** and **superpower** to the extracted trace context

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
1. Extract the context that we obtained from **producer-lambda** into a carrier object.
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

### Deploying the Lambda Functions & Generating Trace Data
Now that we know how to apply manual instrumentation to the functions and services we wish to capture trace data for, let's go about deploying our Lambda functions again, and generating traffic against our **producer-lambda** endpoint.

#### Initialize Terraform in the **manual** directory
Seeing as we're in a new directory, we will need to initialize Terraform here once again.

- Ensure you are in the **manual** directory:
  ```bash
  pwd
  ```
    - _The expected output would be **~/o11y-lambda-workshop/manual**_

- If you are not in the **manual** directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- Run the following command to initialize Terraform in this directory
  ```bash
  terraform init
  ```

#### Deploy the Lambda functions and other AWS resources
Let's go ahead and deploy those resources once more!

- Run the **terraform plan** command, ensuring there are no issues.
  ```bash
  terraform plan
  ```
  
- Follow up with the **terraform apply** command to deploy the Lambda functions and other supporting resources from the **main.tf** file:
  ```bash
  terraform apply
  ```
  - _Respond **yes** when you see the **Enter a value:** prompt_

  - This will result in the following outputs:
    ```bash
    Outputs:

    base_url = "https://______.amazonaws.com/serverless_stage/producer"
    consumer_function_name = "_____-consumer"
    consumer_log_group_arn = "arn:aws:logs:us-east-1:############:log-group:/aws/lambda/______-consumer"
    consumer_log_group_name = "/aws/lambda/______-consumer"
    environment = "______-lambda-shop"
    lambda_bucket_name = "lambda-shop-______-______"
    producer_function_name = "______-producer"
    producer_log_group_arn = "arn:aws:logs:us-east-1:############:log-group:/aws/lambda/______-producer"
    producer_log_group_name = "/aws/lambda/______-producer"
    ```

As you can tell, aside from the first portion of the base_url and the log group ARNs, the output should be largely the same as when you ran the auto-instrumentation portion of this workshop up to this same point.

#### Send some traffic to the **producer-lambda** endpoint (**base_url**)
Once more, we will send our **name** and **superpower** as a message to our endpoint. This will then be added to a record in our Kinesis Stream, along with our trace context.

- Ensure you are in the **manual** directory:
  ```bash
  pwd
  ```
    - _The expected output would be **~/o11y-lambda-workshop/manual**_

- If you are not in the **manual** directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- Run the **send_message.py** script as a background process:
  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```

- Next, check the contents of the response.logs file for successful calls to our**producer-lambda** endpoint:
  ```bash
  cat response.logs
  ```
  - You should see the following output among the lines printed to your screen if your message is successful:
    ```bash
    {"message": "Message placed in the Event Stream: {prefix}-lambda_stream"}
    ```

  - If unsuccessful, you will see:
    ```bash
    {"message": "Internal server error"}
    ```

> [!IMPORTANT]
> If this occurs, ask one of the workshop facilitators for assistance.

#### View the Lambda Function Logs
Let's see what our logs look like now.

- Check the **producer.logs** file:
  ```bash
  cat producer.logs
  ```

- And the **consumer.logs** file:
  ```bash
  cat consumer.logs
  ```

Examine the logs carefully.

##### _Workshop Question_
> Do you notice the difference?

#### Copy the Trace ID from the **consumer-lambda** logs
This time around, we can see that the consumer-lambda log group is logging our message as a **record** together with the **tracecontext** that we propagated.

To copy the Trace ID:
- Take a look at one of the **Kinesis Message** logs. Within it, there is a **data** dictionary
- Take a closer look at **data** to see the nested **tracecontext** dictionary
- Within the **tracecontext** dictionary, there is a **traceparent** key-value pair
- The **traceparent** key-value pair holds the Trace ID we seek
  - There are 4 groups of values, separated by **-**. The Trace ID is the 2nd group of characters    
- **Copy the Trace ID, and save it.** We will need it for a later step in this workshop

![Lambda Consumer Logs, Manual Instruamentation](/images/08-Manual-ConsumerLogs.png)

### Splunk APM, Lambda Functions & Traces
In order to see the result of our context propagation outside of the logs, we'll once again consult the Splunk APM UI.

#### View your Lambda Functions in the Splunk APM Service Map
Let's take a look at the Service Map for our environment in APM once again.

In Splunk Observability Cloud:
- Click on the **APM** Button in the Main Menu.

- Select your APM Environment from the **Environment:** dropdown.

- Click the **Service Map** Button on the right side of the APM Overview page. This will take you to your Service Map view.

> [!NOTE]
> _Reminder: It may take a few minutes for your traces to appear in Splunk APM. Try hitting refresh on your browser until you find your environment name in the list of environments._

##### _Workshop Question_
> _Notice the difference?_

- You should be able to see the **producer-lambda** and **consumer-lambda** functions linked by the propagated context this time!

![Splunk APM, Service Map](/images/09-Manual-ServiceMap.png)

#### Explore a Lambda Trace by Trace ID
Next, we will take another look at a trace related to our Environment.

- Paste the Trace ID you copied from the consumer function's logs into the **View Trace ID** search box under Traces and click **Go**

![Splunk APM, Trace Button](/images/10-Manual-TraceButton.png)

> [!NOTE]
> _The Trace ID was a part of the trace context that we propagated._

You can read up on two of the most common propagation standards:
1. [W3C](https:///www.w3.org/TR/trace-context/#traceparent-header)
2. [B3](https://github.com/openzipkin/b3-propagation#overall-process)

##### _Workshop Question_
> _Which one are we using?_
  - _The Splunk Distribution of Opentelemetry JS, which supports our NodeJS functions, [defaults](https://docs.splunk.com/observability/en/gdi/get-data-in/application/nodejs/splunk-nodejs-otel-distribution.html#defaults-of-the-splunk-distribution-of-opentelemetry-js) to the **W3C** standard_

##### _Workshop Question_
> _Bonus Question: What happens if we mix and match the W3C and B3 headers?_

![Splunk APM, Trace by ID](/images/11-Manual-TraceByID.png)

Click on the **consumer-lambda** span.

##### _Workshop Question_
> _Can you find the attributes from your message?_

![Splunk APM, Span Tags](/images/12-Manual-SpanTags.png)

### Clean Up
We are finally at the end of our workshop. Kindly clean up after yourself!

#### Kill the **send_message**
- If the **send_message.py** script is still running, stop it with the follwing commands:
  ```bash
  fg
  ```
  - This brings your background process to the foreground.
  - Next you can hit **[Control-C]** to kill the process.

#### Destroy all AWS resources
Terraform is great at managing the state of our resources individually, and as a deployment. It can even update deployed resources with any changes to their definitions. But to start afresh, we will destroy the resources and redeploy them as part of the manual instrumentation portion of this workshop.

Please follow these steps to destroy your resources:
- Ensure you are in the **manual** directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/o11y-lambda-workshop/manual**_

- If you are not in the **manual** directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- Destroy the Lambda functions and other AWS resources you deployed earlier:
  ```bash
  terraform destroy
  ```
  - respond **yes** when you see the **Enter a value:** prompt
  - This will result in the resources being destroyed, leaving you with a clean environment

## Conclusion

Congratulations on finishing the Lambda Tracing Workshop! You have seen how we can complement auto-instrumentation with manual steps to have the **producer-lambda** function's context be sent to the **consumer-lambda** function via a record in a Kinesis stream. This allowed us to build the expected Distributed Trace, and to contextualize the relationship between both functions in Splunk APM.

![Lambda application, fully instrumented](/images/13-Architecture_Instrumented.png)

You can now build out a trace manually by linking two different functions together. This comes in handy when your auto-instrumentation, or 3rd-party systems, do not support context propagation out of the box, or when you wish to add custom attributes to a trace for more relevant trace analaysis.
