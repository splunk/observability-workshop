---
title: Explore APM in Splunk
weight: 2
time: 5 minutes

---

## Check Splunk

#### 1. Confirm partial correlation in Service Map

1. Open **http://localhost:30080**
2. Generate 2-3 new requests
3. Navigate to **APM → Service Map**
4. Filter environment: `workshop-context-prop`

{{% notice title="Note" style="green" icon="running" %}}
You may see the service map with APM disjointed correlation between the payment-gateway and payment-api because:

1. The time-window selected is too broad
2. There may still be some health probe orphans
{{% /notice %}}

In this case, the service map will show:
1. Trace A: frontend-api -> payment-gateway:PORT  (stops at gateway)
2. Trace B: payment-gateway -> payment-api:PORT   (gateway starts its own root trace)

![gtway-aft](../images/s-disjointed.png)

#### 2. Confirm the purchase flow

In **APM → Traces** view, open a recent `frontend-api` trace. The trace should now show correlation whereby the payment-api appears in the trace waterfall view.

![gtway-aft](../images/t-gateway-aft.png)
