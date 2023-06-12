---
title: Newbie to Ninja - OpenTelemetry Collector
linkTitle: Newbie to Ninja - OpenTelemetry Collector
description: This workshop will equip you with the basic understanding of monitoring Kubernetes using the Splunk OpenTelemetry Collector
weight: 2
alwaysopen: false
---

### Abstract

Adopting OpenTelemetry within your organisation can bring issues such as dealing with metric naming changes, rollout, and where to start. In this workshop, we will be focusing on using the OpenTelemetry collector and starting with the fundamentals of configuring the receivers, processors, and exporters ready to use with Splunk Cloud. The journey will take attendees from novices to being able to start adding custom components to help solve for their business observability needs for their distributed platform.

Throughout the workshop there will be **🥷 Ninja** sections that will be more hands on and go into further technical detail that you can explore within the workshop or in your own time. Please note that the content in these sections may go out of date due to the frequent development being made to the OpenTelemetry project. Links will be provided in the event details are out of sync, please let us know if you spot something that needs updating.

### Target Audience

This talk is for developers and system administrators who are interested in learning more about architecture and deployment of the OpenTelemetry Collector.

### Prerequisites

- Attendees should have a basic understanding of distributed systems and data collection.
- A instance/host/VM running Ubuntu 20.04 LTS or 22.04 LTS.
- Command line and vim/vi experience.

### Learning Objectives

By the end of this talk, attendees will be able to:

- Understand the components of OpenTelemetry
- Use receivers, processors, and exporters to collect, instrument, and analyze data from distributed systems
- Identify the benefits of using OpenTelemetry
- Building a custom component to solve for their business needs

{{< mermaid >}}
%%{
  init:{
    "theme":"base",
    "themeVariables": {
      "primaryColor": "#ffffff",
      "clusterBkg": "#eff2fb",
      "defaultLinkColor": "#333333"
    }
  }
}%%

flowchart LR;
    subgraph Collector
    A[OTLP] --> M(Receivers)
    B[JAEGER] --> M(Receivers)
    C[Prometheus] --> M(Receivers)
    end
    subgraph Processors
    M(Receivers) --> H(Filters, Attributes, etc)
    E(Extensions)
    end
    subgraph Exporters
    H(Filters, Attributes, etc) --> S(OTLP)
    H(Filters, Attributes, etc) --> T(JAEGER)
    H(Filters, Attributes, etc) --> U(Prometheus)
    end
{{< /mermaid >}}
