---
title: Auto-Instrumentation
linkTitle: 2. Auto-Instrumentation
weight: 2
---

The first part of our workshop will demonstrate how auto-instrumentation with OpenTelemetry allows the OpenTelemetry Collector to auto-detect what language your function is written in, and start capturing traces for those functions.

### The Auto-Instrumentation Workshop Directory & Contents
First, let us take a look at the `workshop/lambda/auto` directory, and some of its files. This is where all the content for the auto-instrumentation portion of our workshop resides.

#### The `auto` Directory
- Run the following command to get into the **workshop/lambda/auto** directory:
  ```bash
  cd ~/workshop/lambda/auto
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

  - _The output should include the following files and directories:_
    ```bash
    get_logs.py    main.tf       send_message.py
    handler        outputs.tf    terraform.tf
    ```

#### The `main.tf` file

- Take a closer look at the `main.tf` file:
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
      OTEL_SERVICE_NAME = "producer-lambda"
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

- In the case of the `producer-lambda` function, we are setting an environment variable to let the function know what Kinesis Stream to put our record to.
  ```bash
  KINESIS_STREAM = aws_kinesis_stream.lambda_streamer.name
  ```

- These values are sourced from the environment variables we set in the Prerequisites section, as well as resources that will be deployed as a part of this Terraform configuration file.

You should also see an argument for setting the Splunk OpenTelemetry Lambda layer on each function
  ```bash
  layers = var.otel_lambda_layer
  ```

- The OpenTelemetry Lambda layer is a package that contains the libraries and dependencies necessary to collector, process and export telemetry data for Lambda functions at the moment of invocation.

- While there is a general OTel Lambda layer that has all the libraries and dependencies for all OpenTelemetry-supported languages, there are also language-specific Lambda layers, to help make your function even more lightweight.
  - _You can see the relevant Splunk OpenTelemetry Lambda layer ARNs (Amazon Resource Name) and latest versions for each AWS region [HERE](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md)_

#### The `producer.mjs` file
Next, let's take a look at the `producer-lambda` function code:

- Run the following command to view the contents of the `producer.mjs` file:
  ```bash
  cat ~/o11y-lambda-workshop/auto/handler/producer.mjs
  ```
  - This NodeJS module contains the code for the producer function.
  - Essentially, this function receives a message, and puts that message as a record to the targeted Kinesis Stream

### Deploying the Lambda Functions & Generating Trace Data
Now that we are familiar with the contents of our `auto` directory, we can deploy the resources for our workshop, and generate some trace data from our Lambda functions.

#### Initialize Terraform in the `auto` directory
In order to deploy the resources defined in the `main.tf` file, you first need to make sure that Terraform is initialized in the same folder as that file.

- Ensure you are in the `auto` directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/workshop/lambda/auto**_

- If you are not in the `auto` directory, run the following command:
  ```bash
  cd ~/workshop/lambda/auto
  ```

- Run the following command to initialize Terraform in this directory
  ```bash
  terraform init
  ```
  - This command will create a number of elements in the same folder:
    - `.terraform.lock.hcl` file: to record the providers it will use to provide resources
    - `.terraform` directory: to store the provider configurations
  - In addition to the above files, when terraform is run using the `apply` subcommand, the `terraform.tfstate` file will be created to track the state of your deployed resources.
  - These enable Terraform to manage the creation, state and destruction of resources, as defined within the `main.tf` file of the `auto` directory

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

#### Send some traffic to the `producer-lambda` URL (`base_url`)

To start getting some traces from our deployed Lambda functions, we would need to generate some traffic. We will send a message to our `producer-lambda` function's endpoint, which should be put as a record into our Kinesis Stream, and then pulled from the Stream by the `consumer-lambda` function.

- Ensure you are in the `auto` directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/workshop/lambda/auto**_

- If you are not in the `auto` directory, run the following command
  ```bash
  cd ~/workshop/lambda/auto
  ```

The `send_message.py` script is a Python script that will take input at the command line, add it to a JSON dictionary, and send it to your `producer-lambda` function's endpoint repeatedly, as part of a while loop.

- Run the `send_message.py` script as a background process
  - _It requires the `--name` and `--superpower` arguments_
  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```
  - You should see an output similar to the following if your message is successful
    ```bash
    [1] 79829
    user@host manual % appending output to nohup.out
    ```
    - _The two most import bits of information here are:_
      - _The process ID on the first line (`79829` in the case of my example), and_
      - _The `appending output to nohup.out` message_
    - _The `nohup` command ensures the script will not hang up when sent to the background. It also captures the curl output from our command in a nohup.out file in the same folder as the one you're currently in._
    - _The `&` tells our shell process to run this process in the background, thus freeing our shell to run other commands._

- Next, check the contents of the `response.logs` file, to ensure your output confirms your requests to your `producer-lambda` endpoint are successful:
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

{{% notice title="Workshop Question" style="tip" icon="question" %}}

- Do you see OpenTelemetry being loaded? Look out for the lines with `splunk-extension-wrapper`
  - - _Consider running `head -n 50 producer.logs` or `head -n 50 consumer.logs` to see the **splunk-extension-wrapper** being loaded._

{{% /notice %}}
