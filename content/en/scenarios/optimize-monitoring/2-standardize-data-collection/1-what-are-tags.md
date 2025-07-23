---
title: What Are Tags?
linkTitle: 2.1 What Are Tags?
weight: 2
authors: ["Tim Hard"]
time: 3 minutes
draft: false
---

Tags are key-value pairs that provide additional metadata about metrics, spans in a trace, or logs allowing you to enrich the context of the data you send to **Splunk Observability Cloud**. Many tags are collected by default such as hostname or OS type. Custom tags can be used to provide environment or application-specific context. Examples of custom tags include:

###### Infrastructure specific attributes

* What data center a host is in
* What services are hosted on an instance
* What team is responsible for a set of hosts

###### Application specific attributes

* What Application Version is running
* Feature flags or experimental identifiers
* Tenant ID in multi-tenant applications

###### User related attributes

* User ID
* User role (e.g. admin, guest, subscriber)
* User geographical location (e.g. country, city, region)

###### There are two ways to add tags to your data

* Add tags as OpenTelemetry attributes to metrics, traces, and logs when you send data to the Splunk Distribution of OpenTelemetry Collector. This option lets you add spans in bulk.
* Instrument your application to create span tags. This option gives you the most flexibility at the per-application level.

### Why are tags so important?

Tags are essential for an application to be truly observable. Tags add context to the traces to help us understand why some users get a great experience and others don't. Powerful features in **Splunk Observability Cloud** utilize tags to help you jump quickly to the root cause.

**Contextual Information:** Tags provide additional context to the metrics, traces, and logs allowing developers and operators to understand the behavior and characteristics of infrastructure and traced operations.

**Filtering and Aggregation:** Tags enable filtering and aggregation of collected data. By attaching tags, users can filter and aggregate data based on specific criteria. This filtering and aggregation help in identifying patterns, diagnosing issues, and gaining insights into system behavior.

**Correlation and Analysis:** Tags facilitate correlation between metrics and other telemetry data, such as traces and logs. By including common identifiers or contextual information as tags, users can correlate metrics, traces, and logs enabling comprehensive analysis and troubleshooting of distributed systems.

**Customization and Flexibility:** OpenTelemetry allows developers to define custom tags based on their application requirements. This flexibility enables developers to capture domain-specific metadata or contextual information that is crucial for understanding the behavior of their applications.

### Attributes vs. Tags

A note about terminology before we proceed. While this workshop is about **tags**, and this is the terminology we use in **Splunk Observability Cloud**, OpenTelemetry uses the term **attributes** instead. So when you see tags mentioned throughout this workshop, you can treat them as synonymous with attributes.
