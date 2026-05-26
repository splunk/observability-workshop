---
title: OpenShift Prerequisites
linkTitle: 2. OpenShift Prerequisites
weight: 2
time: 15 minutes
---

The steps below are required before deploying the OpenShift cluster in AWS. 

## Create a Red Hat Login

The first thing we'll need to do is create an account with Red Hat, which we can do by 
filling out the form 
[here](https://www.redhat.com/wapps/ugc/register.html?_flowId=register-flow&_flowExecutionKey=e1s1).

## Install the AWS CLI

To install the AWS CLI on the EC2 instance provisioned previously, run the following commands:

``` bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
```

Use the following command to ensure it was installed successfully: 

``` bash
aws --version
```

It should return something like the following: 

````
aws-cli/2.30.5 Python/3.13.7 Linux/6.14.0-1011-aws exe/x86_64.ubuntu.24
````

Login to your AWS account using your preferred method.  Refer to the 
[documentation](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) 
for guidance.  For example, you can login by running the `aws configure` command. 

Confirm you're logged in successfully by running a command such as `aws ec2 describe-instances`. 

Then, verify your account identity with: 

``` bash
aws sts get-caller-identity
```

Check whether the service role for ELB (Elastic Load Balancing) exists:

``` bash
aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing"
```

If the role does not exist, create it by running the following command:

``` bash
aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
```

## Install the ROSA CLI 

We'll use the ROSA command-line interface (CLI) for the deployment. The instructions are
based on [Red Hat documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws_classic_architecture/4/html-single/install_rosa_classic_clusters/index#rosa-installing-and-configuring-the-rosa-cli_rosa-installing-cli). 

You can download the latest release of the ROSA CLI for your operating system
[here](https://console.redhat.com/openshift/downloads). 

Alternatively, we can use the following command to download the CLI binary directly 
to our EC2 instance: 

````
curl -L -O https://mirror.openshift.com/pub/cgw/rosa/latest/rosa-linux.tar.gz
````

Extract the contents: 

````
tar -xvzf rosa-linux.tar.gz
````

Move the resulting file (`rosa`) to a location that's included as part of your path.  For example: 

``` bash
sudo mv rosa /usr/local/bin/rosa
```

Log in to your Red Hat account by running the command below, then follow the instructions 
in the command output: 

````
rosa login --use-device-code
````

## Install the OpenShift CLI (oc)

We can use the following command to download the OpenShift CLI binary directly
to our EC2 instance:

````
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
````

Extract the contents:

````
tar -xvzf openshift-client-linux.tar.gz
````

Move the resulting files (`oc` and `kubectl`) to a location that's included as part of your path.  For example:

``` bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## Create Account-Wide Roles and Policies 

Use the following command to create the necessary account-wide roles and policies: 

``` bash
rosa create account-roles --mode auto
```

## Create an AWS VPC for ROSA HCP

We're going to use the Hosted Control Plane (HCP) deployment option to 
deploy our OpenShift cluster.  To do this, we'll need to 
create a new VPC in our AWS account using the following command: 

> Note:  update the region as appropriate for your environment.

``` bash
rosa create network network-template --param Region=us-east-2 --param Name=rosa-network-stack --template-dir='.'
```

> Important: make note of the subnet ids created as a result of this command 
> as you'll need them when creating the cluster.  Make a note of the CloudFormation 
> stack name as well, which will be needed later if you want to delete the network. 

> Note: by default, each AWS region is limited to 5 elastic IP addresses.  
> If you receive the following error: 
> "The maximum number of addresses has been reached."
> then you'll need to contact AWS to request an increase to this limit, 
> or choose another AWS region to create the VPC for ROSA. 

## Create an OpenID Connect configuration

Before creating a Red Hat OpenShift Service on AWS cluster, let's create the OpenID Connect (OIDC) 
configuration with the following command: 

``` bash
rosa create oidc-config --mode=auto --yes
```

> Important: make note of the oidc-provider id that is created.