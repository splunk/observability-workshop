---
title: 3.2 FileLog Receiver のテスト
linkTitle: 3.2 FileLog Receiver のテスト
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway の起動**: **Gateway ターミナル**ウィンドウで `gateway` を起動します。

**Agent の起動**: **Agent ターミナル**ウィンドウで `agent` を起動します。

`quotes.log` からのログデータが `agent` と `gateway` のデバッグログに継続的に出力されます:

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

**`loadgen` の停止**: **Logs ターミナル**ウィンドウで `Ctrl-C` を使用して `loadgen` を停止します。

**Gateway の確認**: `gateway` が `./gateway-logs.out` ファイルを書き出しているか確認します。

この時点で、ディレクトリ構造は以下のようになります:

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

**ログ行の確認**: `gateway-logs.out` のログ行を以下のスニペットと比較します。ログエントリに、以前メトリクスやトレースデータで確認したものと同じ属性が含まれていることを確認してください:

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

すべてのログ行に `"traceId":""` と `"spanId":""` の空のプレースホルダーが含まれていることにも気づいたかもしれません。
FileLog Receiver は、ログ行にこれらのフィールドがまだ存在しない場合にのみ値を設定します。
例えば、OpenTelemetryの計装ライブラリで計装されたアプリケーションによって生成されたログ行の場合、これらのフィールドはすでに含まれており、上書きされません。

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して `agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}
