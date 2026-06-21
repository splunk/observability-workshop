---
title: Distributed Tracing for AWS Lambda Functions
linkTitle: Lambda Tracing
description: Build a distributed trace across an AWS Lambda producer and consumer connected by an AWS Kinesis stream.
weight: 6
authors: ["Kate Hymers", "Guy-Francis Kono", "Updates: Bill Grant"]
time: 45 minutes
aliases:
  - /ninja-workshops/6-lambda-kinesis/
---

This workshop will equip you to build a distributed trace for a small serverless application that runs on AWS Lambda, producing and consuming a message via AWS Kinesis.

First, we will see how OpenTelemetry's auto-instrumentation captures traces and exports them to your target of choice.

Then, we will see how we can enable context propagation with manual instrumentation.

For this workshop Splunk has prepared an Ubuntu Linux instance in AWS/EC2 all pre-configured for you. To get access to that instance, please visit the URL provided by the workshop leader.
