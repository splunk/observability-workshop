---
title: 3.2 Filter Processor のテスト
linkTitle: 3.2 Filter Processor のテスト
weight: 2
---

設定をテストするには、`"/_healthz"` という名前の span を含むトレースデータを生成する必要があります。

{{% exercise title="span がドロップされていることを検証する" %}}

**Gateway を起動する**: **Gateway terminal** ウィンドウで **Gateway** を起動します。

```bash
../otelcol --config ./gateway.yaml
```

**Agent を起動する**: **Agent terminal** ウィンドウで **Agent** を起動します。

```bash
../otelcol --config ./agent.yaml
```

**Loadgen を起動する**: **Loadgen terminal** ウィンドウで、以下のコマンドを実行し、ヘルスチェック span を有効にした状態でロードジェネレーターを起動します。
  
```bash
../loadgen -health -count 5
```

 **Agent terminal** のデバッグ出力に `_healthz` span が表示されます。

 ```text
 InstrumentationScope healthz 1.0.0
Span #0
    Trace ID       : 0cce8759b5921c8f40b346b2f6e2f4b6
    Parent ID      :
    ID             : bc32bd0e4ddcb174
    Name           : /_healthz
    Kind           : Server
    Start time     : 2025-07-11 08:47:50.938703979 +0000 UTC
    End time       : 2025-07-11 08:47:51.938704091 +0000 UTC
    Status code    : Ok
    Status message : Success
```

これらの span は、先ほど設定した filter processor によってドロップされるため、**Gateway** のデバッグ出力には現れません。

**`agent.out` を検証する**: **Test terminal** で `jq` を使用して、**Agent** が受信した span の名前を確認します。

{{% tabs %}}
{{% tab title="agent.out 内の span を確認する" %}}

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

**Gateway のデバッグ出力を確認する**: `jq` を使用して、**Gateway** が受信した span の名前を確認します。

{{% tabs %}}
{{% tab title="gateway-traces.out 内の span を確認する" %}}

```bash
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with name \(.name)"' ./gateway-traces.out
```

{{% /tab %}}
{{% tab title="出力例" %}}

`gateway-metrics.out` ファイルには `/_healthz` という名前の span は含まれません。

```text
"Span 1 found with name /movie-validator"
"Span 2 found with name /movie-validator"
"Span 3 found with name /movie-validator"
"Span 4 found with name /movie-validator"
"Span 5 found with name /movie-validator"
```

{{% /tab %}}
{{% /tabs %}}

{{% /exercise %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}

Filter processor で最適なパフォーマンスを得るには、入力データのフォーマットを十分に理解し、設定を厳密にテストしてください。**できる限り具体的なフィルタ条件を使用** することで、重要なデータを誤ってドロップしてしまうリスクを最小化できます。

この設定は、さまざまな属性、タグ、またはカスタム条件に基づいて span をフィルタリングするように拡張可能で、特定のオブザーバビリティ要件に応じて OpenTelemetry Collector の柔軟性と効率性を高められます。
{{% /notice %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して **Agent** および **Gateway** プロセスを停止してください。

<!--
---
The following excises can be done in your own time after the workshop.

**(Optional) Modify the Filter Condition**:

If you’d like, you can customize the filter condition to drop spans based on different criteria. This step is optional and can be explored later. For example, you might configure the filter to drop spans that include a specific tag or attribute.

Here’s an example of dropping spans based on an attribute:

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
