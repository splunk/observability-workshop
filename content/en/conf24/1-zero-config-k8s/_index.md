---
title: Java microservices Pet Clinic demo (Kubernetes-based).
linkTitle: PetClinic Java Microservices Workshop (Kubernetes)
weight: 1
archetype: chapter
description: Learn how to enable Open Telemetry (Auto) Instrumentation for your Java-based application running in Kubernetes. Experience real-time monitoring and troubleshooting to help you maximize application behavior with end-to-end visibility.
draft: true
---

The goal of this workshop is to introduce the features of Splunk's Opentelemetry Zero-Config Auto instrumentation for Java.

First, we create the workshop scenario, by installing a simple Java microservices application in Kubernetes.

We then walk through the basic steps to set up the OpenTelemetry Collector in Kubernetes and enable auto-instrumentation on the existing Java application running in Kubernetes.  This  will start sending Opentelemetry signals to the **Splunk Observability Cloud** platform and enable the following components:

* Splunk Infrastructure Monitoring (IM)
* Splunk Auto Instrumentation for Java (APM)
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Log Observer (LO)

<!--   to be completed in  version 2.0
* Splunk Real User Monitoring (RUM)
* RUM to APM Correlation
-->
