---
title: TBD
linkTitle: 6.1 TBD
weight: 1
time: 10 minutes
description: TBD
draft: true
---

## Supported Workflow

This learning scenario follows the supported workflow documented by ThousandEyes and Splunk:

- ThousandEyes automatically injects `b3`, `traceparent`, and `tracestate` headers into **HTTP Server** and **API** tests when distributed tracing is enabled.
- The monitored endpoint must accept headers, be instrumented with OpenTelemetry, propagate trace context, and send traces to your observability backend.
- For Splunk APM, ThousandEyes uses a **Generic Connector** that points at `https://api.<REALM>.signalfx.com` and authenticates with an **API-scope** Splunk token.
- Splunk APM enriches matching traces with ThousandEyes attributes such as `thousandeyes.test.id` and `thousandeyes.permalink`, which enables the reverse jump back to ThousandEyes.

## What Those Headers Actually Mean

This part is easy to gloss over and it should not be. The trace correlation only works if the service understands the headers ThousandEyes injects and continues the trace correctly.

- `traceparent` and `tracestate` are the W3C Trace Context headers.
- `b3` is the Zipkin B3 single-header format.
- ThousandEyes injects both because real environments often contain a mix of proxies, meshes, gateways, and app runtimes that do not all prefer the same propagation format.

In OpenTelemetry terms, the important setting is the propagator list:

```text
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

That does two things:

1. It allows the service to extract either **B3** or **W3C** context from the inbound ThousandEyes request.
2. It preserves the W3C `tracestate` by keeping `tracecontext` enabled.

{{% notice title="Important Detail" style="warning" %}}
You do **not** add `tracestate` as a separate OpenTelemetry propagator. The `tracecontext` propagator handles both `traceparent` and `tracestate`.
{{% /notice %}}

## What "Properly Done" Looks Like

The collector is only one part of this setup. A correct ThousandEyes tracing deployment in Kubernetes has **three layers**:

1. **Deployment annotation** so the OpenTelemetry Operator injects the runtime-specific instrumentation.
2. **Instrumentation resource** so the injected SDK knows where to send traces and which propagators to use.
3. **Collector trace pipeline** so OTLP traces are actually received and exported to Splunk APM.

The most common mistake is to focus only on the collector. The collector never sees raw `b3`, `traceparent`, or `tracestate` request headers directly. Your application or auto-instrumentation library must extract those headers first, continue the span context, and then emit spans over OTLP to the collector.

## PetClinic Configuration Pattern

The examples below use the Spring PetClinic application included with this workshop. They show the Kubernetes annotation, `Instrumentation` resource, and pod-level settings that ThousandEyes needs for trace correlation.

### 1. Deployment Annotation

In this guide, the PetClinic Java deployments point at the `default/splunk-otel-collector` Instrumentation resource:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-java: default/splunk-otel-collector
```

This is the first place to verify when ThousandEyes requests are not turning into traces.

### 2. Instrumentation Resource

This is the PetClinic `Instrumentation` object, trimmed to the fields that matter for ThousandEyes:

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: splunk-otel-collector
spec:
  exporter:
    endpoint: http://splunk-otel-collector-agent.otel-splunk.svc:4317
  propagators:
    - baggage
    - b3
    - tracecontext
  sampler:
    type: parentbased_always_on
  env:
    - name: OTEL_RESOURCE_ATTRIBUTES
      value: deployment.environment=thousandeyes-petclinic
```

This is the critical part for the ThousandEyes scenario:

- `endpoint` sends spans to the cluster-local OTel agent service.
- `b3` allows extraction of ThousandEyes B3 headers.
- `tracecontext` preserves `traceparent` and `tracestate`.
- `parentbased_always_on` ensures the trace continues once ThousandEyes starts the request.

### 3. What The Injected Pod Actually Gets

On the running PetClinic `api-gateway` pod, validate that the operator injected the expected OpenTelemetry settings:

```bash
kubectl exec deploy/api-gateway -- printenv | \
  grep -E 'OTEL_EXPORTER_OTLP_ENDPOINT|OTEL_PROPAGATORS|OTEL_TRACES_SAMPLER|OTEL_RESOURCE_ATTRIBUTES'
```

You should see values like these:

```yaml
- name: OTEL_EXPORTER_OTLP_ENDPOINT
  value: http://splunk-otel-collector-agent.otel-splunk.svc:4317
- name: OTEL_PROPAGATORS
  value: baggage,b3,tracecontext
- name: OTEL_TRACES_SAMPLER
  value: parentbased_always_on
- name: OTEL_RESOURCE_ATTRIBUTES
  value: deployment.environment=thousandeyes-petclinic
```

This is a useful validation checkpoint because it proves the propagators are being applied to the workload, not just declared in an abstract config object.

### 4. Agent Collector Trace Pipeline

The live agent collector in `otel-splunk` is receiving OTLP, Jaeger, and Zipkin traffic and forwarding traces upstream. This is a trimmed excerpt from the running ConfigMap:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_http:
        endpoint: 0.0.0.0:14268
  zipkin:
    endpoint: 0.0.0.0:9411

service:
  pipelines:
    traces:
      receivers: [otlp, jaeger, zipkin]
      processors:
        [memory_limiter, k8sattributes, batch, resourcedetection, resource, resource/add_environment]
      exporters: [otlp, signalfx]
```

For ThousandEyes, the important part is not a special B3 option in the collector. The important part is simply that the collector exposes OTLP on `4317` and `4318`, and that your services are exporting their spans there.

{{% notice title="PetClinic Takeaway" style="info" %}}
The PetClinic `Instrumentation` resource is the pattern to follow for ThousandEyes because it explicitly includes `b3` together with `tracecontext`. That is the configuration you want for this scenario.
{{% /notice %}}

{{% notice title="Important" style="warning" %}}
Do **not** use a browser page URL for this section. ThousandEyes documents that browsers do not accept the custom trace headers required for this workflow. Use an instrumented backend endpoint behind an **HTTP Server** or **API** test instead.
{{% /notice %}}



