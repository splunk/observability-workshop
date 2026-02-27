---
title: 3. Add the OBI DaemonSet
weight: 3
---

Now add tracing to the entire cluster without changing any application code.

## Apply the OBI DaemonSet

{{% notice title="Exercise" style="green" icon="running" %}}

``` bash
kubectl apply -f ~/workshop/obi/03-obi-k8s/obi-daemonset.yaml
```

{{% /notice %}}

This creates:

1. A **ConfigMap** with the OBI service discovery config (same concept as `obi-config.yaml` from Phase 2)
2. A **ServiceAccount**, **ClusterRole**, and **ClusterRoleBinding** for OBI's RBAC permissions
3. A **DaemonSet** that runs one OBI pod on every node in your cluster

### What Does the DaemonSet Do?

The DaemonSet spec includes three critical settings:

``` yaml
hostPID: true        # See all processes on the node, including other pods
hostNetwork: true    # Observe and inject trace context into network traffic
privileged: true     # Attach eBPF probes to the kernel
```

OBI discovers your services by port (3000, 8080, 8081), instruments them via eBPF, generates traces, and sends them to the collector at `splunk-otel-collector.obi-workshop:4318`.

## Verify OBI is Running

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n obi-workshop -l app=obi
kubectl logs -n obi-workshop -l app=obi --tail=20
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME        READY   STATUS    RESTARTS   AGE
obi-abc12   1/1     Running   0          45s

level=INFO msg="instrumenting process" service=payment-service
level=INFO msg="instrumenting process" service=order-processor
level=INFO msg="instrumenting process" service=frontend
```

{{% /tab %}}
{{< /tabs >}}

## Check Splunk APM

Wait 30-60 seconds for traces to flow.

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: You should now see three services: `frontend` -> `order-processor` -> `payment-service`.
2. **Traces**: Click into any trace. You'll see the full distributed trace spanning all three services with timing for each hop.
3. **Same story as Phase 2**: Zero code changes, one DaemonSet addition.

{{% /notice %}}
