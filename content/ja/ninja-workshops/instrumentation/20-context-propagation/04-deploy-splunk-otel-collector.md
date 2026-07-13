---
title: OTel Collectorのインストール
linkTitle: 04. OTel Collectorのインストール
weight: 4
time: 15 minutes 

---

このステップでは、Helmを使用してk3dクラスターにSplunk Distribution of the OpenTelemetry Collectorをデプロイします。Collectorは計装されたサービスからトレースとメトリクスを受信し、Splunk Observability Cloudに転送します。

{{% notice title="注意" style="info" %}}

各アプリケーションPodはノードIPを経由してCollectorにデータを送信します。

```text
Pod → http://$(NODE_IP):4318 → Splunk OTel Collector DaemonSet → Splunk O11y Cloud
```

{{% /notice %}}

## Helmによるインストール

`.env` ファイルが設定されていることを確認し、以下を実行します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
make collector
```

{{% /tab %}}
{{% tab title="手動" %}}

```bash
source .env

helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update

helm upgrade --install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --namespace cosmic-shop \
  --create-namespace \
  -f deploy/helm/splunk-otel-values.yaml \
  --set="splunkObservability.realm=${SPLUNK_REALM}" \
  --set="splunkObservability.accessToken=${SPLUNK_ACCESS_TOKEN}" \
  --set="clusterName=${CLUSTER_NAME}" \
  --set="environment=${SPLUNK_DEPLOYMENT_ENV}"
```

{{% /tab %}}
{{< /tabs >}}

## 検証チェックリスト

`make collector` が完了したら、以下のコマンドを実行します。

#### 1. Helmリリースがインストールされていることを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
helm list -n cosmic-shop
```

{{% /tab %}}
{{% tab title="出力例" %}}

```
NAME                    NAMESPACE   REVISION   STATUS     CHART                         APP VERSION
splunk-otel-collector   cosmic-shop 1          deployed   splunk-otel-collector-0.x.x   0.x.x
```

STATUSが `deployed` であることを確認します。`failed` と表示される場合は、`.env` の `SPLUNK_REALM` と `SPLUNK_ACCESS_TOKEN` を再確認してください。

{{% /tab %}}
{{< /tabs >}}

#### 2. Collector Podが稼働していることを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
kubectl -n cosmic-shop get pods -l 'app=splunk-otel-collector,component=otel-collector-agent'
```

{{% /tab %}}
{{% tab title="出力例" %}}

```
NAME                            DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
splunk-otel-collector-agent     1         1         1       1            1           <none>          2m

NAME                                  READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-xxxxx     1/1     Running   0          60s
```

READYが `1/1`、STATUSが `Running` であることを確認します。STATUSが `CrashLoopBackOff` の場合は、ステップ3でログを確認してください。

{{% /tab %}}
{{< /tabs >}}

#### 3. Collectorログに認証エラーがないことを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
kubectl -n cosmic-shop logs -l 'app=splunk-otel-collector,component=otel-collector-agent' --tail=30
```

{{% /tab %}}
{{% tab title="出力例" %}}

```
... Everything is ready. Begin running and processing data.
```

**注意すべきエラーの兆候:**

```
401 Unauthorized
access token is invalid
failed to export
connection refused
```

認証エラーが表示される場合は、`.env` のアクセストークンとrealmを確認し、再インストールします。

```bash
make collector
```

{{% /tab %}}
{{< /tabs >}}

## Splunk Observability Cloudでクラスターを確認

1. Splunk Observability Cloudを開きます
2. **Infrastructure → Kubernetes → Kubernetes Entities → Clusters** に移動します
3. クラスター名（`cosmic-shop-cluster` または `.env` の `CLUSTER_NAME` の値）を検索します

Collectorの起動から数分以内にクラスターが表示されます。

## トラブルシューティング

このステップで発生する可能性のある問題と推奨される対処方法を以下に示します。

{{< details summary="トラブルシューティングガイドを表示するにはここをクリック" >}}

#### 問題1. Helmインストールが認証エラーで失敗する

`.env` の `SPLUNK_ACCESS_TOKEN` と `SPLUNK_REALM` が正しいこと、およびトークンにingest権限があることを確認してください。

#### 問題2. Infrastructureナビゲーターにクラスターが表示されない

2〜3分待ちます。Collector Podが稼働していることを確認し、ログにエクスポートエラーがないか確認してください。

{{< /details >}}
