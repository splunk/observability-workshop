---
title: アプリケーションのビルドとデプロイ
linkTitle: 05. アプリケーションのビルドとデプロイ
weight: 5
time: 10 minutes

---
このステップでは、Cosmic Observatory Shopの全サービスのDockerイメージをビルドし、k3dローカルレジストリにプッシュして、Kubernetesにフルスタックをデプロイします。

## コンテナイメージのビルド

プロジェクトルートで `.env` が設定済みであることを確認してください

```bash
make build
```

これにより4つのイメージがビルドされ、`localhost:5111` にプッシュされます

| イメージ | サービス |
|-------|---------|
| `cosmic-shop/frontend` | Splunk RUMを使用したReactショップUI |
| `cosmic-shop/storefront-api` | Splunk APMを使用した注文API |
| `cosmic-shop/catalog-api` | Splunk APMを使用した商品カタログ |
| `cosmic-shop/order-worker` | Splunk APMを使用したRabbitMQコンシューマー |

## 検証チェックリスト - ビルド

#### 1. 4つのイメージすべてがプッシュされたことを確認する

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
curl -s http://localhost:5111/v2/_catalog | python3 -m json.tool
```

{{% /tab %}}
{{% tab title="出力例" %}}

```json
{
    "repositories": [
        "cosmic-shop/catalog-api",
        "cosmic-shop/frontend",
        "cosmic-shop/order-worker",
        "cosmic-shop/storefront-api"
    ]
}
```

{{% /tab %}}
{{< /tabs >}}

#### 2. 関連するすべてのイメージが存在することを確認する

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
docker images | grep cosmic-shop
```

{{% /tab %}}
{{% tab title="出力例" %}}

```
localhost:5111/cosmic-shop/frontend          latest    abc123def456   2 minutes ago   45MB
localhost:5111/cosmic-shop/storefront-api    latest    def456abc789   2 minutes ago   180MB
localhost:5111/cosmic-shop/catalog-api       latest    ...
localhost:5111/cosmic-shop/order-worker      latest    ...
```

{{% /tab %}}
{{< /tabs >}}
