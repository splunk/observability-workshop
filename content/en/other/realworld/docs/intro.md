---
title: Introduction
weight: 1
---

The goal of this workshop is to focus on the art of doing observability with Splunk Observability Cloud.

### Questions to think about
* We learn about sending metrics, traces and logs, but do we know why?
* We frequently start with logs. How can we do better?
* When something goes wrong, and we only have logs to rely on (to be alerted on and to get to the bottom of the problem), is there a better way?

To get the full experience it's really important that you go through this workshop in order. While the systems will change (based on what we learn), the discussions are what's important. Conclusions you make may even influence a future version of this workshop!

### Things to keep in mind
* We are presenting this in the context of Splunk, and we will show you how to achieve that in Splunk, but as you think about the questions you can think about them in the context of capabilities, not products.
* The answers provided are just suggested answers. There is no single answer. One of your answers may be added to a future version of the workshop!

### Draft Outline

* Event 1: Starve Kubernetes of resources
  * Should be able to solve this issue in Kubernetes Navigator
  * Resolve that change
* Event 2: Cause disk space issue
  * Should be able to solve on an infrastructure dashboard
  * Add a detector to find this proactively
* Event 3: Starve Kafka of resources
  * Solve in logs?
  * Discuss what we could do better
  * Implement Kafka collection
  * Show Kafka dashboard
  * Create detector on Kafka
* Event 4: Slow down a database query
  * Scenario is that a customer calls in to complain about slowness
  * Discuss that we have nothing looking at the application
  * Implement Java collection
  * Show how the database analyzer can surface this issue
* Event 5: Release a new version of "currency converter"
  * See slow downs in the map
  * How would we know it was the new version?
  * Introduce version to the instrumentation
  * Introduce version event to dashboards
  * How would we know it is specific to just one of the currencies?
  * Introduce span tag of currency from the conversion

### Application
* 5 microservices
* 1 or 2 languages
* OTS components (Kafka and DB)

[Go to Initial State](../initial_state)