---
title: 1. スタックの設定と起動
weight: 1
---

## Splunk 認証情報の確認または追加

{{% exercise title="設定と起動" %}}

``` bash
echo $ACCESS_TOKEN; echo $REALM; echo $INSTANCE
```

値が設定されていない場合は、リポジトリのルートに `.env` を作成または編集してください

**注意:** Splunk Observability Cloud からアクセストークンを取得してください: **Settings → Access Tokens**（APM 権限付きの Ingest トークン）。設定ファイルに貼り付ける必要があります。

```bash
cp .env.example .env
```

```bash
SPLUNK_ACCESS_TOKEN=<INGEST_TOKEN>
SPLUNK_REALM=<YOUR-REALM>
WORKSHOP_ENV=trace-propagation-<YOUR-INITIALS>
```

### コレクターのデプロイ

このスクリプトは以下を実行します

1. `.env` から `splunk-credentials` Kubernetes Secret を作成します
2. `k8s/splunk-otel-collector/`（gateway Deployment、agent DaemonSet、RBAC、ConfigMaps）を適用します
3. gateway とインフラストラクチャ agent が準備完了になるまで待機します
4. `http://localhost:13133/` でコレクターのヘルスチェックを検証します

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
```bash
cd ~/workshop/context-propagation/scripts
./2-deploy-collector.sh
```

{{% /tab %}}
{{% tab title="Example Output (abbreviated)" %}}

``` text
Creating Splunk credentials secret...
Deploying Splunk OpenTelemetry Collector...
Waiting for splunk-otel-collector gateway...
Waiting for splunk-otel-collector-agent (infrastructure metrics)...
Splunk OTel Collector image: quay.io/signalfx/splunk-otel-collector:0.108.0
Validating collector health...
{"status":"Server available","upSince":"...","uptime":"..."}
Step 2 complete — Splunk OTel Collector is running.
Infrastructure metrics: host + kubelet (DaemonSet) + k8s_cluster (gateway) → Splunk IMM
Splunk IMM cluster:     trace-workshop ...

Validating collector health...
```

{{% /tab %}}
{{< /tabs >}}

このワークショップでは2つのコレクターワークロードをデプロイします

| ワークロード | 役割 |
| -------- | ---- |
| `deployment/splunk-otel-collector` | OTLP gateway + **k8s_cluster** receiver（クラスターインフラストラクチャメトリクス） |
| `daemonset/splunk-otel-collector-agent` | **hostmetrics** + **kubeletstats**（ノード、Pod、コンテナメトリクス） |

- **Image:** `quay.io/signalfx/splunk-otel-collector:0.108.0`
- **Gateway config:** `k8s/splunk-otel-collector/workshop-config.yaml`
- **Agent config:** `k8s/splunk-otel-collector/agent-config.yaml`

### コレクターのヘルスチェック確認

```bash
curl -s http://localhost:13133/
```

### コレクターログの確認

コレクターがパイプラインエラーなしで起動していることを確認します（`401`、`403`、またはエクスポート失敗が繰り返されていないこと）。

```bash
kubectl logs deployment/splunk-otel-collector -n trace-workshop --tail 20
kubectl logs daemonset/splunk-otel-collector-agent -n trace-workshop --tail 20
```

{{%/ exercise %}}
