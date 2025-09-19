---
title: AWS Setup
linkTitle: 1. AWS Setup
weight: 1
time: 10 minutes
---

## Enable the Red Hat OpenShift Service in AWS

To deploy OpenShift in your AWS account, we'll need to first enable the 
Red Hat OpenShift service using the [AWS console](https://us-east-1.console.aws.amazon.com/rosa/home?region=us-east-1#/). 

Next, follow the instructions to connect your AWS account with your Red Hat account. 

## Provision an EC2 Instance

Let's provision an EC2 instance that we'll use to deploy the Red Hat cluster. This avoids
the limitations running the ROSA command-line interface on Mac OS.

We used a t3.xlarge instance type using Ubuntu 24.04 LTS while creating the workshop,
but a smaller instance type can also be used.

ssh into the instance once it's up and running.
