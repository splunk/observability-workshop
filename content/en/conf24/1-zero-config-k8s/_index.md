---
title: Spring PetClinic SpringBoot Based Microservices On Kubernetes
linkTitle: PetClinic Kubernetes Workshop
weight: 1
archetype: chapter
description: Learn how to enable Open Telemetry Zero-Config Auto-Instrumention for your Java-based application running in Kubernetes. Experience real-time monitoring to help you maximize application behavior with end-to-end visibility.
draft: true
authors: ["Pieter Hagen"]
---

The goal of this workshop is to introduce the features of Splunk's Opentelemetry **Zero-Config Auto-Instrumentation** for Java.

The workshop scenario will be created by installing a simple Java microservices application in Kubernetes.

By following the basic steps to install the OpenTelemetry Collector in Kubernetes and enable Zero-Config Auto-Instrumentation on the existing Java application running in Kubernetes.  This  will start sending Opentelemetry metrics, traces and logs to the **Splunk Observability Cloud** platform and enable the following components:

* Splunk Infrastructure Monitoring (**IM**)
* Splunk Auto Instrumentation for Java (**APM**)
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Log Observer (**LO**)
* Splunk Real User Monitoring (**RUM**)
