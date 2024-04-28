---
title: Architecture
linkTitle: 1. Architecture
weight: 2
---

The diagram below details the architecture of the Spring PetClinic Java application running in Kubernetes with the Splunk OpenTelemetry Operator and Auto-Instrumentation enabled.

The Spring PetClinic Java application is a simple microservices application that consists of a frontend and backend services. The frontend service is a Spring Boot application that serves a web interface to interact with the backend services. The backend services are Spring Boot applications that serve RESTful API's to interact with a MySQL database.

By the end of this workshop, you will have a better understanding of how to enable **Splunk OpenTelemetry Zero-Config Auto-Instrumentation** for your Java-based applications running in Kubernetes.

![Splunk Otel Architecture](../images/auto-instrumentation-java-diagram.png)

---
Based on the [**example**](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/enable-operator-and-auto-instrumentation/spring-petclinic-java.md) **Josh Voravong** has created.
