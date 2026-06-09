---
title: 4. Add Custom Tokenomics Instrumentation
weight: 4
---

The built-in instrumentation tells you what happened inside an AI request. The custom
instrumentation in this section tells you who should own the cost.

## Review the Companion Example

The workshop includes a small Python helper:

```text
workshop/ai-tokenomics-chargeback/instrumentation/tokenomics_instrumentation.py
```

It demonstrates how to:

* Normalize owner dimensions.
* Record input, output, and total token counters.
* Record a request count.
* Estimate request cost from a rate card.
* Attach the same dimensions and token counts to the active span.

{{% notice title="Exercise" style="green" icon="running" %}}

Review the instrumentation helper:

1. Open `workshop/ai-tokenomics-chargeback/instrumentation/tokenomics_instrumentation.py`.
2. Find `REQUIRED_DIMENSIONS`.
3. Confirm that every required dimension has a default value.
4. Find `record_llm_chargeback`.
5. Confirm that token counts are recorded as counters and span attributes.
6. Find `estimate_request_cost_usd`.
7. Replace the workshop rates with your instructor-provided rate card if needed.

{{% /notice %}}

## Add Request Dimensions

Applications usually know the request owner before they call the LLM. In a Flask app,
that might come from headers:

```python
dimensions = dimensions_from_headers(
    request.headers,
    defaults={
        "ai.team": os.getenv("AI_TEAM_DEFAULT", "unknown"),
        "ai.cost_center": os.getenv("AI_COST_CENTER_DEFAULT", "unknown"),
        "ai.workload.name": os.getenv("AI_WORKLOAD_NAME", "llm-app"),
        "ai.product_area": os.getenv("AI_PRODUCT_AREA", "unknown"),
        "deployment.environment": os.getenv("DEPLOYMENT_ENVIRONMENT", "workshop"),
    },
)
```

After the LLM call returns, record the usage:

```python
record_llm_chargeback(
    prompt_tokens=usage.prompt_tokens,
    completion_tokens=usage.completion_tokens,
    model="meta/llama-3.2-1b-instruct",
    dimensions=dimensions,
)
```

## Kubernetes Defaults

Use Kubernetes metadata for defaults that do not change per request. The companion patch
shows one way to add deployment-level defaults:

```text
workshop/ai-tokenomics-chargeback/k8s/llm-app-chargeback-patch.yaml
```

{{% notice title="Exercise" style="green" icon="running" %}}

Patch the sample application metadata in a lab namespace:

```bash
kubectl -n "$USER_NAME" patch deployment llm-app --patch-file \
  workshop/ai-tokenomics-chargeback/k8s/llm-app-chargeback-patch.yaml
```

Then generate a few requests with different headers:

```bash
curl -X POST "http://$LLM_APP_URL/askquestion" \
  -H "content-type: application/json" \
  -H "x-ai-tenant-id: tenant-enterprise" \
  -H "x-ai-team: support-ai" \
  -H "x-ai-cost-center: cc-ml-1200" \
  -d '{"question":"How much memory does the NVIDIA H200 have?"}'
```

{{% /notice %}}

{{< tabs >}}
{{% tab title="Question" %}}
**Where should prompt text be stored for chargeback?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It should not be a metric dimension. If policy allows prompt capture, keep it in
trace events or logs with redaction and retention controls.**
{{% /tab %}}
{{< /tabs >}}
