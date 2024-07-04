---
title: Splunk IM
linkTitle: Splunk IM
description: Splunk delivers real-time monitoring and troubleshooting to help you maximize infrastructure performance with complete visibility.
weight: 1
---

During this _**technical**_ Splunk Observability Cloud Infrastructure Monitoring Workshop, you will build out an environment based on a [lightweight](https://k3s.io/) Kubernetes[^1] cluster.

To simplify the workshop modules, a pre-configured AWS/EC2 instance is provided and the instructor will provide you with the login information for the instance that you will be using during the workshop.

The instance is pre-configured with all the software required to deploy the Splunk OpenTelemetry Connector[^2] in Kubernetes, deploy an NGINX^3 ReplicaSet^4 and finally deploy a microservices-based application which has been instrumented using OpenTelemetry to send metrics, traces, spans and logs[^5].

The workshops also introduce you to dashboards, navigators editing and creating charts, creating detectors to fire alerts, Monitoring as Code and the Service Bureau[^6]

### Connect via SSH

When you first log into your instance, you will be greeted by the Splunk Logo as shown below. If you have any issues connecting to your workshop instance then please reach out to your Instructor.

``` text
$ ssh -p 2222 splunk@<ip-address>

███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗  
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗ 
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝ 
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  
Last login: Mon Feb  5 11:04:54 2024 from [Redacted]
Waiting for cloud-init status...
Your instance is ready!
splunk@show-no-config-i-0d1b29d967cb2e6ff:~$ 
```

To ensure your instance is configured correctly, we need to confirm that the required environment variables for this workshop are set correctly. In your terminal run the following script and check that the environment variables are present and set with actual valid values:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
. ~/workshop/petclinic/scripts/check_env.sh
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
ACCESS_TOKEN = <redacted>
REALM = <e.g. eu0, us1, us2, jp0, au0 etc.>
RUM_TOKEN = <redacted>
HEC_TOKEN = <redacted>
HEC_URL = https://<...>/services/collector/event
INSTANCE = <instance_name>
```

{{% /tab %}}
{{< /tabs >}}

Please make a note of the `INSTANCE` environment variable value as this will used later to filter data in **Splunk Observability Cloud**.

For this workshop, **all** of the above are required. If any have values missing, please contact your Instructor.


![Splunk Architecture](images/architecture.png)

[^1]: [**Kubernetes**](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation.
[^2]: [**OpenTelemetry Collector**](https://opentelemetry.io/) offers a vendor-agnostic implementation on how to receive, process and export telemetry data. In addition, it removes the need to run, operate and maintain multiple agents/collectors to support open-source telemetry data formats (e.g. Jaeger, Prometheus, etc.) sending to multiple open-source or commercial back-ends.
[^3]: [**NGINX**](https://www.nginx.com/) is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.
[^4]: [**Kubernetes ReplicaSet**](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
[^5]: [**Jaeger**](https://www.jaegertracing.io/), inspired by Dapper and OpenZipkin, is a distributed tracing system released as open source by Uber Technologies. It is used for monitoring and troubleshooting microservices-based distributed systems
[^6]: [**Monitoring as Code and Service Bureau**](https://www.splunk.com/en_us/blog/it/monitoring-observability-enterprise-service.html)
