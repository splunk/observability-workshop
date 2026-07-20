---
title: 2.5 補足 - アクセストークンとバッチ処理について
linkTitle: 2.5 補足
weight: 5
hidden: true
---


{{% notice title="ヒント" style="primary" icon="lightbulb" %}}

## otlphttp Exporterの紹介

`otlphttp` Exporterは、Splunk Observability Cloudにメトリクスとトレースをエクスポートするためのデフォルトの方法です。このExporterは、OpenTelemetry Protocol（OTLP）over HTTPを使用してテレメトリデータを送信する、標準化された効率的な方法を提供します。

Splunk Distribution of the OpenTelemetry Collectorをホストモニタリング（エージェント）モードでデプロイする場合、`otlphttp` Exporterはデフォルトで含まれています。これは、段階的に廃止されつつある `sapm` や `signalfx` などの古いExporterに代わるものです。

{{% /notice %}}

## Splunkアクセストークンの設定

Splunk Observability Cloudに認証してデータを送信するには、アクセストークンを適切に設定する必要があります。
OpenTelemetryでは、認証はHTTPヘッダーを介して処理されます。アクセストークンを渡すには、`headers:` キーとサブキー `X-SF-Token:` を使用します。この設定はエージェントモードとゲートウェイモードの両方で動作します。

例:

```yaml
exporters:
  otlphttp:
    endpoint: "https://ingest.<realm>.signalfx.com"
    headers:
      X-SF-Token: "your-access-token"
```

### パススルーモード

パイプラインを通じてヘッダーを転送する必要がある場合は、OTLP Receiverの設定で `include_metadata:` を `true` に設定してパススルーモードを有効にします。これにより、Collectorが受信した認証ヘッダーが保持され、データとともに転送されます。

例:

```yaml
receivers:
  otlp:
    protocols:
      http:
        include_metadata: true
```

これは、複数のエージェントからのデータがSplunkに送信される前に集中ゲートウェイを通過するゲートウェイモードで特に有用です。

## バッチ処理の理解

Batch Processorは、データ送信効率を最適化するための重要なコンポーネントです。トレース、メトリクス、ログをバッチにグループ化してからバックエンドに送信します。バッチ処理は以下の点でパフォーマンスを向上させます:

- 送信リクエスト数の削減
- 圧縮効率の向上
- ネットワークオーバーヘッドの低減

### Batch Processorの設定

バッチ処理を有効にするには、`batch:` セクションを設定し、`X-SF-Token:` キーを含めます。これにより、Splunk Observability Cloudに送信される前にデータが正しくグループ化されます。

例:

```yaml
processors:
  batch:
    metadata_keys: [X-SF-Token]   # Array of metadata keys to batch 
    send_batch_size: 100
    timeout: 5s
```

### バッチ処理のベストプラクティス

最適なパフォーマンスのために、すべてのCollectorデプロイメントでBatch Processorを使用することを推奨します。Batch Processorの最適な配置場所は **memory limiterとsampling Processorの後** です。これにより、必要なデータのみがバッチ処理され、ドロップされたデータの不要な処理を回避できます。

### Batch Processorを使用したゲートウェイ設定

ゲートウェイをデプロイする際は、パイプラインにBatch Processorが含まれていることを確認してください:

```yaml
service:
  pipelines:
    traces:
      processors: [memory_limiter, tail_sampling, batch]
```

## まとめ

`otlphttp` Exporterは、Splunk Observability Cloudにテレメトリデータを送信するための推奨される方法です。Splunkアクセストークンを適切に設定することで安全なデータ送信が保証され、Batch Processorはネットワークオーバーヘッドを削減してパフォーマンスを最適化します。これらのベストプラクティスを実装することで、オブザーバビリティデータを大規模に効率的に収集・送信できます。
