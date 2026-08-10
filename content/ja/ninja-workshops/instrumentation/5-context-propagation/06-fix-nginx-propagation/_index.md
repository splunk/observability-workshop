---
title: NGINXのプロパゲーション修正
linkTitle: 06. NGINXのプロパゲーション修正
weight: 6
time: 15 minutes
description: このステップでは、エッジゲートウェイのNGINX設定を **編集** してW3C Trace Contextヘッダーを転送し、ゲートウェイを **再デプロイ** して変更を反映させます。これにより、Splunk RUMとバックエンドAPM Traceの間のorderパスにおける相関が復元されます。

---

{{% notice title="注意" style="info" %}}
このワークショップでは **2つの別々のNGINXインスタンス** を実行しています。このステップで変更するのは **エッジゲートウェイ** のみです。

#### なぜエッジゲートウェイだけなのか？

これはOrderトラフィックパス（break #1が発生する箇所）であるためです

```
Browser
  → Frontend NGINX (port 30080, NodePort)
    → frontend-api (Node.js BFF)
      → Edge Gateway NGINX (ClusterIP service gateway:80)   ← ここに修正を適用します
        → order-api:3001
```

`/api/purchases`のTraceヘッダーは **frontend-api → gateway → order-api** を通過する必要があります。エッジゲートウェイが `order-api` へのプロキシホップで `traceparent`、`tracestate`、`baggage` をドロップしています。
{{% /notice %}}

## 修正の適用

各 `location` ブロックに3つのW3Cコンテキストヘッダーの明示的な転送を追加する必要があります。

これらのディレクティブは、クライアント（Splunk RUM）からの受信Traceコンテキストをアップストリームサービスに渡すようNGINXに指示します。

{{% notice title="注意" style="info" %}}
注意: vi以外のエディタも使用できます
{{% /notice %}}

プロジェクトルート [~/workshop/context-propagation] から、gateway-configファイルを開いて編集します

```
vi deploy/k8s/gateway-config.yaml 
```

`default.conf` セクション内（`data:` の下のインデントされたNGINX設定）の **`location /api/`** ブロックを見つけ、標準の `proxy_set_header` 行の **後** 、`proxy_http_version` / `proxy_pass` の **前** に3つのW3Cコンテキストヘッダーの明示的な転送を追加します

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

{{% notice title="続行する前に作業を確認してください" style="primary" icon="running" %}}
./workshop/context-propagationフォルダから以下のコマンドを実行して、変更内容を期待される解決策と比較します

```bash
diff ./deploy/k8s/gateway-config.yaml  ./deploy/k8s/gateway-config-fixed.yaml
```

{{% / notice %}}

{{% notice title="注意" style="green" icon="running" %}}
これらのディレクティブは、`frontend-api` からの受信Traceコンテキストを `order-api` に渡すようNGINXに指示します。
{{% /notice %}}
