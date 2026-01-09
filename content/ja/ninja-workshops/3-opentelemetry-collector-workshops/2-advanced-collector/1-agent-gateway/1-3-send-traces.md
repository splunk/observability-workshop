---
title: 1.3 Agent から Gateway へトレースを送信
linkTitle: 1.3 Send Traces
weight: 4
hidden: true
draft: true
---

{{% notice title="Exercise" style="green" icon="running" %}}

**テストトレースの送信**:

1. **Agent** と **Gateway** がまだ実行中であることを確認します。
2. **Loadgen ターミナル** ウィンドウで、以下のコマンドを実行して5つのスパンを送信し、**Agent** と **Gateway** のデバッグログの出力を確認します：

{{% tabs %}}
{{% tab title="Start the Load Generator" %}}

```bash
../loadgen -count 5
```

{{% /tab %}}
{{% tab title="Agent/Gateway Debug Output" %}}

```text
2025-03-06T11:49:00.456Z        info    Traces  {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
2025-03-06T11:49:00.456Z        info    ResourceSpans #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> service.name: Str(cinema-service)
     -> deployment.environment: Str(production)
     -> host.name: Str(workshop-instance)
     -> os.type: Str(linux)
     -> otelcol.service.mode: Str(agent)
ScopeSpans #0
ScopeSpans SchemaURL:
InstrumentationScope cinema.library 1.0.0
InstrumentationScope attributes:
     -> fintest.scope.attribute: Str(Starwars, LOTR)
Span #0
    Trace ID       : 97fb4e5b13400b5689e3306da7cff077
    Parent ID      :
    ID             : 413358465e5b4f15
    Name           : /movie-validator
    Kind           : Server
    Start time     : 2025-03-06 11:49:00.431915 +0000 UTC
    End time       : 2025-03-06 11:49:01.431915 +0000 UTC
    Status code    : Ok
    Status message : Success
Attributes:
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
     -> payment.amount: Double(87.01)
        {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces"}
```

{{% /tab %}}
{{% /tabs %}}

**Gateway がスパンを処理したことの確認**: Gateway が受信スパンを処理すると、トレースデータを `gateway-traces.out` という名前のファイルに書き込みます。スパンが正常に処理されたことを確認するには、このファイルを検査します。

**Tests ターミナル** で、`jq` コマンドを使用して各スパンの `spanId` やファイル内の位置などの主要な詳細を抽出して表示します。また、**Hostmetrics Receiver** がスパンに追加した属性も抽出できます。

{{% tabs %}}
{{% tab title="Inspect the Gateway Trace File" %}}

```bash
jq -c '.resourceSpans[] as $resource | $resource.scopeSpans[].spans[] | "Span \(input_line_number) found with spanId \(.spanId), hostname \($resource.resource.attributes[] | select(.key == "host.name") | .value.stringValue), os \($resource.resource.attributes[] | select(.key == "os.type") | .value.stringValue)"' ./gateway-traces.out
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
"Span 1 found with spanId d71fe6316276f97d, hostname workshop-instance, os linux"
"Span 2 found with spanId e8d19489232f8c2a, hostname workshop-instance, os linux"
"Span 3 found with spanId 9dfaf22857a6bd05, hostname workshop-instance, os linux"
"Span 4 found with spanId c7f544a4b5fef5fc, hostname workshop-instance, os linux"
"Span 5 found with spanId 30bb49261315969d, hostname workshop-instance, os linux"
```

{{% /tab %}}
{{% /tabs %}}

<!--
> [!IMPORTANT]
> **Agent** と **Gateway** のプロセスを、それぞれのターミナルで `Ctrl-C` を押して停止してください。
-->

{{% /notice %}}
