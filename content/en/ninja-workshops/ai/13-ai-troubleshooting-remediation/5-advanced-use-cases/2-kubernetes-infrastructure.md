---
title: 2. Kubernetes Infrastructure Alert
weight: 2
---

Kubernetes incidents often look like application problems until you inspect workload, pod, node, and resource evidence. The AI troubleshooting agent can help responders connect application symptoms to infrastructure signals when the alert comes from supported Kubernetes metrics.

{{% notice title="Exercise" style="green" icon="running" %}}

Use a Kubernetes alert from Infrastructure Monitoring.

* On **Overview**, identify the affected cluster, namespace, workload, pod, node, or container.
* On **Root Cause Analysis**, look for hypotheses such as:
  * Pod restart loop or crash behavior.
  * CPU, memory, or disk pressure.
  * Node-level resource saturation.
  * Failed scheduling or unavailable replicas.
  * Network or dependency symptoms that appear after infrastructure stress begins.
* On **Evidence**, separate service impact from infrastructure cause:

| Signal | What to check |
|--------|---------------|
| Workload health | Desired vs available replicas, rollout status, restart counts. |
| Pod health | Container state, last termination reason, readiness and liveness failures. |
| Node health | Pressure conditions, allocatable resources, noisy neighbors. |
| Application traces | Whether latency begins after infrastructure saturation. |
| Logs | OOM, crash, connection, or readiness probe errors. |

* If the action plan suggests `kubectl` steps, run read-only commands first.

```bash
kubectl get deploy,statefulset,daemonset -n <namespace>
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

* Submit command output to the plan when requested.
* Execute state-changing commands only in a lab or with production approval.

{{< tabs >}}
{{% tab title="Question" %}}
**What is the difference between a Kubernetes symptom and a Kubernetes root cause?**
{{% /tab %}}
{{% tab title="Answer" %}}
**A symptom is what became unhealthy, such as unavailable pods. A root cause explains why, such as memory pressure, a bad image, a failed probe, or a node resource issue.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

