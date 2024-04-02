---
title: Standardize Data Collection
linkTitle: 2. Standardize Data Collection
weight: 1
authors: ["Tim Hard"]
time: 2 minutes
draft: false
---

## Why Standards Matter

As cloud adoption grows, we often face requests to support new technologies within a diverse landscape, posing challenges in delivering timely content. Take, for instance, a team containerizing five workloads on AWS requiring EKS visibility. Usually, this involves assisting with integration setup, configuring metadata, and creating dashboards and alerts—a process that's both time-consuming and increases administrative overhead and technical debt.

**Splunk Observability Cloud** was designed to handle customers with a diverse set of technical requirements and stacks – from monolithic to microservices architectures, from homegrown applications to Software-as-a-Service. 

Splunk offers a native experience for OpenTelemetry, which means OTel is the preferred way to get data into Splunk.
Between Splunk’s integrations and the OpenTelemetry community, there are a number of integrations available to easily collect from diverse infrastructure and applications. This includes both on-prem systems like VMWare and as well as guided integrations with cloud vendors, centralizing these hybrid environments.

![Splunk Observability Cloud Integrations](../images/integrations.png?width=50vw)

For someone like a Splunk admin, the OpenTelemetry Collector can additionally be deployed to a Splunk Universal Forwarder as a [Technical Add-on](https://splunkbase.splunk.com/app/7125). This enables fast roll-out and centralized configuration management using the Splunk Deployment Server. 
Let’s assume that the same team adopting Kubernetes is going to deploy a cluster for each one of our B2B customers.  I’ll show you how to make a simple modification to the OpenTelemetry collector to add the customerID, and then use mirrored dashboards to allow any of our SRE teams to easily see the customer they care about. 
