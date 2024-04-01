---
title: Getting Started
linkTitle: 1. Getting Started
weight: 1
authors: ["Tim Hard"]
time: 3 minutes
draft: true
---

During this _**technical**_ Optimize Cloud Monitoring Workshop, you will build out an environment based on a [lightweight](https://k3s.io/) Kubernetes[^1] cluster.

To simplify the workshop modules, a pre-configured AWS/EC2 instance is provided.

The instance is pre-configured with all the software required to deploy the Splunk OpenTelemetry Connector[^2] and the microservices-based OpenTelemetry Demo Application[^3] in Kubernetes which has been instrumented using OpenTelemetry to send metrics, traces, spans and logs.

This workshop will introduce you to the benefits of standardized data collection, how content can be re-used across teams, correlating metrics and logs, and creating detectors to fire alerts. By the end of these technical workshops, you will have a good understanding of some of the key features and capabilities of the Splunk Observability Cloud.

Here are the instructions on how to access your pre-configured [AWS/EC2 instance](./1-access-ec2/)

![Splunk Architecture](../images/architecture.png)

[^1]: [**Kubernetes**](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation.
[^2]: [**OpenTelemetry Collector**](https://opentelemetry.io/) offers a vendor-agnostic implementation on how to receive, process and export telemetry data. In addition, it removes the need to run, operate and maintain multiple agents/collectors to support open-source telemetry data formats (e.g. Jaeger, Prometheus, etc.) sending to multiple open-source or commercial back-ends.
[^3]: The [**OpenTelemetry Demo Application**](https://opentelemetry.io/docs/demo/) is a microservice-based distributed system intended to illustrate the implementation of OpenTelemetry in a near real-world environment.
