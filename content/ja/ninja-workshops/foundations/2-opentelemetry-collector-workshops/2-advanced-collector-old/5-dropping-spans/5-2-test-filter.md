---
title: 5.2 Filter Processor のテスト
linkTitle: 5.2 Filter Processor のテスト
weight: 2
---

設定をテストするには、`"/_healthz"` という名前のSpanを含むトレースデータを生成する必要があります。

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway の起動**: **Gateway ターミナル** ウィンドウで `gateway` を起動します。

```bash
../otelcol --config ./gateway.yaml
```

**Agent の起動**: **Agent ターミナル** ウィンドウで `agent` を起動します。

```bash
../otelcol --config ./agent.yaml
```

**Loadgen の起動**: **Spans ターミナル** ウィンドウで、基本的なSpanと一緒に `healthz` Spanも送信するフラグを付けて `loadgen` を実行します。
  
```bash
../loadgen -health -count 5
```

**`agent.out` の確認**: `jq` を使用して、`agent` が受信したSpanの名前を確認します。

{{% tabs %}}
{{% tab title="agent.out のSpanを確認" %}}

```bash
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with name \(.name)"' ./agent.out
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
"Span 1 found with name /movie-validator"
"Span 2 found with name /_healthz"
"Span 3 found with name /movie-validator"
"Span 4 found with name /_healthz"
"Span 5 found with name /movie-validator"
"Span 6 found with name /_healthz"
"Span 7 found with name /movie-validator"
"Span 8 found with name /_healthz"
"Span 9 found with name /movie-validator"
"Span 10 found with name /_healthz"
```

{{% /tab %}}
{{% /tabs %}}

**Gateway のデバッグ出力を確認**: `jq` を使用して、`gateway` が受信したSpanの名前を確認します。

{{% tabs %}}
{{% tab title="gateway-traces.out のSpanを確認" %}}

```bash { title="Check spans in gateway-traces.out" }
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with name \(.name)"' ./gateway-traces.out
```

{{% /tab %}}
{{% tab title="出力例" %}}

`gateway-metrics.out` ファイルには `/_healthz` という名前のSpanは含まれません。

```text
"Span 1 found with name /movie-validator"
"Span 2 found with name /movie-validator"
"Span 3 found with name /movie-validator"
"Span 4 found with name /movie-validator"
"Span 5 found with name /movie-validator"
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}

`Filter` Processor を使用する際は、受信データの構造を理解し、設定を十分にテストしてください。一般的に、誤ったデータが削除されるリスクを低減するために、**できるだけ具体的な設定** を使用してください。

この設定をさらに拡張して、異なる属性、タグ、その他の条件に基づいてSpanをフィルタリングすることで、OpenTelemetry Collectorをオブザーバビリティのニーズに合わせてよりカスタマイズ可能かつ効率的にできます。

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}
<!--
---
The following excises can be done in your own time after the workshop.

**(Optional) Modify the Filter Condition**:

If you'd like, you can customize the filter condition to drop spans based on different criteria. This step is optional and can be explored later. For example, you might configure the filter to drop spans that include a specific tag or attribute.

Here's an example of dropping spans based on an attribute:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'attributes["service.name"] == "frontend"'
```

This filter would drop spans where the `service.name` attribute is set to `frontend`.

**(Optional) Filter Multiple Spans**:

You can filter out multiple span names by extending the span list:

```yaml
filter:
  error_mode: ignore
  traces:
    span:
      - 'name == "/_healthz"'
      - 'name == "/internal/metrics"'
```

This will drop spans with the names `"/_healthz"` and `"/internal/metrics"`.
-->
