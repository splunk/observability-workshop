---
title: Observe in Splunk
weight: 2
time: 5 minutes

---

## Check Splunk

#### 1. Confirm partial correlation in Service Map

You will now see the service map with APM correlation between the payment-gateway and payment-api 

![gtway-aft](../images/s-gateway-aft.png)

#### 2. Confirm partial correlation in Traces

In **APM → Traces** view, open a recent `order-api` trace. The order span should now show correlation between the order-api and .

![gtway-aft](../images/t-gateway-aft.png)
