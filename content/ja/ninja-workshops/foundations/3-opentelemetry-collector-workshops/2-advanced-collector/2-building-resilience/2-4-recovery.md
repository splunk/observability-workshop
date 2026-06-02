---
title: 2.4 Recovery
linkTitle: 2.4 Recovery
weight: 4
---

このエクササイズでは、**Gateway** Collector を再起動することで、**OpenTelemetry Collector** がネットワーク障害からどのように回復するかをテストします。**Gateway** が再び利用可能になると、**Agent** は最後のチェックポイント状態からデータの送信を再開し、データロスが発生しないことを保証します。

{{% exercise title="Restart and verify recovery" %}}

**Gateway を再起動する**: **Gateway terminal** ウィンドウで以下を実行します:

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

**Agent を再起動する**: **Agent terminal** ウィンドウで以下を実行します:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

> **Agent** が起動すると、**File_Storage** 拡張機能が checkpoint フォルダー内のバッファされたデータを検出します。最後の checkpoint フォルダーから保存されたスパンのデキューを開始し、データが失われないことを保証します。

**Agent デバッグ出力を確認する:** **Agent** のデバッグ出力は変化せず、以下の行が表示され続け、新しいデータがエクスポートされていないことを示している点に注意してください:
  
  ```text
  2025-07-11T08:31:58.176Z        info    service@v0.126.0/service.go:289 Everything is ready. Begin running and processing data.   {"resource": {}}
  ```

**Gateway デバッグ出力を観察する**  
**Gateway** のデバッグ画面から、追加の操作を行わなくても、それまで欠落していたトレースの受信を開始していることが確認できるはずです。例:

  ```txt
Attributes:
     -> user.name: Str(Luke Skywalker)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
     -> payment.amount: Double(75.75)
        {"resource": {}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
  ```

**`gateway-traces.out` ファイルを確認する:** `jq` を使用して、再作成された `gateway-traces.out` 内のトレースの数をカウントします。**Gateway** がダウンしていた間に送信した数と一致するはずです。

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

{{% /exercise %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止します。

### Conclusion

このエクササイズでは、`file_storage` 拡張機能を構成し、`otlp` exporter のリトライ機構を有効化し、一時データ保存用にファイルバックドキューを使用することで、OpenTelemetry Collector のレジリエンスを強化する方法を実演しました。

ファイルベースのチェックポイントとキューの永続化を実装することで、テレメトリーパイプラインが一時的な中断から正常に回復できるようになり、本番環境向けに、より堅牢で信頼性の高いものにできます。
