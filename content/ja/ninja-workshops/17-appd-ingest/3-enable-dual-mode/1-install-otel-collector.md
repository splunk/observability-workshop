---
title: 1. OTel Collector のインストール
weight: 1
---

デュアルモードのAppDynamicsエージェントは、OTLP経由でOpenTelemetryデータを出力します。このデータを受信してSplunk Observability Cloudに転送するために、同じホスト上にコレクターが必要です。

## 環境変数の確認

インスタンスにはこれらの変数が事前に設定されているはずです。利用可能であることを確認してください：

```bash
echo "REALM=$REALM"
echo "ACCESS_TOKEN=$ACCESS_TOKEN"
echo "INSTANCE=$INSTANCE"
```

3つすべてに値が設定されている必要があります。いずれかが空の場合は、インストラクターに確認してください。

## Splunk OpenTelemetry Collector のインストール

Splunk OTel Collectorのインストールスクリプトを実行します。これにより、コレクターが `systemd` サービスとしてインストールされます：

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

デフォルトのコレクター設定は汎用的なものです。AppDynamicsエージェントからOTLPを受信し、Splunk Observability Cloudにエクスポートするワークショップ専用の設定に置き換えます：

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

## コレクターの環境変数の設定

コレクターサービスは設定ファイルから環境変数を読み込みます。Splunk OTel Collectorバイナリには `SPLUNK_REALM` と `SPLUNK_ACCESS_TOKEN`（`SPLUNK_` プレフィックス付き）が必要です。インスタンスには `REALM` と `ACCESS_TOKEN` があるため、それらをマッピングします：

```bash
sudo bash -c "cat > /etc/otel/collector/splunk-otel-collector.conf << EOF
SPLUNK_REALM=${REALM}
SPLUNK_ACCESS_TOKEN=${ACCESS_TOKEN}
INSTANCE=${INSTANCE}
EOF"
```

## コレクターの再起動

新しい設定を適用するために再起動します：

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

ヘルスエンドポイントを確認します：

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

これでコレクターはポート **4317**（gRPC）と **4318**（HTTP）でOTLPをリッスンしています。
