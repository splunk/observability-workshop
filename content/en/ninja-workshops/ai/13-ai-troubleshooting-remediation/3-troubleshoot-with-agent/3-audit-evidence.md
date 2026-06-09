---
title: 3. Audit the Evidence
weight: 3
---

The **Evidence** tab is where responders check whether the suspected root cause is supported by real telemetry. Evidence can include relevant logs, exemplar traces, APM services, and infrastructure signals.

{{% notice title="Exercise" style="green" icon="running" %}}

* Open the **Evidence** tab.
* Review each evidence type that is available for the alert.
* For each item, decide whether it strengthens, weakens, or does not affect the current hypothesis.

| Evidence type | What to inspect | How it helps |
|---------------|-----------------|--------------|
| Logs | Error messages, timestamps, service fields, Kubernetes metadata, deployment markers. | Confirms symptoms and sometimes exposes exact failure messages. |
| Exemplar traces | Slow or erroring trace waterfalls near the alert trigger time. | Shows where latency or errors entered the request path. |
| APM services | RED metrics, service dependencies, endpoint behavior, span tags. | Confirms whether the issue is isolated to one service or cascades through dependencies. |
| Kubernetes signals | Workload, pod, node, container, and resource metrics. | Confirms whether infrastructure health explains application symptoms. |

* Add one sentence to the incident brief for each strong evidence item:

```text
Evidence: <signal> supports <hypothesis> because <time-aligned observation>.
```

* Add one sentence for important negative evidence:

```text
Negative evidence: <signal> does not support <hypothesis> because <observation>.
```

{{< tabs >}}
{{% tab title="Question" %}}
**Why record negative evidence during an AI-assisted investigation?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Negative evidence prevents the team from over-fitting to the first plausible root cause and helps narrow the blast radius.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

## Evidence Quality Rubric

| Rating | Meaning |
|--------|---------|
| Strong | The evidence is time-aligned, component-specific, and directly explains the alert condition. |
| Medium | The evidence is related but needs another signal to establish causality. |
| Weak | The evidence is generic, stale, or too broad to guide action. |
| Contradictory | The evidence points away from the current hypothesis. |

