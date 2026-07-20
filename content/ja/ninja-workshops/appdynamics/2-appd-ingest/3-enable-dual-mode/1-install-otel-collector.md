---
title: 1. OTel Collectorのインストール
weight: 1
---

デュアルモードのAppDynamicsエージェントはOTLP経由でOpenTelemetryデータを送信します。そのデータを受信してSplunk Observability Cloudに転送するために、同じホスト上にCollectorが必要です。

## 環境変数の確認

インスタンスにはこれらの変数が事前に設定されているはずです。`env` または以下のコマンドで利用可能であることを確認します。

```bash
echo "REALM=$REALM"
echo "ACCESS_TOKEN=$ACCESS_TOKEN"
echo "INSTANCE=$INSTANCE"
```

3つすべてに値が設定されている必要があります。空のものがある場合は、インストラクターに確認してください。

## Splunk OpenTelemetry Collectorのインストール

Splunk OTel Collectorのインストールスクリプトを実行します。これによりCollectorが `systemd` サービスとしてインストールされます。

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
  sudo sh /tmp/splunk-otel-collector.sh --realm $REALM --deployment-environment ${INSTANCE}-appd-dual --hec-token ${HEC_TOKEN} --hec-url ${HEC_URL}  -- $ACCESS_TOKEN
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
Splunk OpenTelemetry Collector has been successfully installed.
```

{{% /tab %}}
{{< /tabs >}}

ここでは `--deployment-environment` で環境情報を渡し、`--hec-token` と `--hec-url` でHECログエクスポートの詳細を渡しています。これはログを出力し、相関させるために重要です。

## ワークショップ用Collector設定の適用

デフォルトのCollector設定は汎用的なものです。AppDynamicsエージェントからOTLPを受信し、Splunk Observability Cloudにエクスポートするワークショップ固有の設定に置き換えます。まず、追加する内容を確認しましょう。

```bash
vim ~/workshop/appd/collector-config.yaml
```

`processors:` の下にある以下のセクションを確認します。
{{< tabs >}}
{{% tab title="collector-config.yaml" %}}

```yaml
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
{{< /tabs >}}
`transform/drop_dims_high_cardinality` Processorは [OpenTelemetry Transformation Language (OTTL)](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/LANGUAGE.md) を使用して、34を超える属性を持つメトリクスをチェックします（メトリクスに付加される実際の値もポイントとしてカウントされます）。

- **重要: 現在、バックエンドでは属性が多すぎる（36超）メトリクスはドロップされます。** これはAppDynamicsテレメトリでは追加の属性により発生する可能性があります。

この `transform` 設定では、メトリクスの属性が合計34を超えているかをチェックし、超えている場合は価値の低い属性を段階的に削除します。
最後に、利用可能なスペースを確認した上で `cardinality.trimmed` ディメンションを追加し、属性が削除されたメトリクスを簡単に識別できるようにします。

これらの各Processorは、設定内のメトリクス用 `pipeline:` の末尾に含まれています。

次に、そのカスタム設定を `agent_config.yaml` に上書きコピーします。

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

## Collectorの再起動

新しい設定を反映するために再起動します。

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
sudo systemctl restart splunk-otel-collector
```

{{% /tab %}}
{{< /tabs >}}

## Collectorの動作確認

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
sudo systemctl status splunk-otel-collector --no-pager
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
● splunk-otel-collector.service - Splunk OpenTelemetry Collector
     Loaded: loaded (/lib/systemd/system/splunk-otel-collector.service; enabled)
     Active: active (running) since ...
```

{{% /tab %}}
{{< /tabs >}}

ヘルスエンドポイントを確認します。

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
curl -s http://localhost:13133/ | jq
```

{{% /tab %}}
{{% tab title="出力例" %}}

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

Collectorはポート **4317**（gRPC）と **4318**（HTTP）でOTLPをリッスンしています。
