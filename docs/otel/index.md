# Introduction

During this _**technical**_ Splunk Observability Cloud Workshop you will build out an environment based on a [lightweight](https://k3s.io/){: target=_blank} Kubernetes[^1] cluster.

In order to simplify the Workshop modules, a pre-configured AWS/EC2 instance is provided.

The instance is pre-configured with all the software required to deploy the OpenTelemetery Collector[^2] in Kubernetes, deploy a NGINX[^3] ReplicaSet[^4] and finally deploy a microservices based application which has been instrumented using OpenTelemetry to send metrics, traces and spans[^5].

The Workshop also introduces you to dashboards, editing and creating charts, creating detectors to fire alerts, Monitoring as Code[^6] and the Service Bureau[^6]

By the end of this technical workshop you will have a good understanding of some of the key features and capabilities of the Splunk Observability Cloud.

Here are the instructions on how to access you pre-configured [AWS/EC2 instance](../otel/connect-info/)

![Splunk Architecture](../images/otel/architecture.png)

[^1]: [Kubernetes](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation.
[^2]: The OpenTelemetry Collector offers a vendor-agnostic implementation on how to receive, process and export telemetry data. In addition, it removes the need to run, operate and maintain multiple agents/collectors in order to support open-source telemetry data formats (e.g. Jaeger, Prometheus, etc.) sending to multiple open-source or commercial back-ends.
[^3]: NGINX is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.
[^4]: [Kubernetes ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/){: target=_blank}
[^5]: Jaeger, inspired by Dapper and OpenZipkin, is a distributed tracing system released as open source by Uber Technologies. It is used for monitoring and troubleshooting microservices-based distributed systems
[^6]: [Monitoring as Code and Service Bureau](https://www.splunk.com/en_us/blog/it/monitoring-observability-enterprise-service.html){: target=_blank}
