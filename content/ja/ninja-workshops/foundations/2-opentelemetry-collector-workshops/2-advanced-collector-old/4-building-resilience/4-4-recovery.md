---
title: 4.4 リカバリー
linkTitle: 4.4 リカバリー
weight: 4
---

この演習では、**Gateway** Collectorを再起動することで、**OpenTelemetry Collector** がネットワーク障害からどのようにリカバリーするかをテストします。`gateway`が再び利用可能になると、`agent`は最後のチェックポイント状態からデータ送信を再開し、データ損失が発生しないことを確認します。

{{% notice title="Exercise" style="green" icon="running" %}}

**Gatewayの再起動**: **Gatewayターミナル** ウィンドウで以下を実行します

```bash {title="Gateway"}
../otelcol --config=gateway.yaml
```

**Agentの再起動**: **Agentターミナル** ウィンドウで以下を実行します

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

{{% /notice %}}

`agent`が起動して稼働すると、**File_Storage** エクステンションがチェックポイントフォルダー内のバッファされたデータを検出します。  
最後のチェックポイントフォルダーから保存されたSpanのデキューを開始し、データが失われないことを保証します。

{{% notice title="Exercise" style="green" icon="running" %}}

**Agentのデバッグ出力を確認する**  
Agentのデバッグ画面は変更 **されず** 、以下の行が表示されたままであることに注意してください。これは新しいデータがエクスポートされていないことを示しています。
  
  ```text
  2025-02-07T13:40:12.195+0100    info    service@v0.120.0/service.go:253 Everything is ready. Begin running and processing data.
  ```

**Gatewayのデバッグ出力を監視する**  
`gateway`のデバッグ画面から、追加のアクションなしに、以前に失われたトレースの受信が開始されたことが表示されます。  

  ```txt
  2025-02-07T12:44:32.651+0100    info    service@v0.120.0/service.go:253 Everything is ready. Begin running and processing data.
  2025-02-07T12:47:46.721+0100    info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 4, "spans": 4}
  2025-02-07T12:47:46.721+0100    info    ResourceSpans #0
  Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
  Resource attributes:
  ```

**`gateway-traces.out` ファイルを確認する**  
`jq`を使用して、再作成された `gateway-traces.out` 内のトレース数をカウントします。`gateway`がダウンしていたときに送信した数と一致するはずです。

{{% tabs %}}
{{% tab title="Gateway Traces Outファイルの確認" %}}

```bash
jq '.resourceSpans | length | "\(.) resourceSpans found"' gateway-traces.out
```

{{% /tab %}}

{{% tab title="出力例" %}}

```text
"5 resourceSpans found"
```

{{% /tab %}}
{{% /tabs %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent`と `gateway`のプロセスを停止してください。

{{% /notice %}}

### まとめ

この演習では、`file_storage`エクステンションの設定、`otlp` Exporterのリトライメカニズムの有効化、および一時的なデータ保存のためのファイルバックアップキューの使用により、OpenTelemetry Collectorの耐障害性を強化する方法を示しました。

ファイルベースのチェックポイントとキューの永続化を実装することで、テレメトリーパイプラインが一時的な中断から正常にリカバリーできるようになり、本番環境にとってより堅牢で信頼性の高いものになります。
