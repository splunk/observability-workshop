---
title: Splunkで確認する
weight: 2
time: 5 minutes

---

## Splunkを確認する

#### 1. Service Mapで部分的な相関を確認する

payment-gatewayとpayment-api間のAPM相関がService Mapに表示されます。

![gtway-aft](../images/s-gateway-aft.png)

#### 2. Tracesで部分的な相関を確認する

**APM → Traces** ビューで、最近の `order-api` トレースを開きます。orderのSpanにorder-apiとの相関が表示されます。

![gtway-aft](../images/t-gateway-aft.png)
