### µAPM architecture
SignalFx µAPM captures end-to-end distributed transactions from your applications, with trace spans sent directly to SignalFx or via the SignalFx Smart Agent deployed on each host (recommended). Optionally, you can deploy an OpenTelemetry Collector to act as a central aggregation point prior to sending trace spans to SignalFx. In addition to proxying spans and infrastructure metrics, the OpenTelemetry Collector can also perform other functions, such as redacting sensitive tags prior to spans leaving your environment.

The following illustrations show the recommended deployment model: SignalFx auto-instrumentation libraries send spans to the Smart Agent; the Smart Agent can send the spans to SignalFx directly or via an optional OpenTelemetry Collector.

![Architecture Ove4view](../images/module6/arch-overview.png#shadow) 


---

Use the **Next** link in the footer below to continue the workshop
