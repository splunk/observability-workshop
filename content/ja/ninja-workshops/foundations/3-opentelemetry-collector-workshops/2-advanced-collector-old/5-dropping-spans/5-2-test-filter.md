---
title: 5.2 Test Filter Processor
linkTitle: 5.2 Test Filter Processor
weight: 2
---

設定をテストするには、`"/_healthz"` という名前のスパンを含むトレースデータを生成する必要があります。

{{% notice title="演習" style="green" icon="running" %}}

**Gateway を起動する**: **Gateway terminal** ウィンドウで `gateway` を起動します。

```bash
../otelcol --config ./gateway.yaml
```

**Agent を起動する**: **Agent terminal** ウィンドウで `agent` を起動します。

```bash
../otelcol --config ./agent.yaml
```

**Loadgen を起動する**: **Spans terminal** ウィンドウで、ベースのスパンと併せて `healthz` スパンも送信するフラグを付けて `loadgen` を実行します。
  
```bash
../loadgen -health -count 5
```

**`agent.out` を確認する**: `jq` を使って、`agent` が受信したスパンの名前を確認します。

{{% tabs %}}
{{% tab title="Check spans in agent.out" %}}

```bash
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with name \(.name)"' ./agent.out
```

{{% /tab %}}
{{% tab title="Example output" %}}

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

**Gateway のデバッグ出力を確認する**: `jq` を使って、`gateway` が受信したスパンの名前を確認します。

{{% tabs %}}
{{% tab title="Check spans in gateway-traces.out" %}}

```bash { title="Check spans in gateway-traces.out" }
jq -c '.resourceSpans[].scopeSpans[].spans[] | "Span \(input_line_number) found with name \(.name)"' ./gateway-traces.out
```

{{% /tab %}}
{{% tab title="Example output" %}}

`gateway-metrics.out` ファイルには `/_healthz` という名前のスパンは含まれません。

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

`Filter` プロセッサを使用する際は、入力データの形式を必ず把握し、設定を十分にテストしてください。誤ったデータが破棄されるリスクを下げるために、原則として **可能な限り具体的な設定** を使用してください。

この設定をさらに拡張して、別の属性、タグ、その他の条件に基づいてスパンをフィルタリングすることで、OpenTelemetry Collector を観測ニーズに合わせてよりカスタマイズしやすく、効率的に運用できます。

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止します。

{{% /notice %}}
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
