---
title: Optimize Cloud Monitoring
linkTitle: 1. Optimize Cloud Monitoring
weight: 1
archetype: chapter
authors: ["Tim Hard"]
time: 2 minutes
draft: true
---

{{% badge icon="clock" style="primary" %}}5 minutes{{% /badge %}} {{% badge style="blue" title="Authors" %}}Tim Hard{{% /badge %}}

The elasticity of cloud architectures means that monitoring artifacts must scale elastically as well, breaking the paradigm of purpose-built monitoring assets. As a result, administrative overhead, visibility gaps, and tech debt skyrocket while MTTR slows. This typically happens for three reasons:

* **Complex and Inefficient Data Management**: Infrastructure data is scattered across multiple tools with inconsistent naming conventions, leading to fragmented views and poor metadata and labeling. Managing multiple agents and data flows adds to the complexity.
* **Inadequate Monitoring and Troubleshooting Experience**: Slow data visualization and troubleshooting, cluttered with bespoke dashboards and manual correlations, are hindered further by the lack of monitoring tools for ephemeral technologies like Kubernetes and serverless functions.
* **Operational and Scaling Challenges**: Manual onboarding, user management, and chargeback processes, along with the need for extensive data summarization, slow down operations and inflate administrative tasks, complicating data collection and scalability.

In order to address these challenges you need a way to:

* **Standardize Data Collection and Tags**: Centralized monitoring with a single, open-source agent to apply uniform naming standards and ensure metadata for visibility. Optimize data collection and use a monitoring-as-code approach for consistent collection and tagging.
* **Reuse Content Across Teams**: Streamline new IT infrastructure onboarding and user management with templates and automation. Utilize out-of-the-box dashboards, alerts, and self-service tools to enable content reuse, ensuring uniform monitoring and reducing manual effort.
* **Improve Timeliness of Alerts**: Utilize highly performant open source data collection, combined with real-time streaming-based data analytics and alerting, to enhance the timeliness of notifications. Automatically configured alerts for common problem patterns (AutoDetect) and minimal yet effective monitoring dashboards and alerts will ensure rapid response to emerging issues, minimizing potential disruptions.
* **Correlate Infrastructure Metrics and Logs**: Achieve full monitoring coverage of all IT infrastructure by enabling seamless correlation between infrastructure metrics and logs. High-performing data visualization and a single source of truth for data, dashboards, and alerts will simplify the correlation process, allowing for more effective troubleshooting and analysis of the IT environment.

In this workshop, we'll explore:

* How to standardize data collection and tags using **OpenTelemetry**. 
* How to reuse content across teams. 
* How to improve timeliness of alerts. 
* How to correlate infrastructure metics and logs. 

During this _**technical**_ Optimize Cloud Monitoring Workshop, you will build out an environment based on a [lightweight](https://k3s.io/) Kubernetes[^1] cluster.

To simplify the workshop modules, a pre-configured AWS/EC2 instance is provided.

The instance is pre-configured with all the software required to deploy the Splunk OpenTelemetry Connector[^2] in Kubernetes and the microservices-based OpenTelemetry Demo Application[^3] which has been instrumented using OpenTelemetry to send metrics, traces, spans and logs.

The workshops also introduce you to dashboards and how they can be re-used across teams, jpwcreating detectors to fire alerts

By the end of these technical workshops, you will have a good understanding of some of the key features and capabilities of the Splunk Observability Cloud.

Here are the instructions on how to access your pre-configured [AWS](./getting_started/)/[EC2 instance](./getting_started/)

![Splunk Architecture](images/architecture.png)

[^1]: [**Kubernetes**](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation.
[^2]: [**OpenTelemetry Collector**](https://opentelemetry.io/) offers a vendor-agnostic implementation on how to receive, process and export telemetry data. In addition, it removes the need to run, operate and maintain multiple agents/collectors to support open-source telemetry data formats (e.g. Jaeger, Prometheus, etc.) sending to multiple open-source or commercial back-ends.
[^3]: The [**OpenTelemetry Demo Application**](https://opentelemetry.io/docs/demo/) is a microservice-based distributed system intended to illustrate the implementation of OpenTelemetry in a near real-world environment.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
  {{% /notice %}}