---
title: 1. OTel Collector のインストール
weight: 1
---

デュアルモードの AppDynamics エージェントは、OTLP 経由で OpenTelemetry データを送信します。そのデータを受信して Splunk Observability Cloud に転送するために、同じホスト上にコレクターが必要です。

## 環境変数の確認

インスタンスにはこれらの変数が事前に設定されているはずです。`env` または以下のコマンドで利用可能であることを確認してください

```bash
echo "REALM=$REALM"
echo "ACCESS_TOKEN=$ACCESS_TOKEN"
echo "INSTANCE=$INSTANCE"
```

3つすべてに値が設定されている必要があります。いずれかが空の場合は、インストラクターに確認してください。

## Splunk OpenTelemetry Collector のインストール

Splunk OTel Collector のインストールスクリプトを実行します。これにより、コレクターが `systemd` サービスとしてインストールされます

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

## ワークショップ用コレクター設定の適用

デフォルトのコレクター設定は汎用的なものです。これを、AppDynamics エージェントからの OTLP を受信して Splunk Observability Cloud にエクスポートするワークショップ固有の設定に置き換えます。まず、追加する内容を確認しましょう

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

これらのプロセッサーは、`host.name` と `deployment.enviroment`/`deployment.environment.name`（推奨）属性に対して変数を正しく参照するようにします。

`transform/drop_dims_high_cardinality` プロセッサーは、[OpenTelemetry Transformation Language (OTTL)](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/LANGUAGE.md) を使用して、メトリクスの属性が34を超えていないかチェックします（メトリクスに付加される実際の値もポイントとしてカウントされます）。

- **重要: 現在、バックエンドでは属性が多すぎるメトリクス（>36）はドロップされます。** これは、AppDynamics テレメトリーの追加属性により発生する可能性があります。

`transform` の設定では、メトリクスの結合属性数が34を超えているかどうかをチェックし、超えている場合は重要度の低い属性を段階的に削除します。
最後に、空きスペースを確認した上で `cardinality.trimmed` ディメンションを追加し、属性が削除されたメトリクスを簡単に識別できるようにします。

これらのプロセッサーはそれぞれ、設定内のメトリクス用 `pipeline:` の末尾に含まれています。

次に、そのカスタム設定を `agent_config.yaml` にコピーします

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

## コレクターの環境変数の設定

コレクターサービスは設定ファイルから環境変数を読み取ります。Splunk OTel Collector バイナリは `SPLUNK_REALM` と `SPLUNK_ACCESS_TOKEN`（`SPLUNK_` プレフィックス付き）を必要とします。インスタンスには `REALM` と `ACCESS_TOKEN` があるため、それらをマッピングします

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

## コレクターの再起動

新しい設定を適用するために再起動します

{{< tabs >}}
{{% tab title="Command" %}}

```bash
sudo systemctl restart splunk-otel-collector
```

{{% /tab %}}
{{< /tabs >}}

## コレクターの動作確認

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
curl -s http://localhost:13133/ | jq
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk@ip-172-31-47-33 ~/workshop/appd $ curl -s http://localhost:13133/ | jq
{
  "status": "Server available",
  "upSince": "2026-05-04T16:02:29.509202038Z",
  "uptime": "30.174963775s"
}
```

{{% /tab %}}
{{< /tabs >}}

コレクターは現在、ポート **4317**（gRPC）と **4318**（HTTP）で OTLP をリッスンしています。
