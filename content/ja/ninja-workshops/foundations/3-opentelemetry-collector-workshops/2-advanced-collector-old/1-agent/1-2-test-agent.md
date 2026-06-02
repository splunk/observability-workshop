---
title: 1.2 Test Agent Configuration
linkTitle: 1.2 Test Agent Configuration
weight: 2
---

新しく作成した `agent.yaml` を使って OpenTelemetry Collector を起動する準備が整いました。この演習では、OpenTelemetry Collector を通じてデータがどのように流れていくのかを理解するための基礎を築きます。

{{% notice title="演習" style="green" icon="running" %}}

**Agent を起動する**: **Agent terminal** ウィンドウで次のコマンドを実行します。

```bash { title="Start Collector" }
../otelcol --config=agent.yaml
```

**デバッグ出力を確認する**: すべてが正しく構成されていれば、出力の最初と最後の行は次のようになります。

```text
2025/01/13T12:43:51 settings.go:478: Set config to [agent.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.120.0/service.go:261 Everything is ready. Begin running and processing data.
```

**テスト用 Span を送信する**: アプリケーションを計装する代わりに、`loadgen` ツールを使って OpenTelemetry Collector へトレースデータを送信する動作をシミュレートします。

**Spans terminal** ウィンドウで `1-agent` ディレクトリに移動し、次のコマンドを実行して Span を 1 件送信します。

{{% tabs %}}
{{% tab title="Start Load Generator" %}}

```bash
../loadgen -count 1
```

{{% /tab %}}
{{% tab title="Load Generator Output" %}}

```text
Sending traces. Use Ctrl-C to stop.
Response: {"partialSuccess":{}}

Base trace sent with traceId: 1aacb1db8a6d510f10e52f154a7fdb90 and spanId: 7837a3a2d3635d9f
 ```

`{"partialSuccess":{}}`: `partialSuccess` フィールドが空であるため、100% 成功したことを示しています。一部が失敗した場合は、このフィールドに失敗した部分の詳細が含まれます。

{{% /tab %}}
{{% /tabs %}}

**デバッグ出力を確認する**:

**Agent terminal** ウィンドウで Collector のデバッグ出力を確認します。

```text
2025-03-06T10:11:35.174Z        info    Traces  {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
2025-03-06T10:11:35.174Z        info    ResourceSpans #0
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
    Trace ID       : 0ef4daa44a259a7199a948231bc383c0
    Parent ID      :
    ID             : e8fdd442c36cbfb1
    Name           : /movie-validator
    Kind           : Server
    Start time     : 2025-03-06 10:11:35.163557 +0000 UTC
    End time       : 2025-03-06 10:11:36.163557 +0000 UTC
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
     -> payment.amount: Double(86.48)
        {"otelcol.component.id": "debug", "otelcol.component.kind": "Exporter", "otelcol.signal": "traces"}
```

> [!IMPORTANT]
> **Agent terminal** ウィンドウで `Ctrl-C` を使って `agent` を停止します。

{{% /notice %}}
