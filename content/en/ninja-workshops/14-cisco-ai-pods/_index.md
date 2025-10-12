---
title: Monitoring Cisco AI Pods with Splunk Observability Cloud 
linkTitle: Monitoring Cisco AI Pods with Splunk Observability Cloud
weight: 14
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: This hands-on workshop demonstrates how to monitor Cisco AI Pods with Splunk Observability Cloud. Learn to deploy the OpenTelemetry Collector in Red Hat OpenShift, ingest infrastructure metrics using Prometheus receivers, and configure APM to monitor Python services that interact with Large Language Models (LLMs). 
draft: false
hidden: false
---

**Cisco’s AI-ready PODs** combine the best of hardware and software technologies to create a robust, 
scalable, and efficient AI-ready infrastructure tailored to diverse needs.

**Splunk Observability Cloud** provides comprehensive visibility into all of this infrastructure 
along with all the application components that are running on this stack.

The steps to configure Splunk Observability Cloud for a Cisco AI POD environment are fully 
documented (see [here](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods)
for details). 

However, it's not always possible to get access to a Cisco AI POD environment to practice 
the installation steps.

This workshop provides hands-on experience deploying and working with several of the technologies
that are used to monitor Cisco AI PODs with Splunk Observability Cloud, without requiring 
access to an actual Cisco AI POD.  This includes: 

* Practice deploying a **RedHat OpenShift** cluster with GPU-based worker nodes.
* Practice deploying the **NVIDIA NIM Operator** and **NVIDIA GPU Operator**.
* Practice deploying **Large Language Models (LLMs)** using NVIDIA NIM to the cluster.
* Practice deploying the **OpenTelemetry Collector** in the Red Hat OpenShift cluster.
* Practice adding **Prometheus** receivers to the collector to ingest infrastructure metrics.
* Practice deploying the **Weaviate** vector database to the cluster.
* Practice instrumenting Python services that interact with Large Language Models (LLMs) with **OpenTelemetry**.
* Understanding which details which OpenTelemetry captures in the trace from applications that interact with LLMs.

> Please note: Red Hat OpenShift and NVIDIA AI Enterprise components 
> are typically pre-installed with an actual AI POD. However, because we’re using AWS for this workshop, 
> it’s necessary to perform these setup steps manually.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
  {{% /notice %}}
