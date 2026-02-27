---
title: 3. Verify Traces in Splunk
weight: 3
---

## Quick Verification

First, confirm everything is healthy:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker compose ps
curl -s localhost:3000/create-order | python3 -m json.tool
docker compose logs obi | head -30
```

{{% /tab %}}
{{% tab title="Expected" %}}

``` text
# docker compose ps - all 6 containers running
# curl - returns JSON order confirmation
# obi logs - shows "instrumenting process" for each service
```

{{% /tab %}}
{{< /tabs >}}

In the OBI logs, look for lines like:

``` text
level=INFO msg="instrumenting process" cmd=/usr/local/bin/payment-service service=payment-service
level=INFO msg="instrumenting process" cmd=/usr/local/bin/order-processor service=order-processor
level=INFO msg="instrumenting process" cmd=node service=frontend
```

## Check Splunk APM

Wait 30-60 seconds for traces to flow, then check Splunk APM.

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: Navigate to APM and filter by your environment. You should now see three services: `frontend` -> `order-processor` -> `payment-service`.
2. **Traces**: Click into any trace. You'll see the full distributed trace spanning all three services with timing for each hop.
3. **Compare to Phase 1**: The APM dashboard that was completely empty a few minutes ago now shows a full service topology.

{{% /notice %}}

**You added ONE container to your compose file. You changed ZERO lines of application code. You now have full distributed tracing.**

## Answer Key

If you got stuck at any point, the complete final `docker-compose.yaml` with all changes applied is available at:

``` bash
cat ~/workshop/obi/02-obi-docker/docker-compose.final.yaml
```

Compare it against your `docker-compose.yaml` to spot any differences.

## Docker Cleanup

Before moving to the Kubernetes phase, bring down the Docker stack:

``` bash
docker compose down
```
