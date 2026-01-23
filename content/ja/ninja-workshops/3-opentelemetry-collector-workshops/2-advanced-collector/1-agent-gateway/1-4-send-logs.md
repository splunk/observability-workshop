---
title: 1.4 ログの送信
linkTitle: 1.4 Send Logs
weight: 5
hidden: true
draft: true
---

{{% notice title="Exercise" style="green" icon="running" %}}

**ログ Load Generator の起動:** **Loadgen ターミナル** ウィンドウで、以下のコマンドを実行して `loadgen` を起動します

```bash
../loadgen -logs
```

`quotes.log` からの継続的なログデータストリームが **Agent** と **Gateway** のデバッグログに表示されます

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

**`loadgen` の停止**: **Loadgen ターミナル** ウィンドウで、`Ctrl-C` を使用して `loadgen` を停止します。

**Gateway の確認**: **Gateway** が `./gateway-logs.out` ファイルを書き込んだか確認します。

この時点で、ディレクトリ構造は以下のようになります

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

**ログ行の検査**: `gateway-logs.out` 内のログ行を以下のスニペットと比較します。ログエントリに、以前メトリクスとトレースデータで確認したのと同じ属性が含まれていることを確認します

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

すべてのログ行に `"traceId":""` と `"spanId":""` の空のプレースホルダーが含まれていることにお気づきかもしれません。
FileLog Receiver は、ログ行にこれらのフィールドがまだ存在しない場合にのみ、これらのフィールドを入力します。
例えば、ログ行が OpenTelemetry 計装ライブラリで計装されたアプリケーションによって生成された場合、これらのフィールドはすでに含まれており、上書きされません。

> [!IMPORTANT]
> **Agent** と **Gateway** のプロセスを、それぞれのターミナルで `Ctrl-C` を押して停止してください。

{{% /notice %}}
