---
title: NGINXのプロパゲーション修正
linkTitle: 06. NGINXのプロパゲーション修正
weight: 6
time: 15 minutes
description: このステップでは、エッジゲートウェイのNGINX設定を **編集** してW3C Trace Contextヘッダーを転送し、ゲートウェイを **再デプロイ** して変更を反映させます。これにより、注文パスにおけるSplunk RUMとバックエンドAPMトレース間の相関が復元されます。

---

{{% notice title="注意" style="info" %}}
このワークショップでは **2つの別々のNGINXインスタンス** を実行しています。このステップでは **エッジゲートウェイ** のみを変更します。

#### なぜエッジゲートウェイだけなのか？

これは注文トラフィックのパス（break #1が発生する箇所）だからです。

```
Browser
  → Frontend NGINX (port 30080, NodePort)
    → frontend-api (Node.js BFF)
      → Edge Gateway NGINX (ClusterIP service gateway:80)   ← ここに修正を適用します
        → order-api:3001
```

`/api/purchases`のトレースヘッダーは **frontend-api → gateway → order-api** を通過する必要があります。エッジゲートウェイが `order-api` へのプロキシホップで `traceparent`、`tracestate`、`baggage` を削除しています。
{{% /notice %}}

## 修正内容

各 `location` ブロックに3つのW3Cコンテキストヘッダーの明示的な転送を追加する必要があります。

```nginx
proxy_set_header traceparent $http_traceparent;
proxy_set_header tracestate $http_tracestate;
proxy_set_header baggage $http_baggage;
```

これらのディレクティブは、クライアント（Splunk RUM）からの受信トレースコンテキストを上流のサービスに渡すようNGINXに指示します。

## 修正の適用

```
vi deploy/k8s/gateway-config.yaml 
```

`default.conf` セクション（`data:` 配下のインデントされたNGINX設定）内の **`location /api/`** ブロックを見つけます。

標準の `proxy_set_header` 行の **後** 、`proxy_http_version` / `proxy_pass` の **前** に、3つのW3Cコンテキストヘッダーの明示的な転送を追加します。

```nginx
    # W3C Trace Context propagation
    proxy_set_header traceparent $http_traceparent;
    proxy_set_header tracestate $http_tracestate;
    proxy_set_header baggage $http_baggage;
```

{{% notice title="注意" style="green" icon="running" %}}
これらのディレクティブは、`frontend-api` からの受信トレースコンテキストを `order-api` に渡すようNGINXに指示します。
{{% /notice %}}

## 変更前と変更後

{{% notice title="注意" style="info" %}}
**エッジゲートウェイ** の **`location /api/`** ブロックのみが更新されます（フロントエンドNGINXではありません）。
{{% /notice %}}

{{< tabs >}}
{{% tab title="変更前" %}}

```nginx
        location /api/ {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_pass http://order_api;
        }
```

{{% /tab %}}
{{% tab title="変更後" %}}

```nginx
        location /api/ {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # W3C Trace Context propagation
            proxy_set_header traceparent $http_traceparent;
            proxy_set_header tracestate $http_tracestate;
            proxy_set_header baggage $http_baggage;

            proxy_http_version 1.1;
            proxy_pass http://order_api;
        }
```

{{% /tab %}}
{{< /tabs >}}
