---
title: トラフィックの生成
linkTitle: 2. Generate Traffic
weight: 2
time: 15 minutes

---

このステップでは、Cosmic Observatory Shopにトラフィックを生成します。

## アプリケーションへのアクセス

ブラウザでCosmic Observatory Shopを開きます。

**<http://localhost:30080>**

望遠鏡、アイピース、天体写真機材などの天文機器カタログが表示されます。

![cosmic-shop](../images/cosmic-shop.png)

オプション - RabbitMQ管理UI

**<http://localhost:15672>** (ログイン: `guest` / `guest`)

![rabbitmq](../images/rabbitmq.png)

UIが読み込まれない場合は、ロードバランサーのポートを確認し、port-forwardを使用します。

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

## 初期トラフィックの生成

1. <http://localhost:30080> でショップを開きます
2. メールアドレスを入力します（例: `observer@cosmic.shop`）
3. 任意の商品の **Purchase** をクリックします
4. モーダルで注文を確認します

トレースデータを生成するために、これを数回繰り返します。
