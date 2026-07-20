---
title: Splunk APMで確認する
weight: 2
time: 5 minutes

---

## Splunkで確認する

#### 1. Service Mapで部分的な相関を確認する

1. **<http://localhost:30080>** を開きます
2. 2〜3件の新しいリクエストを生成します
3. **APM → Service Map** に移動します
4. 環境をフィルタリングします: `workshop-context-prop`

{{% notice title="注意" style="green" icon="running" %}}
以下の理由により、payment-gatewayとpayment-api間のAPM相関が分断されたサービスマップが表示される場合があります。

1. 選択した時間範囲が広すぎる
2. ヘルスプローブによる孤立したSpanがまだ残っている
{{% /notice %}}

この場合、サービスマップは以下のように表示されます。

1. Trace A: frontend-api -> payment-gateway:PORT（gatewayで停止）
2. Trace B: payment-gateway -> payment-api:PORT（gatewayが独自のルートTraceを開始）

![gtway-aft](../images/s-disjointed.png)

#### 2. 購入フローを確認する

**APM → Traces** ビューで、最新の `frontend-api` Traceを開きます。Traceにはpayment-apiがTraceのウォーターフォールビューに表示される相関が確認できるはずです。

![gtway-aft](../images/t-gateway-aft.png)
