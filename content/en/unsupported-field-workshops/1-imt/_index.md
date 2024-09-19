---
title: Splunk IM
linkTitle: Splunk IM
description: Splunk delivers real-time monitoring and troubleshooting to help you maximize infrastructure performance with complete visibility.
weight: 1
---

During this _**technical**_ Splunk Observability Cloud Infrastructure Monitoring and APM Workshop, you will build out an environment based on a [lightweight](https://k3s.io/) Kubernetes[^1] cluster.

To simplify the workshop modules, a pre-configured AWS/EC2 instance is provided.

The instance is pre-configured with all the software required to deploy the Splunk OpenTelemetry Connector[^2] in Kubernetes, deploy an NGINX^3 ReplicaSet^4 and finally deploy a microservices-based application which has been instrumented using OpenTelemetry to send metrics, traces, spans and logs[^5].

The workshops also introduce you to dashboards, editing and creating charts, creating detectors to fire alerts, Monitoring as Code and the Service Bureau[^6]

By the end of these technical workshops, you will have a good understanding of some of the key features and capabilities of the Splunk Observability Cloud.

Here are the instructions on how to access your pre-configured [AWS](./initial-setup/)/[EC2 instance](./initial-setup/)

![Splunk Architecture](images/architecture.png)

[^1]: [**Kubernetes**](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation.
[^2]: [**OpenTelemetry Collector**](https://opentelemetry.io/) offers a vendor-agnostic implementation on how to receive, process and export telemetry data. In addition, it removes the need to run, operate and maintain multiple agents/collectors to support open-source telemetry data formats (e.g. Jaeger, Prometheus, etc.) sending to multiple open-source or commercial back-ends.
[^3]: [**NGINX**](https://www.nginx.com/) is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.
[^4]: [**Kubernetes ReplicaSet**](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
[^5]: [**Jaeger**](https://www.jaegertracing.io/), inspired by Dapper and OpenZipkin, is a distributed tracing system released as open source by Uber Technologies. It is used for monitoring and troubleshooting microservices-based distributed systems
[^6]: [**Monitoring as Code and Service Bureau**](https://www.splunk.com/en_us/blog/it/monitoring-observability-enterprise-service.html)
