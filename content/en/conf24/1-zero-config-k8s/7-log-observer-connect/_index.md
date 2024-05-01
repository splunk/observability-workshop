---
title: Log Observer
linkTitle: 7. Log Observer
weight: 8
archetype: chapter
time: 10 minutes
---

Up until this point, there have been no code changes, yet tracing, profiling and Database Query Performance data is being sent to Splunk Observability Cloud.

Next we will add the **Splunk Log Observer** to the mix to obtain log data from the Spring PetClinic application.

This change will update the configuration of [**logback**](https://logback.qos.ch/) in the Spring PetClinic application. This will allow the Auto Instrumentation to add OpenTelemetry relevant information into the logs.

The **Splunk Log Observer** is then used to view the logs and with the changes to the log format the platform can automatically correlate log information with services and traces.

This feature is called [**Related Content**](https://docs.splunk.com/observability/en/metrics-and-metadata/relatedcontent.html).
