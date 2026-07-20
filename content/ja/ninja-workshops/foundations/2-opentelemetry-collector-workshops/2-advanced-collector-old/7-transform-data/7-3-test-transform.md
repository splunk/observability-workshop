---
title: 7.3 Transform Processorのテスト
linkTitle: 7.3 Transform Processorのテスト
weight: 3
---

このテストでは、`com.splunk/source`と`os.type`のメタデータが`agent`によるエクスポート前にログのリソース属性から **削除** されていることを検証します。さらに、以下を確認します。

1. ログ本文が解析され、重大度情報が抽出されていること。
   - `SeverityText`と`SeverityNumber`が`LogRecord`に設定されていること。
2. ログ本文のJSONフィールドがログの`attributes`に昇格されていること。

これにより、エクスポート前に適切なメタデータフィルタリング、重大度マッピング、および構造化ログのエンリッチメントが行われていることを確認します。

{{% notice title="エクササイズ" style="green" icon="running" %}}

**デバッグ出力の確認**: `agent`と`gateway`の両方で、`com.splunk/source`と`os.type`が削除されていることを確認します。

{{% tabs %}}
{{% tab title="新しいデバッグ出力" %}}

  ```text
Resource attributes:
     -> com.splunk.sourcetype: Str(quotes)
     -> host.name: Str(workshop-instance)
     -> otelcol.service.mode: Str(agent)
  ```

{{% /tab %}}
{{% tab title="元のデバッグ出力" %}}

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

`agent`と`gateway`の両方で、`LogRecord`の`SeverityText`と`SeverityNumber`がログ本文の重大度`level`で定義されていることを確認します。本文のJSONフィールドがトップレベルのログ`Attributes`としてアクセスできることを確認します。

{{% tabs %}}
{{% tab title="新しいデバッグ出力" %}}

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
{{% tab title="元のデバッグ出力" %}}

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

**ファイル出力の確認**: 新しい`gateway-logs.out`ファイルでデータが変換されていることを確認します。

{{% tabs %}}
{{% tab title="jq Query" %}}

```bash
jq '[.resourceLogs[].scopeLogs[].logRecords[] | {severityText, severityNumber, body: .body.stringValue}]' gateway-logs.out
```

{{% /tabs %}}
{{% tab title="出力例" %}}

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

> [!IMPORTANT]
> それぞれのターミナルで`Ctrl-C`を押して、`agent`と`gateway`のプロセスを停止してください。

{{% /notice %}}
