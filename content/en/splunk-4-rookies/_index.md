---
title: Infrastructure Monitoring and APM Workshop
linkTitle: Splunk4Rookies
description: Whether on-prem, hybrid or multicloud, Splunk delivers real-time monitoring and troubleshooting to help you maximize infrastructure performance with complete visibility.
weight: 1
---

During this Splunk4Rookies workshop we will be focusing on introducing you to Splunk Infrastructure Monitoring ([**IM**](https://www.splunk.com/en_us/products/infrastructure-monitoring.html)) and Splunk Application Performance Monitoring ([**APM**](https://www.splunk.com/en_us/products/apm-application-performance-monitoring.html)).

The workshop can be taken in two modes:

- **User Mode** - Requires only your browser to run through this interactive workshop. You will become familiar with navigating the UI and using the various features of the Splunk Observability Cloud for IM and APM. If you are new to Splunk Observability Cloud, this is the best place to start.

    Your instructor will provide you with all the details on how to login Splunk Observability Cloud and any additional URLs you will need to access during the workshop.
- **Ninja Mode** - Is the same as the above but will task you with more advanced steps where you will be using the command line to install and deploy the various components to get IM and APM data flowing into Splunk Observability Cloud. You will be provided with a pre-configured AWS/EC2 instance that you will use SSH to connect to.

    The instance is pre-configured with all the software required to deploy the Splunk OpenTelemetery Connector[^1] in Kubernetes, deploy a NGINX[^2] ReplicaSet[^3] and finally deploy a microservices based application which has been instrumented using OpenTelemetry to send metrics, traces and logs.

    Ninja Mode sections are marked with a {{% badge style="primary" icon=user-ninja title="" %}}**Ninja Mode**{{% /badge %}} badge and you will need to click on badge to expand the section to see the Ninja Mode instructions.

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja Mode:** Test Me!{{% /badge %}}" %}}
**You are officially a Ninja in training!**
{{% /expand %}}

By the end of the Splunk4Rookies Workshop you will have a good understanding of some of the key features and capabilities of Splunk IM and Splunk APM.

![Splunk Architecture](imt/images/architecture.png)

[^1]: The OpenTelemetry Collector offers a vendor-agnostic implementation on how to receive, process and export telemetry data. In addition, it removes the need to run, operate and maintain multiple agents/collectors in order to support open-source telemetry data formats (e.g. Jaeger, Prometheus, etc.) sending to multiple open-source or commercial back-ends.
[^2]: NGINX is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.
[^3]: [Kubernetes ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
