---
title: 5. Connect Mobile Sessions to APM
weight: 5
---

RUM answers what the user experienced. APM answers what the backend did. The strongest troubleshooting workflow links the two so a slow checkout screen can lead directly to a backend trace.

## Prepare the Backend

The backend services called by the app must be instrumented with Splunk APM or OpenTelemetry and must preserve W3C Trace Context headers through gateways and proxies.

{{% notice title="Exercise" style="green" icon="running" %}}

Confirm your backend has:

- APM traces flowing to Splunk Observability Cloud.
- Stable `service.name` and `deployment.environment` values.
- No proxy rule stripping `traceparent` or `tracestate`.
- CORS configuration that permits trace response headers where browser RUM is involved.

Generate a mobile request to a known endpoint such as `/checkout`, `/login`, or `/api/products`.

{{% /notice %}}

## Use Server Timing for Browser and WebView Correlation

Browser RUM and WebView traffic can use server timing headers to link front-end activity to backend traces. The backend or gateway should emit the response header expected by Splunk RUM after it has access to the active trace context.

```text
Server-Timing: traceparent;desc="00-<trace-id>-<span-id>-01"
Access-Control-Expose-Headers: Server-Timing
```

For mobile-native Flutter requests, validate the correlation behavior supported by the current Flutter/mobile RUM agent and your backend instrumentation. If automatic correlation is not available for a particular client library or platform path, keep shared attributes consistent and use backend request IDs as privacy-safe troubleshooting pivots.

{{% notice title="Exercise" style="green" icon="running" %}}

In Splunk Observability Cloud:

1. Open **RUM** and select the app you instrumented.
2. Filter to your `deployment.environment`.
3. Open a recent mobile or WebView session.
4. Find the slowest or failed network request.
5. Look for an **APM** or trace link from the RUM request details.
6. Open the backend trace and confirm it matches the mobile action you performed.

{{% /notice %}}

{{< tabs >}}
{{% tab title="Question" %}}
**What usually breaks RUM-to-APM correlation first?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Missing backend instrumentation, stripped trace headers, missing `Server-Timing` exposure for browser/WebView traffic, or mismatched environment filters.**
{{% /tab %}}
{{< /tabs >}}

## Correlation Tags to Standardize

Use a small set of attributes across RUM and APM:

| Attribute | Example | Notes |
| --------- | ------- | ----- |
| `deployment.environment` | `workshop` | Match RUM and APM filters. |
| `app.version` | `1.0.0` | Compare mobile releases. |
| `tenant.tier` | `gold` | Low-cardinality business context. |
| `workflow.name` | `checkout` | Useful for custom events and backend spans. |
| `request.id` | opaque UUID | Use only if generated safely and not tied to PII. |
