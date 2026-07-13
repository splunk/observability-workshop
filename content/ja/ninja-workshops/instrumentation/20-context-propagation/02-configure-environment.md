---
title: 環境の設定
linkTitle: 02. 環境の設定
weight: 2
time: 5 minutes

---
このステップでは、Splunk Observability Cloudの認証情報とワークショップの設定を含む `.env` ファイルを作成します。

{{% notice title="検証チェックリスト" style="green" icon="running" %}}
環境には `SPLUNK_ACCESS_TOKEN`、`SPLUNK_REALM`、`SPLUNK_RUM_ACCESS_TOKEN` の値がすでに設定されている必要があります。

プロジェクトルートから以下のコマンドを実行して `.env` を確認します。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
grep -E '^SPLUNK_(REALM|ACCESS_TOKEN|RUM_ACCESS_TOKEN)=' .env | cut -d= -f1
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
SPLUNK_REALM
SPLUNK_ACCESS_TOKEN
SPLUNK_RUM_ACCESS_TOKEN
```

{{% /tab %}}
{{< /tabs >}}

**存在しない場合は、以下の手順で設定します**

```bash
cp .env.example .env
```

エディタで `.env` を開き、プレースホルダーの値を置き換えます。

```bash
# Splunk Observability Cloud
SPLUNK_REALM=<splunk-realm>
SPLUNK_ACCESS_TOKEN=<your-org-access-token>

# RUM browser agent
SPLUNK_RUM_ACCESS_TOKEN=<your-rum-access-token>
SPLUNK_RUM_APP_NAME=cosmic-observatory-shop
SPLUNK_DEPLOYMENT_ENV=workshop-context-prop

# Kubernetes
K3D_CLUSTER_NAME=cosmic-shop
CLUSTER_NAME=cosmic-shop-cluster
REGISTRY=localhost:5111
TAG=latest
```

{{% /notice %}}
