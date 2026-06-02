---
title: 4.4 Recovery
linkTitle: 4.4 Recovery
weight: 4
---

この演習では、**Gateway** コレクターを再起動することで、**OpenTelemetry Collector** がネットワーク障害からどのように回復するかをテストします。`gateway` が再び利用可能になると、`agent` は最後にチェックポイントが記録された状態からデータの送信を再開し、データ損失が発生しないことを保証します。

{{% notice title="演習" style="green" icon="running" %}}

**Gateway を再起動する**: **Gateway ターミナル** ウィンドウで以下を実行します。

```bash {title="Gateway"}
../otelcol --config=gateway.yaml
```

**Agent を再起動する**: **Agent ターミナル** ウィンドウで以下を実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

{{% /notice %}}

`agent` が起動して稼働を開始すると、**File_Storage** 拡張機能はチェックポイントフォルダー内にバッファリングされたデータを検出します。  
そして、最後のチェックポイントフォルダーから保存済みのスパンをデキューし始め、データが失われないようにします。

{{% notice title="演習" style="green" icon="running" %}}

**Agent のデバッグ出力を確認する**  
Agent のデバッグ画面は変化**しない**ことに注意してください。次の行が表示されたままで、新しいデータがエクスポートされていないことを示しています。
  
  ```text
  2025-02-07T13:40:12.195+0100    info    service@v0.120.0/service.go:253 Everything is ready. Begin running and processing data.
  ```

**Gateway のデバッグ出力を観察する**  
`gateway` のデバッグ画面では、追加の操作を一切行わなくても、それまで送信できなかったトレースの受信を開始したことが確認できるはずです。  

  ```txt
  2025-02-07T12:44:32.651+0100    info    service@v0.120.0/service.go:253 Everything is ready. Begin running and processing data.
  2025-02-07T12:47:46.721+0100    info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 4, "spans": 4}
  2025-02-07T12:47:46.721+0100    info    ResourceSpans #0
  Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
  Resource attributes:
  ```

**`gateway-traces.out` ファイルを確認する**  
`jq` を使用して、再生成された `gateway-traces.out` 内のトレース数をカウントします。`gateway` がダウンしていた間に送信した数と一致しているはずです。

{{% tabs %}}
{{% tab title="Check Gateway Traces Out File" %}}

```bash
jq '.resourceSpans | length | "\(.) resourceSpans found"' gateway-traces.out
```

{{% /tab %}}

{{% tab title="Example output" %}}

```text
"5 resourceSpans found"
```

{{% /tab %}}
{{% /tabs %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent` プロセスと `gateway` プロセスを停止してください。

{{% /notice %}}

### まとめ

この演習では、`file_storage` 拡張機能を構成し、`otlp` エクスポーターのリトライ機構を有効化し、ファイルバックアップキューを一時的なデータ保存に使用することで、OpenTelemetry Collector のレジリエンスをどのように高められるかを示しました。

ファイルベースのチェックポイント処理とキューの永続化を実装することで、テレメトリーパイプラインは一時的な中断から優雅に回復できるようになり、本番環境においてより堅牢で信頼性の高いものとなります。
