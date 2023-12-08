---
title: PetClinic Java Workshop
weight: 1
description: A workshop using Zero Configuration Auto-Instrumentation for Java.
hidden: true
---

The goal is to walk through the basic steps to configure the following components of the Splunk Observability platform:

* Splunk Infrastructure Monitoring (IM)
* Splunk Zero Configuration Auto Instrumentation for Java (APM)
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Real User Monitoring (RUM)
* RUM to APM Correlation
* Splunk Log Observer

We will also show the steps about how to clone (download) a sample Java application (Spring PetClinic), as well as how to compile, package and run the application.

Once the application is up and running, we will instantly start seeing metrics and traces via the Zero Configuration Auto Instrumentation for Java that will be used by the Splunk APM product.

After that, we will instrument PetClinic's end user interface (HTML pages rendered by the application) with the Splunk OpenTelemetry Javascript Libraries (RUM) that will generate RUM traces around all the individual clicks and page loads executed by an end user.

Lastly, we will configure the Spring PetClinic application to write application logs to the filesystem and also configure the Splunk OpenTelemetry Collector to read (tail) the logs and send them to Splunk Cloud.

{{% notice title="Prerequisites" style="info" %}}
A Splunk-run workshop where a host/instance is provided  **OR** a self-led workshop on your own host / [multipass instance](https://github.com/splunk/observability-workshop/tree/main/multipass)

For your own system, you will need the following installed and enabled:

1. JDK 17 installed
2. Maven
3. Port `8083` open inbound/outbound
{{% /notice %}}

![PetClinic Exercise](images/petclinic-exercise.png)
