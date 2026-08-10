---
title: 環境の設定
linkTitle: 02. 環境の設定
weight: 2
time: 5 minutes

---
このステップでは、Splunk Observability Cloudの認証情報とワークショップの設定を含む `.env` ファイルを作成します。

## 検証チェックリスト

環境には `SPLUNK_ACCESS_TOKEN`、`SPLUNK_REALM`、`SPLUNK_RUM_ACCESS_TOKEN` の値がすでに設定されているはずです。

プロジェクトルートから `env` コマンドを実行して確認します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
env
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
SPLUNK_REALM=<splunk-realm-value>
SPLUNK_ACCESS_TOKEN=<org-access-token-value>
SPLUNK_RUM_ACCESS_TOKEN=<rum-access-token-value>
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="[オプション] 演習" style="green" icon="running" %}}
**これらの値がインスタンスに存在しない場合は、以下の手順で設定できます** - プロジェクトルート [~/workshop/context-propagation] から実行してください:

```bash
cp .env.example .env
```

エディタで `.env` を開き、プレースホルダーの値を置き換えます:

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

{{% notice title="注意" style="info" %}}
インストラクターが必要なログイン認証情報と環境の詳細をすべて提供します。
{{% /notice %}}
