---
title: 2.5 補足 - アクセストークンとバッチ処理に関する情報
linkTitle: 2.5 Addendum
weight: 5
hidden: true
---


{{% notice title="ヒント" style="primary" icon="lightbulb" %}}

## otlphttp Exporter の概要

`otlphttp` exporter は、Splunk Observability Cloud にメトリクスとトレースを送信する際の現在のデフォルトの方式です。この exporter は、OpenTelemetry Protocol (OTLP) を HTTP 経由で利用し、テレメトリデータを標準化された効率的な方法で送信できます。

Splunk Distribution of the OpenTelemetry Collector をホスト監視 (agent) モードでデプロイする場合、`otlphttp` exporter はデフォルトで含まれています。これは `sapm` や `signalfx` といった旧来の exporter を置き換えるもので、これらの旧 exporter は段階的に廃止されつつあります。

{{% /notice %}}

## Splunk アクセストークンの設定

Splunk Observability Cloud に対して認証を行いデータを送信するには、アクセストークンを適切に設定する必要があります。
OpenTelemetry では、認証は HTTP ヘッダーを介して処理されます。アクセストークンを渡すには、`headers:` キーとそのサブキーである `X-SF-Token:` を使用します。この設定は agent モードと gateway モードの両方で機能します。

例:

```yaml
exporters:
  otlphttp:
    endpoint: "https://ingest.<realm>.signalfx.com"
    headers:
      X-SF-Token: "your-access-token"
```

### Pass-Through モード

ヘッダーをパイプライン経由で転送する必要がある場合は、OTLP receiver の設定で `include_metadata:` を `true` に設定し、pass-through モードを有効にしてください。これにより、collector が受信した認証ヘッダーが保持され、データとともに転送されます。

例:

```yaml
receivers:
  otlp:
    protocols:
      http:
        include_metadata: true
```

これは特に gateway モードにおいて有用で、複数の agent からのデータが Splunk へ送信される前に集約された gateway を経由するケースで役立ちます。

## バッチ処理の理解

Batch Processor は、データ送信効率を最適化するための重要なコンポーネントです。トレース、メトリクス、ログをバッチにまとめてからバックエンドに送信します。バッチ処理は以下の点でパフォーマンスを向上させます。

- 送信リクエスト数を削減します。
- 圧縮効率を向上させます。
- ネットワークオーバーヘッドを低減します。

### Batch Processor の設定

バッチ処理を有効にするには、`batch:` セクションを設定し、`X-SF-Token:` キーを含めてください。これにより、Splunk Observability Cloud に送信される前にデータが正しくグループ化されます。

例:

```yaml
processors:
  batch:
    metadata_keys: [X-SF-Token]   # Array of metadata keys to batch 
    send_batch_size: 100
    timeout: 5s
```

### バッチ処理のベストプラクティス

最適なパフォーマンスを得るためには、すべての collector のデプロイに Batch Processor を使用することが推奨されます。Batch Processor の最適な配置位置は、**memory limiter およびサンプリング processor の後** です。これにより、必要なデータのみがバッチ化され、ドロップされたデータに対する不要な処理を回避できます。

### Batch Processor を使った Gateway の設定

gateway をデプロイする際は、Batch Processor がパイプラインに含まれていることを確認してください。

```yaml
service:
  pipelines:
    traces:
      processors: [memory_limiter, tail_sampling, batch]
```

## まとめ

`otlphttp` exporter は、Splunk Observability Cloud にテレメトリデータを送信する際に現在推奨される方式です。Splunk アクセストークンを適切に設定することで安全なデータ送信が可能になり、Batch Processor によりネットワークオーバーヘッドを削減してパフォーマンスを最適化できます。これらのベストプラクティスを実践することで、オブザーバビリティデータを大規模に効率よく収集・送信できます。
