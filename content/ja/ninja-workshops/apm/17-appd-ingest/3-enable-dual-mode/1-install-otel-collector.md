---
title: 1. OTel Collector のインストール
weight: 1
---

dual モードの AppDynamics エージェントは OpenTelemetry データを OTLP で出力します。そのデータを受信して Splunk Observability Cloud に転送するため、同じホスト上にコレクターが必要です。

## 環境変数の確認

インスタンスにはこれらの変数があらかじめ設定されているはずです。`env` または以下のコマンドで利用可能であることを確認してください。

```bash
echo "REALM=$REALM"
echo "ACCESS_TOKEN=$ACCESS_TOKEN"
echo "INSTANCE=$INSTANCE"
```

3 つすべてに値が設定されている必要があります。いずれかが空の場合は、講師に確認してください。

## Splunk OpenTelemetry Collector のインストール

Splunk OTel Collector のインストールスクリプトを実行します。これによりコレクターが `systemd` サービスとしてインストールされます。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
  sudo sh /tmp/splunk-otel-collector.sh --realm $REALM --deployment-environment ${INSTANCE}-appd-dual --hec-token ${HEC_TOKEN} --hec-url ${HEC_URL}  -- $ACCESS_TOKEN
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
Splunk OpenTelemetry Collector has been successfully installed.
```

{{% /tab %}}
{{< /tabs >}}

ここでは `--deployment-environment` で環境を、`--hec-token` と `--hec-url` で HEC ログエクスポートの詳細を確実に渡しています。これはログを取得して相関させるために重要です。

## Workshop 用 Collector 設定の適用

デフォルトのコレクター設定は汎用的なものです。これを、AppDynamics エージェントから OTLP を受信し Splunk Observability Cloud にエクスポートするワークショップ専用の設定に置き換えます。その前に、何を追加するのか見てみましょう。

```bash
vim ~/workshop/appd/collector-config.yaml
```

`processors:` の下にある以下のセクションを探してください。
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
{{% /tabs %}}
`transform/drop_dims_high_cardinality` プロセッサーは [OpenTelemetry Transformation Language (OTTL)](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/LANGUAGE.md) を使用して、属性が 34 を超えるメトリクスがないかチェックします（メトリクスにアタッチされた実際の値も 1 ポイントとしてカウントされます）。

- **重要: 現在、属性が多すぎる（>36）メトリクスはバックエンドでドロップされます。** これは追加の属性により AppDynamics のテレメトリーで発生する可能性があります。

`transform` 設定では、メトリクスの属性数の合計が 34 を超えるかをチェックし、超えている場合は重要度の低い属性を順次削除しています。
最後に、削除された属性を持つメトリクスを簡単に識別できるよう、空きがあれば `cardinality.trimmed` のディメンションを追加するチェックを行います。

これらのプロセッサーはそれぞれ、設定内のメトリクス用 `pipeline:` の末尾に組み込まれています。

次に、このカスタム設定を `agent_config.yaml` に上書きコピーします。

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

## Collector の再起動

新しい設定を反映させるために再起動します。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
sudo systemctl restart splunk-otel-collector
```

{{% /tab %}}
{{< /tabs >}}

## Collector が稼働していることの確認

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

ヘルスエンドポイントを確認します。

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

これでコレクターはポート **4317**（gRPC）および **4318**（HTTP）で OTLP をリッスンするようになりました。
