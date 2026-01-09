---
title: 2.4 復旧
linkTitle: 2.4 Recovery
weight: 4
---

この演習では、**Gateway** Collector を再起動することで、**OpenTelemetry Collector** がネットワーク障害からどのように復旧するかをテストします。**Gateway** が再び利用可能になると、**Agent** は最後にチェックポイントされた状態からデータの送信を再開し、データ損失がないことを保証します。

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway の再起動**: **Gateway ターミナル** ウィンドウで以下を実行します：

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

**Agent の再起動**: **Agent ターミナル** ウィンドウで以下を実行します：

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

> **Agent** が起動して実行されると、**File_Storage** Extension がチェックポイントフォルダー内のバッファされたデータを検出します。最後のチェックポイントフォルダーから保存されたスパンをデキューし始め、データが失われないことを保証します。

**Agent デバッグ出力の確認:** **Agent** のデバッグ出力は変化**せず**、以下の行を表示し続け、新しいデータがエクスポートされていないことを示していることに注意してください：

  ```text
  2025-07-11T08:31:58.176Z        info    service@v0.126.0/service.go:289 Everything is ready. Begin running and processing data.   {"resource": {}}
  ```

**Gateway デバッグ出力の確認**
**Gateway** のデバッグ画面から、以前見逃されていたトレースを追加のアクションなしで受信し始めていることが確認できるはずです。例：

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

**`gateway-traces.out` ファイルの確認:** `jq` を使用して、再作成された `gateway-traces.out` 内のトレース数をカウントします。**Gateway** がダウンしていたときに送信した数と一致するはずです。

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

{{% /notice %}}

> [!IMPORTANT]
> **Agent** と **Gateway** のプロセスを、それぞれのターミナルで `Ctrl-C` を押して停止してください。

### まとめ

この演習では、`file_storage` Extension の設定、`otlp` Exporter のリトライメカニズムの有効化、および一時的なデータ保存用のファイルベースのキューの使用により、OpenTelemetry Collector の耐障害性を強化する方法を示しました。

ファイルベースのチェックポイントとキューの永続化を実装することで、テレメトリーパイプラインが一時的な中断から適切に復旧できることを保証し、本番環境でより堅牢で信頼性の高いものにします。
