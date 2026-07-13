---
title: NGINX修正後の再デプロイ
weight: 1
time: 5 minutes

---

## 保存後の再デプロイ

ファイルを保存しただけでは、実行中のgatewayは更新 **されません** 。ConfigMapを適用し、deploymentを再起動して、NGINXに新しい設定を読み込ませる必要があります。

プロジェクトルートから以下を実行します。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl apply -f deploy/k8s/gateway-config.yaml
kubectl -n cosmic-shop rollout restart deployment/gateway
kubectl -n cosmic-shop rollout status deployment/gateway --timeout=180s
```

Podが変更を反映したことを確認します。

```bash
kubectl -n cosmic-shop exec deploy/gateway -- grep traceparent /etc/nginx/conf.d/default.conf
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
proxy_set_header traceparent $http_traceparent;
```

{{% /tab %}}
{{< /tabs >}}

## 検証チェックリスト

再デプロイ完了後に以下のコマンドを実行します。

#### 1. gateway Podが再起動したことを確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop rollout status deployment/gateway
kubectl -n cosmic-shop get pods -l app=gateway
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
deployment "gateway" successfully rolled out

NAME                       READY   STATUS    RESTARTS   AGE
gateway-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
```

AGEが最近の値であることを確認します（設定変更後にPodが再作成されたことを示します）。

{{% /tab %}}
{{< /tabs >}}

#### 2. ConfigMapにトレースヘッダーが含まれていることを確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop get configmap gateway-nginx-config -o yaml | grep traceparent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
  proxy_set_header traceparent $http_traceparent;
```

出力に `traceparent`、`tracestate`、`baggage` が表示されます。

{{% /tab %}}
{{< /tabs >}}

#### 3. traceparentがorder-apiに到達することを確認

既知のトレースヘッダーを付けて **エッジgateway経由で** リクエストを送信します。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop port-forward svc/gateway 8888:80 &
sleep 2

TRACE_ID="deadbeefdeadbeefdeadbeefdeadbeef"
curl -s -H "traceparent: 00-${TRACE_ID}-deadc0dedeadbeef-01" \
  -X POST http://localhost:8888/api/orders \
  -H "Content-Type: application/json" \
  -d '{"productId":"eyepiece-plossl-set","quantity":1,"customerEmail":"trace-test@cosmic.shop"}' \
  | python3 -m json.tool

kill %1 2>/dev/null
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
    "message": "Order created",
    "order": { "orderId": "ORD-...", ... },
    "traceHint": {
        "traceId": "deadbeefdeadbeefdeadbeefdeadbeef",
        ...
    }
}
```

`traceHint.traceId` が `traceparent` ヘッダーで送信したトレースIDと一致することを確認します。これにより、gatewayが `order-api` にヘッダーを転送したことが確認できます。

{{% /tab %}}
{{< /tabs >}}

### $ 4. 新しいブラウザトラフィックを生成

**新しいシークレットウィンドウ** またはハードリフレッシュ（Cmd+Shift+R）を使用して、ショップで2〜3件の新しい注文を行います。

## トラブルシューティング

このステップで発生する可能性のある問題と、推奨される対処方法を以下に示します。

{{< details summary="トラブルシューティングガイダンスはこちら" >}}

#### 問題1: 修正後もトレースが切断されたまま

- `deploy/k8s/gateway-config.yaml` を **保存** し、 **`make fix-nginx`** （または手動の `kubectl apply` + restartコマンド）を実行したことを確認します
- gateway Podが再起動したことを確認します: `kubectl -n cosmic-shop get pods -l app=gateway`
- ConfigMapを確認します: `kubectl -n cosmic-shop get configmap gateway-nginx-config -o yaml | grep traceparent`
- Pod内部を確認します: `kubectl -n cosmic-shop exec deploy/gateway -- cat /etc/nginx/conf.d/default.conf`
- **新しい** トラフィックを生成します。古いトレースは遡って変更されません

#### 問題2: ConfigMapは更新されたがPodに古い設定が残っている

NGINXは既存のPod上でConfigMapボリュームの変更をホットリロードしません。YAMLを編集した後は必ず **`rollout restart deployment/gateway`** を実行してください。

#### 問題3: CORSプリフライトがヘッダーを除去している

NGINXにCORSを追加する場合、`Access-Control-Allow-Headers` に `traceparent` と `tracestate` を含めてください。

```nginx
add_header Access-Control-Allow-Headers 'Content-Type, traceparent, tracestate, baggage';
```

{{< /details >}}
