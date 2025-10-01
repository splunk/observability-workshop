---
title: Monitoring Cisco AI Pods with Splunk Observability Cloud 
linkTitle: Monitoring Cisco AI Pods with Splunk Observability Cloud
weight: 14
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: By the end of this workshop you'll have experience deploying and working several of the technologies that are used to monitor Cisco AI Pods with Splunk Observability Cloud.  This includes deploying an OpenTelemetry Collector in a Red Hat OpenShift cluster, using Prometheus receivers with the collector to ingest infrastructure metrics, and configuring APM to monitor Python services that interact with Large Language Models (LLMs). 
draft: false
hidden: false
---

**Cisco’s AI-ready PODs** combine the best of hardware and software technologies to create a robust, 
scalable, and efficient AI-ready infrastructure tailored to diverse needs.

**Splunk Observability Cloud** provides comprehensive visibility into all of this infrastructure 
along with all the application components that are running on this stack.

This workshop provides hands-on experience deploying and working with several of the technologies
that are used to monitor Cisco AI PODs with Splunk Observability Cloud, including:

* Practice deploying an OpenTelemetry Collector in a Red Hat OpenShift cluster.
* Practice configuring Prometheus receivers with the collector to ingest infrastructure metrics.
* Practice instrumenting Python services that interact with Large Language Models (LLMs) with OpenTelemetry. 

While access to an actual Cisco AI POD isn't required, the workshop **does** require access 
to an AWS account.  We'll walk you through the steps of creating a Red Hat OpenShift 
cluster in AWS that we'll use for the rest of the workshop. 

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
  {{% /notice %}}
