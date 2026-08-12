---
title: Explore APM in Splunk
weight: 2
time: 5 minutes

---

## Check Splunk

#### 1. Confirm partial correlation in Service Map

1. Navigate yo the app in the browser http://localhost:30080
2. Refresh the browser session using Command + Shift + R
3. Generate 2-3 new requests
4. Navigate to **APM → Service Map**
5. Filter environment: `workshop-$INSTANCE`

{{% notice title="Note" style="green" icon="running" %}}
You may see the service map with APM disjointed correlation between the payment-gateway and payment-api because:

1. The time-window selected is too broad
2. There may still be some health probe orphans
{{% /notice %}}

In this case, the service map will show:
1. Trace A: frontend-api -> payment-gateway:PORT  (stops at gateway)
2. Trace B: payment-gateway -> payment-api:PORT   (gateway starts its own root trace)

![gtway-dsj](../images/s1-disjointed.png)

#### 2. Confirm the purchase flow

In **APM → Traces** view, open a recent `frontend-api` trace. The trace should now show correlation whereby the payment-api appears in the trace waterfall view.

![gtway-aft](../images/t-gateway-aft.png)
