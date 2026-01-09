---
title: 5.3 Test Transform Processor
linkTitle: 5.3 Test Transform Processor
weight: 3
---

このテストでは、**Agent** によってエクスポートされる前に、`com.splunk/source` と `os.type` のメタデータがログリソース属性から **削除** されていることを確認します。さらに、このテストでは以下を確認します：

1. 重大度情報を抽出するためにログ本文がパースされていること
   - `SeverityText` と `SeverityNumber` が `LogRecord` に設定されていること
2. ログ本文の JSON フィールドがログ `attributes` に昇格していること

これにより、エクスポート前に適切なメタデータフィルタリング、重大度マッピング、および構造化ログのエンリッチメントが行われることが保証されます。

{{% notice title="Exercise" style="green" icon="running" %}}

**デバッグ出力を確認する**: **Agent** と **Gateway** の両方で、`com.splunk/source` と `os.type` が削除されていることを確認します：

{{% tabs %}}
{{% tab title="Gateway Debug Output" %}}

  ```text
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(workshop-instance)
     -> otelcol.service.mode: Str(agent)
  ```

{{% /tab %}}
{{% tab title="Agent Debug Output" %}}

  ```text
Resource attributes:
     -> com.splunk.source: Str(./quotes.log)
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(workshop-instance)
     -> os.type: Str(linux)
     -> otelcol.service.mode: Str(agent)
  ```

{{% /tab %}}
{{% /tabs %}}

**Agent** と **Gateway** の両方で、`LogRecord` の `SeverityText` と `SeverityNumber` がログ本文の重大度 `level` で定義されていることを確認します。また、本文の JSON フィールドがトップレベルのログ `Attributes` としてアクセスできることを確認します：

{{% tabs %}}
{{% tab title="Gateway Debug Output" %}}

```text
<snip>
SeverityText: WARN
SeverityNumber: Warn(13)
Body: Str({"level":"WARN","message":"Your focus determines your reality.","movie":"SW","timestamp":"2025-03-07 11:17:26"})
Attributes:
     -> log.file.path: Str(quotes.log)
     -> level: Str(WARN)
     -> message: Str(Your focus determines your reality.)
     -> movie: Str(SW)
     -> timestamp: Str(2025-03-07 11:17:26)
</snip>
```

{{% /tab %}}
{{% tab title="Agemt Debug Output" %}}

```text
<snip>
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str({"level":"WARN","message":"Your focus determines your reality.","movie":"SW","timestamp":"2025-03-07 11:17:26"})
Attributes:
     -> log.file.path: Str(quotes.log)
</snip>
```

{{% /tab %}}
{{% /tabs %}}

**ファイル出力を確認する**: 新しい `gateway-logs.out` ファイルでデータが変換されていることを確認します：

{{% tabs %}}
{{% tab title="jq Query" %}}

```bash
jq '[.resourceLogs[].scopeLogs[].logRecords[] | {severityText, severityNumber, body: .body.stringValue}]' gateway-logs.out
```

{{% /tabs %}}
{{% tab title="Example Output" %}}

```json
[
  {
    "severityText": "DEBUG",
    "severityNumber": 5,
    "body": "{\"level\":\"DEBUG\",\"message\":\"All we have to decide is what to do with the time that is given us.\",\"movie\":\"LOTR\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  },
  {
    "severityText": "WARN",
    "severityNumber": 13,
    "body": "{\"level\":\"WARN\",\"message\":\"The Force will be with you. Always.\",\"movie\":\"SW\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  },
  {
    "severityText": "ERROR",
    "severityNumber": 17,
    "body": "{\"level\":\"ERROR\",\"message\":\"One does not simply walk into Mordor.\",\"movie\":\"LOTR\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  },
  {
    "severityText": "DEBUG",
    "severityNumber": 5,
    "body": "{\"level\":\"DEBUG\",\"message\":\"Do or do not, there is no try.\",\"movie\":\"SW\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  }
]
[
  {
    "severityText": "ERROR",
    "severityNumber": 17,
    "body": "{\"level\":\"ERROR\",\"message\":\"There is some good in this world, and it's worth fighting for.\",\"movie\":\"LOTR\",\"timestamp\":\"2025-03-07 11:56:29\"}"
  }
]
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止してください。
