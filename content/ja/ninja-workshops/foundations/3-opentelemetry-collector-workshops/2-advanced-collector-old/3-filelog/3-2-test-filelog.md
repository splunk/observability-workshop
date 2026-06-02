---
title: 3.2 Test FileLog Receiver
linkTitle: 3.2 Test FileLog Receiver
weight: 4
---

{{% notice title="演習" style="green" icon="running" %}}

**Gateway を起動する**: **Gateway terminal** ウィンドウで `gateway` を起動します。

**Agent を起動する**: **Agent terminal** ウィンドウで `agent` を起動します。

`quotes.log` からのログデータの連続的なストリームが、`agent` と `gateway` のデバッグログに表示されます。

```text { title="Agent/Gateway Debug Output" }
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str(2025-03-06 15:18:32 [ERROR] - There is some good in this world, and it's worth fighting for. LOTR)
Attributes:
     -> log.file.path: Str(quotes.log)
Trace ID:
Span ID:
Flags: 0
LogRecord #1
```

**`loadgen` を停止する**: **Logs terminal** ウィンドウで、`Ctrl-C` を使って `loadgen` を停止します。

**gateway を確認する**: `gateway` が `./gateway-logs.out` ファイルを書き出しているかを確認します。

この時点で、ディレクトリ構造は以下のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.out
├── agent.yaml
├── gateway-logs.out     # Output from the logs pipeline
├── gateway-metrics.out  # Output from the metrics pipeline
├── gateway-traces.out   # Output from the traces pipeline
├── gateway.yaml
└── quotes.log           # File containing Random log lines
```

**ログ行を調べる**: `gateway-logs.out` の中のログ行を、以下のスニペットと比較します。ログエントリに、以前メトリクスやトレースのデータで見たものと同じ属性が含まれていることを確認します。

{{% tabs %}}
{{% tab title="cat /gateway-logs.out" %}}

```json
{"resourceLogs":[{"resource":{"attributes":[{"key":"com.splunk.source","value":{"stringValue":"./quotes.log"}},{"key":"com.splunk.sourcetype","value":{"stringValue":"quotes"}},{"key":"host.name","value":{"stringValue":"workshop-instance"}},{"key":"os.type","value":{"stringValue":"linux"}},{"key":"otelcol.service.mode","value":{"stringValue":"gateway"}}]},"scopeLogs":[{"scope":{},"logRecords":[{"observedTimeUnixNano":"1741274312475540000","body":{"stringValue":"2025-03-06 15:18:32 [DEBUG] - All we have to decide is what to do with the time that is given us. LOTR"},"attributes":[{"key":"log.file.path","value":{"stringValue":"quotes.log"}}],"traceId":"","spanId":""},{"observedTimeUnixNano":"1741274312475560000","body":{"stringValue":"2025-03-06 15:18:32 [DEBUG] - Your focus determines your reality. SW"},"attributes":[{"key":"log.file.path","value":{"stringValue":"quotes.log"}}],"traceId":"","spanId":""}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="cat ./gateway-logs.out | jq" %}}

```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "com.splunk.source",
            "value": {
              "stringValue": "./quotes.log"
            }
          },
          {
            "key": "com.splunk.sourcetype",
            "value": {
              "stringValue": "quotes"
            }
          },
          {
            "key": "host.name",
            "value": {
              "stringValue": "workshop-instance"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "linux"
            }
          },
          {
            "key": "otelcol.service.mode",
            "value": {
              "stringValue": "gateway"
            }
          }
        ]
      },
      "scopeLogs": [
        {
          "scope": {},
          "logRecords": [
            {
              "observedTimeUnixNano": "1741274312475540000",
              "body": {
                "stringValue": "2025-03-06 15:18:32 [DEBUG] - All we have to decide is what to do with the time that is given us. LOTR"
              },
              "attributes": [
                {
                  "key": "log.file.path",
                  "value": {
                    "stringValue": "quotes.log"
                  }
                }
              ],
              "traceId": "",
              "spanId": ""
            },
            {
              "observedTimeUnixNano": "1741274312475560000",
              "body": {
                "stringValue": "2025-03-06 15:18:32 [DEBUG] - Your focus determines your reality. SW"
              },
              "attributes": [
                {
                  "key": "log.file.path",
                  "value": {
                    "stringValue": "quotes.log"
                  }
                }
              ],
              "traceId": "",
              "spanId": ""
            }
          ]
        }
      ],
      "schemaUrl": "https://opentelemetry.io/schemas/1.6.1"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

すべてのログ行に、`"traceId":""` と `"spanId":""` の空のプレースホルダーが含まれていることに気付いたかもしれません。
FileLog receiver は、これらのフィールドがログ行にまだ存在しない場合にのみ、これらを設定します。
たとえば、ログ行が OpenTelemetry のインストルメンテーションライブラリで計装されたアプリケーションによって生成された場合、これらのフィールドはすでに含まれており、上書きされることはありません。

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}
