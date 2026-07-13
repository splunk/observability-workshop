---
title: Splunkで確認する
weight: 2
time: 5 minutes

---

## Splunkを確認する

#### 1. RUMで部分的な相関を確認する

RUMセッションにAPMの相関が表示されます。

![nginx-aft](../images/r-nginx-aft.png)

#### 2. Traceで部分的な相関を確認する

**APM → Traces** ビューで、最新の `frontend-api` Traceを開きます。この修正により、フロントエンドのSpanがブラウザ/RUMセッションとTrace IDを共有するようになります。

![nginx-aft](../images/t-nginx-aft.png)
