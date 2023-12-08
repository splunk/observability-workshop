---
title: Setup
linkTitle: 1. Setup
weight: 1
---

This lab will make a tracing superhero out of you!

In this lab you will learn how a distributed trace is constructed for a small serverless application that runs on AWS Lambda, producing and consuming your message via AWS Kinesis.

![1-architecture](../images/1-architecture.png)

## Pre-requisites

You should already have the lab content available on your EC2 lab host.

Ensure that this lab's required folder o11y-lambda-lab is on your home directory:

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd ~ && ls
```

{{% /tab %}}
{{% tab title="Output" %}}

``` text
o11y-lambda-lab
```

{{% /tab %}}
{{< /tabs >}}

{{% notice style="note" %}} If you don't see it, fetch the lab contents by running the following command:

``` bash
git clone https://github.com/kdroukman/o11y-lambda-lab.git
```

{{% /notice %}}

## Set Environment Variables

In your Splunk Observability Cloud Organisation (Org) obtain your Access Token and Realm Values.

Please reset your environment variables from the earlier lab. Take care that for this lab we may be using different names - make sure to match the Environment Variable names below.

{{< tabs >}}
{{% tab title="Export Environment Variables" %}}

``` ini
export ACCESS_TOKEN=CHANGE_ME \
export REALM=CHANGE_ME \
export PREFIX=$INSTANCE
```

{{% /tab %}}
{{< /tabs >}}

## Update Auto-instrumentation serverless template

Update your auto-instrumentation Serverless template to include new values from the Enviornment variables.

{{< tabs >}}
{{% tab title="Substitute Environment Variables" %}}

``` bash
cat ~/o11y-lambda-lab/auto/serverless_unset.yml | envsubst > ~/o11y-lambda-lab/auto/serverless.yml
```

{{% /tab %}}
{{< /tabs >}}

Examine the output of the updated serverless.yml contents (you may need to scroll up to the relevant section).

{{< tabs >}}
{{% tab title="Check file contents" %}}

``` bash
cat ~/o11y-lambda-lab/auto/serverless.yml
```

{{% /tab %}}
{{% tab title="Expected Content" %}}

``` yaml
# USER SET VALUES =====================              
custom: 
  accessToken: <updated to your Access Token>
  realm: <updated to your Realm>
  prefix: <updated to your Hostname>
#====================================== 
```

{{% /tab %}}
{{< /tabs >}}

## Update Manual instrumentation template

Update your manual instrumentation Serverless template to include new values from the Enviornment variables.

{{< tabs >}}
{{% tab title="Substitute Environment Variables" %}}

``` bash
cat ~/o11y-lambda-lab/manual/serverless_unset.yml | envsubst > ~/o11y-lambda-lab/manual/serverless.yml
```

{{% /tab %}}
{{< /tabs >}}

Examine the output of the updated serverless.yml contents (you may need to scroll up to the relevant section).

{{< tabs >}}
{{% tab title="Check file contents" %}}

``` bash
cat ~/o11y-lambda-lab/manual/serverless.yml
```

{{% /tab %}}
{{% tab title="Expected Content" %}}

``` yaml
# USER SET VALUES =====================              
custom: 
  accessToken: <updated to your Access Token>
  realm: <updated to your Realm>
  prefix: <updated to your Hostname>
#====================================== 
```

{{% /tab %}}
{{< /tabs >}}

## Set your AWS Credentials

You will be provided with AWS Access Key ID and AWS Secret Access Key values - substitue these values in place of AWS_ACCESS_KEY_ID and AWS_ACCESS_KEY_SECRET in the bellow command:

{{< tabs >}}
{{% tab title="Set AWS Credentials" %}}

``` bash
sls config credentials --provider aws --key AWS_ACCCESS_KEY_ID --secret AWS_ACCESS_KEY_SECRET
```

{{% /tab %}}
{{< /tabs >}}

This command will create a file `~/.aws/credentials` with your AWS Credentials populated.

Note that we are using sls here, which is a Serverless framework for developing and deploying AWS Lambda functions. We will be using this command throughout the lab.

Now you are set up and ready go!
