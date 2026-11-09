---
title: 6. Wrap-up
weight: 6
draft: true
---

{{< presenter >}}
Turn remaining `S-*` flags **off** on `/Feature`, including **S-Resource-management**. Wait until dummy pods (`email-oom`, and any leftover `cart-imagepull` / `paymentservice` / `storefront-spread`) disappear. Leave **S-TEST-shelltester** off.
{{< /presenter >}}

{{% notice style="blue" title="Congratulations" icon="wine-bottle" %}}

You used **Splunk Infrastructure Monitoring** — and APM — to investigate four Kubernetes issues in the Astronomy Shop, from a noisy neighbour through to an OOM restart cycle.

{{% /notice %}}

## What we accomplished

1. **Filtered to your cluster** in the Kubernetes new experience
2. **Found a noisy neighbour** (`otel-collector-noisy`) and the scheduling blast radius on `storefront-spread`
3. **Inventoried degraded deployments** from Kubernetes Overview (`paymentservice` not at desired count)
4. **Explained ImagePullBackOff** from status reason, events, and a typo in YAML (`lastest`)
5. **Correlated APM to Kubernetes** for the `email-oom` sawtooth and OOMKills

## Investigation map

| Scenario | Where you started | What you proved |
|----------|-------------------|-----------------|
| Noisy neighbour | Kubernetes Nodes | Memory outlier pod + required anti-affinity leaving replicas Pending |
| Degraded deployments | Kubernetes Overview | Inventory of deployments below desired count, same YAML affinity root cause |
| Image pull | Pods sorted by Status | `ImagePullBackOff` from image tag `lastest` |
| APM to Kubernetes | APM → email → Instances | Sawtooth to a 100Mi limit, probe failures, OOMKill |

{{% notice title="Info" style="info" %}}
In this module, Kubernetes was the **primary** investigation surface, with APM as the entry point for the last scenario. Related Content still connects traces, infrastructure, metrics, and logs. The right starting point depends on the signal you have when the incident starts.
{{% /notice %}}

{{< pager prev="/en/splunk4rookies/o11y-rookies-26/modules/" prevLabel="Back to Lessons" >}}
