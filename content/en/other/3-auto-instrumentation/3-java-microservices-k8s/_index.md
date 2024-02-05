---
title: Workshop using the Java microservices Pet Clinic demo (Kubernetes based).
linkTitle: PetClinic Java Microservices Workshop (Kubernetes)
weight: 99
description: Learn how to enable Open Telemetry (Auto) Instrumentation for your Java-based application running in Kubernetes. Experience real-time monitoring and troubleshooting to help you maximize application behavior with end-to-end visibility.
hidden: false
---

The goal of this workshop is to introduce the features of Splunk's Opentelemetry Java Auto instrumentation.
First we create the workshop scenario, by installing a simple Java microservices application in Kubernetes.
We then walk through the basic steps to set up the OpenTelemetry Collector in Kubernetes, and enable auto-instrumentation on the existing Java application running in Kubernetes.  This  will start sending Opentelemetry signals to **Splunk Observability Cloud** platform and enable the following components:

* Splunk Infrastructure Monitoring (IM)
* Splunk Auto Instrumentation for Java (APM)
  * Database Query Performance
  * AlwaysOn Profiling
<!--   to be completed in  version 2.0
* Splunk Real User Monitoring (RUM)
* RUM to APM Correlation
-->
* Splunk Log Observer (LO)

We will show the steps about how to clone (download) a sample microservices Java application (Spring PetClinic), as well as how to compile, package and deploy/run the application.

Once the application is up and running, we will examine the default metrics send by the Opentelemetry Collector in the **Splunk Observability UI** Next, when auto instrumentation is enabled we will start seeing metrics and traces created via the **Auto Instrumentation** for Java that will be used by the **Splunk APM** product.

We also will examine Always-on Profiling and Database Query performance.

<!--  to be completed in version 2.0
After that, we will instrument PetClinic's end user interface (HTML pages rendered by the application) with the **Splunk OpenTelemetry Javascript Libraries (RUM)** that will generate RUM traces around all the individual clicks and page loads executed by an end user.
-->

Lastly, we will configure the Spring PetClinic application to inject trace information into the application logs and send them to **Splunk Cloud**.

{{% notice title="Prerequisites" style="primary" icon="info" %}}

* Outbound SSH access to port `2222`.
* Outbound HTTP access to port `81`.
* Familiarity with the `bash` shell and `vi/vim/nano` editor.

{{% /notice %}}
![Splunk Otel Architecture](images/auto-instrumentation-java-diagram.png)

---
Based on the [example](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/enable-operator-and-auto-instrumentation/spring-petclinic-java.md) **Josh Voravong** has created.
