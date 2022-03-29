---
title: Getting Started
weight: 1
---

The goal is to walk through the basic steps to configure the following components of the Splunk Observability platform:

1. Splunk Infrastructure Monitoring (IM)
2. Splunk Application Performance Monitoring (APM)
3. Splunk Real User Monitoring (RUM)
4. Splunk LogsObserver (LO)

We will also show the steps about how to clone (download) a sample java application (Spring PetClinic), as well as how to compile, package and run the application.

Once the application is up and running, we will instrument the application using Splunk OpenTelemetry Java Instrumentation libraries that will generate traces and metrics used by the Splunk APM product.

After that, we will instrument the PetClinic's end user interface (HTML pages rendered by the application) with the Splunk OpenTelemetry Javascript Libraries (RUM) that will generate RUM traces about all the individual clicks and page loads executed by the end user.

Lastly, we will configure the Spring PetClinic application to write application logs to the filesystem and also configure the Splunk OpenTelemetry Collector to read (tail) the logs and report to Splunk Observability Cloud.

Here's a diagram of the final state of this exercise:

![PetClinic Exercise](../../../images/petclinic-exercise.png)
