---
title: 2.4 リカバリー
linkTitle: 2.4 リカバリー
weight: 4
---

この演習では、**Gateway** Collectorを再起動してネットワーク障害からの **OpenTelemetry Collector** の回復をテストします。**Gateway** が再び利用可能になると、**Agent** は最後のチェックポイントの状態からデータ送信を再開し、データの損失がないことを確認します。

{{% exercise title="再起動とリカバリーの検証" %}}

**Gatewayの再起動**: **Gatewayターミナル** ウィンドウで以下を実行します

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

**Agentの再起動**: **Agentターミナル** ウィンドウで以下を実行します

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

> **Agent** が起動して実行された後、**File_Storage** extensionはチェックポイントフォルダー内のバッファされたデータを検出します。最後のチェックポイントフォルダーから保存されたSpanのデキューを開始し、データが失われないようにします。

**Agentのデバッグ出力の確認:** **Agent** のデバッグ出力は変化せず、新しいデータがエクスポートされていないことを示す以下の行が表示されたままであることに注意してください。
  
  ```text
  2025-07-11T08:31:58.176Z        info    service@v0.126.0/service.go:289 Everything is ready. Begin running and processing data.   {"resource": {}}
  ```

**Gatewayのデバッグ出力の確認**  
**Gateway** のデバッグ画面から、追加のアクションなしに以前送信できなかったTraceの受信が開始されたことが確認できます。例:

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

**`gateway-traces.out`ファイルの確認:**  `jq`を使用して、再作成された`gateway-traces.out`内のTrace数をカウントします。**Gateway** がダウンしていた間に送信した数と一致するはずです。

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

{{% /exercise %}}

> [!IMPORTANT]
> それぞれのターミナルで`Ctrl-C`を押して、**Agent** と **Gateway** のプロセスを停止してください。

### まとめ

この演習では、`file_storage` extensionの設定、`otlp` Exporterのリトライメカニズムの有効化、およびファイルベースのキューによる一時的なデータストレージの使用により、OpenTelemetry Collectorの耐障害性を強化する方法を示しました。

ファイルベースのチェックポイントとキューの永続化を実装することで、テレメトリパイプラインが一時的な中断から正常に回復でき、本番環境でより堅牢で信頼性の高いものになります。
