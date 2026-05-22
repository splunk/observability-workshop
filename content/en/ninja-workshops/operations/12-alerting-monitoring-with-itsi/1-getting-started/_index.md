---
title: Getting Started
linkTitle: 1. Getting Started
weight: 1
---

# Monitoring and Alerting with Splunk, AppDynamics, and Splunk Observability Cloud

## Introduction and Overview

In today's complex IT landscape, ensuring the performance and availability of applications and services is paramount.  This workshop will introduce you to a powerful combination of tools – Splunk, AppDynamics, Splunk Observability Cloud, and Splunk IT Service Intelligence (ITSI) – that work together to provide comprehensive monitoring and alerting capabilities.

### The Challenge of Modern Monitoring

Modern applications often rely on distributed architectures, microservices, and cloud infrastructure.  This complexity makes it challenging to pinpoint the root cause of performance issues or outages.  Traditional monitoring tools often focus on individual components, leaving gaps in understanding the overall health and performance of a service.

### The Solution: Integrated Observability

A comprehensive observability strategy requires integrating data from various sources and correlating it to gain actionable insights.  This workshop will demonstrate how Splunk, AppDynamics, Splunk Observability Cloud, and ITSI work together to achieve this:

* **Splunk:**  Acts as the central platform for log analytics, security information and event management (SIEM), and broader data analysis.  It ingests data from AppDynamics, Splunk Observability Cloud, and other sources, enabling powerful search, visualization, and correlation capabilities.  Splunk provides a holistic view of your IT environment.

* **Splunk Observability Cloud:** Offers full-stack observability, encompassing infrastructure metrics, distributed traces, and logs. It provides a unified view of the health and performance of your entire infrastructure, from servers and containers to cloud services and custom applications. Splunk Observability Cloud helps correlate performance issues across the entire stack.

* **AppDynamics:**  Provides deep Application Performance Monitoring (APM).  It instruments applications to capture detailed performance metrics, including transaction traces, code-level diagnostics, and user experience data.  AppDynamics excels at identifying performance bottlenecks *within* the application.

* **Splunk IT Service Intelligence (ITSI):**  Provides service intelligence by correlating data from all the other platforms.  ITSI allows you to define services, map dependencies, and monitor Key Performance Indicators (KPIs) that reflect the overall health and performance of those services.  ITSI is essential for understanding the *business impact* of IT issues.

### Data Flow and Integration

A key concept to understand is how data flows between these platforms:

1. **Splunk Observability Cloud and AppDynamics collect data:**  They monitor applications and infrastructure, gathering performance metrics and traces.

2. **Data is sent to Splunk:**  AppDynamics and Splunk Observability Cloud integrate with Splunk to forward their collected data alongside logs sent directly to Splunk.

3. **Splunk analyzes and indexes data:** Splunk processes and stores the data, making it searchable and analyzable.

4. **ITSI leverages Splunk data:** ITSI uses the data in Splunk to create services, define KPIs, and monitor the overall health of your IT operations.

### Workshop Objectives

By the end of this workshop, you will:

* Understand the complementary roles of Splunk, AppDynamics, Splunk Observability Cloud, and ITSI.
* Create basic alerts in Splunk, Observability Cloud and AppDynamics.
* Configure a new Service and a simple KPI and alerting in ITSI.
* Understand the concept of episodes in ITSI.

This workshop provides a foundation for building a robust observability practice. We will focus on the alerting configuration workflows, preparing you to explore more advanced features and configurations in your own environment. We will **not** be covering ITSI or Add-On installation and configuration.

Here are the instructions on how to access your pre-configured [Splunk Enterprise Cloud](./1-access-cloud-instances/) instance.