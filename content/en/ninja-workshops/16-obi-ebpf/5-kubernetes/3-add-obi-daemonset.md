---
title: 3. Enable OBI via Helm
weight: 3
---

Now add tracing to the entire cluster without changing any application code -- just one Helm upgrade.

## Upgrade the Collector with OBI Enabled

{{% notice title="Exercise" style="green" icon="running" %}}

``` bash
helm -n obi-workshop  upgrade splunk-otel-collector \
  splunk-otel-collector-chart/splunk-otel-collector \
  --set="splunkObservability.realm=${REALM}" \
  --set="splunkObservability.accessToken=${ACCESS_TOKEN}" \
  --set="clusterName=${INSTANCE}-k8s" \
  --set="environment=${INSTANCE}-ebpf" \
  --set="obi.enabled=true"
```

{{% /notice %}}

That single `--set="obi.enabled=true"` is the only change. The Helm chart handles everything else:

- Deploys the **OBI DaemonSet** (one pod per node)
- Configures RBAC (ServiceAccount, ClusterRole, ClusterRoleBinding)
- Points OBI at the collector automatically
- Grants the required Linux capabilities for eBPF

### What Does OBI Need?

The OBI pods run with elevated privileges because eBPF operates at the kernel level:

``` yaml
hostPID: true        # See all processes on the node, including other pods
hostNetwork: true    # Observe and inject trace context into network traffic
privileged: true     # Attach eBPF probes to the kernel
```

See the [OBI Security Documentation](https://opentelemetry.io/docs/zero-code/obi/security/) for details on reducing permissions if your cluster policies require it.

## Verify OBI is Running

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods  -n obi-workshop -l app.kubernetes.io/name=obi
kubectl logs  -n obi-workshop -l app.kubernetes.io/name=obi --tail=20
```

{{% /tab %}}
{{% tab title="Example Output to look for" %}}

``` text
NAME        READY   STATUS    RESTARTS   AGE
obi-abc12   1/1     Running   0          45s

...
level=INFO msg="instrumenting process" service=payment-service
...
level=INFO msg="instrumenting process" service=order-processor
...
level=INFO msg="instrumenting process" service=frontend
```

{{% /tab %}}
{{< /tabs >}}

Generate some traffic:

``` bash
curl -s http://localhost:30000/create-order | python3 -m json.tool
```

## Check Splunk APM

Wait 30-60 seconds for traces to flow.

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: You should now see three services: `frontend` -> `order-processor` -> `payment-service`.
2. **Traces**: Click into any trace. You'll see the full distributed trace spanning all three services with timing for each hop.
3. **Same story as Phase 2**: Zero code changes. One `helm upgrade` with a single flag.

{{% /notice %}}
