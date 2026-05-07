---
title: 1. OTel Collector のインストール
weight: 1
---

デュアルモードの AppDynamics エージェントは OTLP 経由で OpenTelemetry データを送信します。そのデータを受信して Splunk Observability Cloud に転送するために、同じホスト上に Collector が必要です。

## 環境変数の確認

インスタンスにはこれらの変数が事前に設定されているはずです。`env` または以下のコマンドで利用可能であることを確認してください

```bash
echo "REALM=$REALM"
echo "ACCESS_TOKEN=$ACCESS_TOKEN"
echo "INSTANCE=$INSTANCE"
```

3つすべてに値が設定されている必要があります。空のものがある場合は、インストラクターに確認してください。

## Splunk OpenTelemetry Collector のインストール

Splunk OTel Collector のインストールスクリプトを実行します。これにより、Collector が `systemd` サービスとしてインストールされます

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
  sudo sh /tmp/splunk-otel-collector.sh --realm $REALM -- $ACCESS_TOKEN
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
Splunk OpenTelemetry Collector has been successfully installed.
```

{{% /tab %}}
{{< /tabs >}}

## ワークショップ用 Collector 設定の適用

デフォルトの Collector 設定は汎用的なものです。これを、AppDynamics エージェントから OTLP を受信し Splunk Observability Cloud にエクスポートするワークショップ専用の設定に置き換えます。まず、追加する内容を確認しましょう

```bash
vim ~/workshop/appd/collector-config.yaml
```

`processors:` の下にある以下のセクションを確認してください
{{< tabs >}}
{{% tab title="collector-config.yaml" %}}

```yaml
  resource/workshop:
    attributes:
      - key: host.name
        value: "${INSTANCE}"
        action: upsert
      - key: deployment.environment
        value: "${INSTANCE}-appd-dual"
        action: upsert 
      - key: deployment.environment.name
        value: "${INSTANCE}-appd-dual"
        action: upsert

  transform/drop_dims_high_cardinality:
      error_mode: ignore
      metric_statements:
        - context: resource
          conditions:
            - Len(resource.attributes) + Len(attributes) > 34
          statements:
            # Delete from datapoint attributes (where the Java agent puts them)
            - delete_key(attributes, "process.command_args") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.executable.path") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.runtime.description") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.runtime.name") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.runtime.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.pid") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "os.description") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "os.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "host.arch") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "host.image.id") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.distro.name") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.distro.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.sdk.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.sdk.name") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.sdk.language") where Len(resource.attributes) + Len(attributes) >= 34

            # Add marker
            - set(resource.attributes["cardinality.trimmed"], "true")
```

{{% /tab %}}
{{% /tabs %}}

これらのプロセッサーは、`host.name` と `deployment.enviroment`/`deployment.environment.name`（推奨）属性の変数を正しく参照するようにします。

`transform/drop_dims_high_cardinality` プロセッサーは [OpenTelemetry Transformation Language (OTTL)](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/LANGUAGE.md) を使用して、34を超える属性を持つメトリクスをチェックします（メトリクスに付与される実際の値もポイントとしてカウントされます）。

- **重要: 現在、属性が多すぎる（36を超える）メトリクスはバックエンドでドロップされます。** AppDynamics テレメトリでは追加の属性により、この問題が発生する可能性があります。

`transform` 設定では、メトリクスの属性の合計が34を超えているかどうかを確認し、超えている場合は価値が低い可能性のある属性を段階的に削除します。  
最後に、空きスペースを確認した後 `cardinality.trimmed` ディメンションを追加し、属性が削除されたメトリクスを簡単に識別できるようにします。

これらの各プロセッサーは、設定内のメトリクス用 `pipeline:` の末尾に含まれています。

次に、カスタム設定を `agent_config.yaml` に上書きコピーします

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

## Collector 環境変数の設定

Collector サービスは設定ファイルから環境変数を読み取ります。Splunk OTel Collector バイナリには `SPLUNK_REALM` と `SPLUNK_ACCESS_TOKEN`（`SPLUNK_` プレフィックス付き）が必要です。インスタンスには `REALM` と `ACCESS_TOKEN` があるため、それらをマッピングします

```bash
sudo bash -c "cat > /etc/otel/collector/splunk-otel-collector.conf << EOF
INSTANCE=${INSTANCE}
SPLUNK_INGEST_URL=https://ingest.${REALM}.signalfx.com
SPLUNK_CONFIG=/etc/otel/collector/agent_config.yaml
SPLUNK_ACCESS_TOKEN=${ACCESS_TOKEN}
SPLUNK_REALM=${REALM}
SPLUNK_API_URL=https://api.${REALM}.signalfx.com
SPLUNK_HEC_TOKEN=${HEC_TOKEN}
SPLUNK_HEC_URL=${HEC_URL}
SPLUNK_MEMORY_TOTAL_MIB=512
SPLUNK_BUNDLE_DIR=/usr/lib/splunk-otel-collector/agent-bundle
SPLUNK_COLLECTD_DIR=/usr/lib/splunk-otel-collector/agent-bundle/run/collectd
EOF"
```

## Collector の再起動

新しい設定を反映するために再起動します

{{< tabs >}}
{{% tab title="Command" %}}

```bash
sudo systemctl restart splunk-otel-collector
```

{{% /tab %}}
{{< /tabs >}}

## Collector の動作確認

{{< tabs >}}
{{% tab title="Command" %}}

```bash
sudo systemctl status splunk-otel-collector --no-pager
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
● splunk-otel-collector.service - Splunk OpenTelemetry Collector
     Loaded: loaded (/lib/systemd/system/splunk-otel-collector.service; enabled)
     Active: active (running) since ...
```

{{% /tab %}}
{{< /tabs >}}

ヘルスエンドポイントを確認します

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -s http://localhost:13133/
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk@ip-172-31-77-108 ~/workshop/appd $ curl -s http://localhost:13133/
{"status":"Server available","upSince":"2026-03-09T21:25:53.277371609Z","uptime":"22.684480311s"}%
```

{{% /tab %}}
{{< /tabs >}}

Collector はポート **4317**（gRPC）と **4318**（HTTP）で OTLP をリッスンしています。
