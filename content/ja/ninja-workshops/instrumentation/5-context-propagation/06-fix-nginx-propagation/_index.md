---
title: NGINXプロパゲーションの修正
linkTitle: 06. NGINXプロパゲーションの修正
weight: 6
time: 15 minutes
description: このステップでは、エッジゲートウェイのNGINX設定を **編集** してW3C Trace Contextヘッダーを転送し、ゲートウェイを **再デプロイ** して変更を反映させます。これにより、Splunk RUMとバックエンドのAPMトレース間の相関が注文パスで復元されます。

---

{{% notice title="注意" style="info" %}}
このワークショップでは **2つの別々のNGINXインスタンス** を実行しています。このステップでは **エッジゲートウェイ** のみを変更します。

#### なぜエッジゲートウェイだけなのか？

これは注文トラフィックのパス（break #1が発生する箇所）だからです

```
Browser
  → Frontend NGINX (port 30080, NodePort)
    → frontend-api (Node.js BFF)
      → Edge Gateway NGINX (ClusterIP service gateway:80)   ← We are applying the fixes here
        → order-api:3001
```

`/api/purchases` のトレースヘッダーは **frontend-api → gateway → order-api** を通じて維持される必要があります。エッジゲートウェイは `order-api` へのプロキシホップで `traceparent`、`tracestate`、`baggage` を落としています。
{{% /notice %}}

## 修正内容

各 `location` ブロックにW3Cコンテキストヘッダー3つの明示的な転送を追加する必要があります

これらのディレクティブは、クライアント（Splunk RUM）からの受信トレースコンテキストをアップストリームサービスに渡すようNGINXに指示します。

## 修正の適用

```
vi deploy/k8s/gateway-config.yaml 
```

`default.conf` セクション（`data:` の下にインデントされたNGINX設定）内の **`location /api/`** ブロックを見つけ、標準の `proxy_set_header` 行の **後** かつ `proxy_http_version` / `proxy_pass` の **前** にW3Cコンテキストヘッダー3つの明示的な転送を追加します

```nginx
proxy_set_header traceparent $http_traceparent;
proxy_set_header tracestate $http_tracestate;
proxy_set_header baggage $http_baggage;
```

{{% notice title="注意" style="info" %}}
**エッジゲートウェイ** の **`location /api/`** ブロックのみを更新します（フロントエンドNGINXではありません）。
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

{{% notice title="注意" style="green" icon="running" %}}
これらのディレクティブは、`frontend-api` からの受信トレースコンテキストを `order-api` に渡すようNGINXに指示します。
{{% /notice %}}
