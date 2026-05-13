---
title: Distributed Tracing and Bi-Directional Drilldowns
linkTitle: 4. Distributed Tracing
weight: 4
time: 25 minutes
description: Enable supported trace correlation between ThousandEyes and Splunk APM so teams can move between the two products during an investigation.
---

This section turns the ThousandEyes and Splunk integration into a true investigation workflow. In the previous section, ThousandEyes streamed synthetic metrics into Splunk Observability Cloud. In this section, you will enable the supported **ThousandEyes <-> Splunk APM distributed tracing integration** so network, platform, and application teams can pivot between both tools while looking at the same request.

{{% notice title="Why This Matters" style="primary" icon="lightbulb" %}}
This is the piece that gives you **bi-directional access** between the two environments. ThousandEyes can open the related trace in Splunk APM, and Splunk APM can take you back to the originating ThousandEyes test.
{{% /notice %}}

## What You Will Learn

By the end of this section, you will be able to:

- Instrument an internal service so it sends traces to Splunk APM
- Enable distributed tracing on a ThousandEyes **HTTP Server** or **API** test
- Configure the ThousandEyes **Generic Connector** for Splunk APM
- Open the ThousandEyes **Service Map** and jump directly into the corresponding Splunk trace
- Use the ThousandEyes metadata in Splunk APM to jump back to the original ThousandEyes test





