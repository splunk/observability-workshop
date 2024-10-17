---
title: Setup
linkTitle: 1. Setup
weight: 1
---

![Lambda application, not yet instrumented](../images/01-Architecture.png)

## Prerequisites

### Observability Workshop Instance
The Observability Workshop is most often completed on a Splunk-issued and preconfigured EC2 instance running Ubuntu.
- Your workshop instructor will have provided you with your credentials to access your instance.
- Alternatively, you can deploy a local observability workshop instance using Multipass.

### AWS Command Line Interface (awscli)
The AWS Command Line Interface, or `awscli`, is an API used to interact with AWS resources. In this workshop, it is used by certain scripts to interact with the resource you'll deploy. 

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
The Workshop Directory `o11y-lambda-workshop` is a repository that contains all the configuration files and scripts to complete both the auto-instrumentation and manual instrumentation of the example Lambda-based application we will be using today.

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

- Ensure you have the following environment variables set for AWS access:
  ```bash
  echo $AWS_ACCESS_KEY_ID
  echo $AWS_SECRET_ACCESS_KEY
  ```
    - _These commands should output text results for your **access key ID** and **secret access key**_

- If the AWS environment variables aren't set, request those keys from your instructor.
  - Replace the **CHANGEME** values for the following variables, then copy and paste them into your command line.
  ```bash
  export AWS_ACCESS_KEY_ID="CHANGEME"
  export AWS_SECRET_ACCESS_KEY="CHANGEME"
  ```

#### Terraform
Terraform supports the passing of variables to ensure sensitive or dynamic data is not hard-coded in your .tf configuration files.

Terraform variables are defined by setting TF_VAR_ environment variables and declaring those variables in our TF configuration files.

In our workshop, Terraform requires variables necessary for deploying the Lambda functions with the right environment variables for the OpenTelemetry Lambda layer, as well as the ingest values for Splunk Observability Cloud.

- Ensure you have the following environment variables set for AWS access:
  ```bash
  echo $TF_VAR_o11y_access_token
  echo $TF_VAR_o11y_realm
  echo $TF_VAR_otel_lambda_layer
  echo $TF_VAR_prefix
  ```
    - _These commands should output text for the **access token**, **realm**, and **otel lambda layer** for Splunk Observability Cloud, which your instructor has, or can, share with you._
    - _Also there should be an output for the **prefix** that will be used to name your resources. It will be a value that you provide._

- If the Terraform environment variables aren't set, request the **access token**, **realm**, and **otel lambda layer** from your instructor.
  - Replace the **CHANGEME** values for the following variables, then copy and paste them into your command line.
  ```bash
  export TF_VAR_o11y_access_token="CHANGEME"
  export TF_VAR_o11y_realm="CHANGEME"
  export TF_VAR_otel_lambda_layer='["CHANGEME"]'
  export TF_VAR_prefix="CHANGEME"
  ```

Now that we've squared off the prerequisites, we can get started with the workshop!
