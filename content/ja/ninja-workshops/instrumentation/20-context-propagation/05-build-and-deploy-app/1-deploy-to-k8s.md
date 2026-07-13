---
title: K8sへのデプロイ
linkTitle: 1. K8sへのデプロイ
weight: 1
time: 10 minutes

---
このステップでは、Helmを使用してSplunk Distribution of the OpenTelemetry Collectorをk3dクラスターにデプロイします。

## Kubernetesへのデプロイ

```bash
make deploy
```

このスクリプトは以下を実行します。

1. `deploy/k8s/` からすべてのKubernetesマニフェストを適用する
2. `.env` の認証情報から `splunk-otel` Secretを作成する
3. デプロイメントをレジストリのイメージに向ける
4. すべてのロールアウトが完了するまで待機する

## 検証チェックリスト - デプロイ

#### 1. すべてのPodが実行中であることを確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAME                                  READY   STATUS    RESTARTS   AGE
catalog-api-xxxxxxxxxx-xxxxx          1/1     Running   0          2m
frontend-xxxxxxxxxx-xxxxx             1/1     Running   0          2m
gateway-xxxxxxxxxx-xxxxx              1/1     Running   0          2m
order-worker-xxxxxxxxxx-xxxxx         1/1     Running   0          2m
rabbitmq-xxxxxxxxxx-xxxxx             1/1     Running   0          2m
splunk-otel-collector-agent-xxxxx     1/1     Running   0          10m
storefront-api-xxxxxxxxxx-xxxxx       1/1     Running   0          2m
```

**失敗の指標:**

| STATUS | 考えられる原因 |
|--------|--------------|
| `ImagePullBackOff` | イメージがプッシュされていない - `make build` を再実行してください |
| `CrashLoopBackOff` | `kubectl -n cosmic-shop logs deployment/<name>` でログを確認してください |
| `Pending` | クラスターリソースが不足している - `kubectl describe pod <name>` で確認してください |

{{% /tab %}}
{{< /tabs >}}

#### 2. サービスとNodePortの確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop get svc
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)              AGE
catalog-api      ClusterIP   10.43.xxx.xxx   <none>        3002/TCP             2m
frontend         NodePort    10.43.xxx.xxx   <none>        80:30080/TCP         2m
gateway          ClusterIP   10.43.xxx.xxx   <none>        80/TCP               2m
order-worker     ClusterIP   10.43.xxx.xxx   <none>        3003/TCP             2m
rabbitmq         NodePort    10.43.xxx.xxx   <none>        5672:xxxxx/TCP,15672:15672/TCP   2m
storefront-api   ClusterIP   10.43.xxx.xxx   <none>        3001/TCP             2m
```

{{% /tab %}}
{{< /tabs >}}

#### 3. バックエンドのヘルスエンドポイントの確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl -n cosmic-shop exec deploy/frontend-api -- wget -qO- http://localhost:3007/health
kubectl -n cosmic-shop exec deploy/catalog-api -- wget -qO- http://localhost:3002/health
kubectl -n cosmic-shop exec deploy/order-api -- wget -qO- http://localhost:3001/health
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"status":"ok","service":"frontend-api","stage":"bff"}
{"status":"ok","service":"catalog-api"}
{"status":"ok","service":"order-api","stage":"order"}
```

{{% /tab %}}
{{< /tabs >}}

#### 4. ショップUIの応答確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:30080/
curl -s http://localhost:30080/ | head -5
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
HTTP 200
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
```

{{% /tab %}}
{{< /tabs >}}

#### 5. ゲートウェイ経由でAPIカタログエンドポイントの確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s http://localhost:30080/api/catalog | python3 -m json.tool | head -20
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
    "products": [
        {
            "id": "telescope-orion-8",
            "name": "Orion 8\" Dobsonian Telescope",
            "price": 449.99,
            ...
        }
    ]
}
```

{{% /tab %}}
{{< /tabs >}}

#### 6. RabbitMQ管理UIの確認

RabbitMQサービスは **NodePort 15672** を使用しており、k3dがロードバランサーを通じて管理UIを公開できるようにしています。

#### k3dロードバランサーがポート15672にマッピングされていることを確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
0.0.0.0:30080->30080/tcp, 0.0.0.0:15672->15672/tcp, ...
```

出力に **15672が含まれていない** 場合、クラスターがRabbitMQのポートマッピングなしで作成されています。下記の「RabbitMQ UIが読み込めない場合」を参照してください。

{{% /tab %}}
{{< /tabs >}}

#### HTTPの応答確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:15672/
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
HTTP 200
```

{{% /tab %}}
{{< /tabs >}}

#### RabbitMQへのログイン（オプション）

ブラウザで **<http://localhost:15672>** を開き、`guest` / `guest` でログインします。

**RabbitMQ UIが読み込めない場合**、 **別のターミナル** でport-forwardを使用します（開いたままにしてください）。

```bash
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

その後、再度 <http://localhost:15672> を開きます。
