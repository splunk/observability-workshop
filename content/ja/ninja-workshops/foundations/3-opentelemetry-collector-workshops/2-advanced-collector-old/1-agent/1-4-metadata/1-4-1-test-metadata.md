---
title: 1.4.1 リソースメタデータのテスト
linkTitle: 1.4.1 リソースメタデータのテスト
weight: 1
---
{{% notice title="演習" style="green" icon="running" %}}

**Agent を再起動する**: **Agent ターミナル** ウィンドウで、変更内容をテストするために更新された設定を使って `agent` を再起動します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

すべてが正しくセットアップされていれば、出力の最後の行で collector が稼働していることが確認できるはずです。

```text
  2025-01-13T12:43:51.747+0100 info service@v0.120.0/service.go:261 Everything is ready. Begin running and processing data.
```

**トレースを送信する**: **Spans ターミナル** ウィンドウから（`1-agent` ディレクトリにいることを確認したうえで）、`loadgen` バイナリで再度 span を送信し、新しい `agent.out` を作成します。

```bash { title="Start Load Generator" }
../loadgen
```

**Agent のデバッグ出力を確認する**: `resource attributes` セクションに 3 つの新しい行（`host.name`、`os.type`、`otelcol.service.mode`）が表示されているはずです。

```text
<snip>
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
    -> service.name: Str(cinema.service)
    -> deployment.environment: Str(production)
    -> host.name: Str([MY_HOST_NAME])
    -> os.type: Str([MY_OS])
    -> otelcol.service.mode: Str(agent)
</snip>
```

**メタデータが span に追加されていることを確認する**: `Ctrl-C` で `loadgen` を停止します。新しい `agent.out` ファイルで以下を確認します。

1. `resourceSpans` セクションに `otelcol.service.mode` 属性が存在し、その値が `agent` であることを確認します。
2. `resourcedetection` の属性（`host.name` と `os.type`）も存在することを確認します。

これらの値は、パイプラインに設定された processor によって、お使いのデバイスに基づいて自動的に追加されます。

{{% tabs %}}
{{% tab title="cat ./agent.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"cinema-service"}},{"key":"deployment.environment","value":{"stringValue":"production"}},{"key":"host.name","value":{"stringValue":"RCASTLEY-M-YQRY.local"}},{"key":"os.type","value":{"stringValue":"darwin"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"cinema.library","version":"1.0.0","attributes":[{"key":"fintest.scope.attribute","value":{"stringValue":"Starwars, LOTR"}}]},"spans":[{"traceId":"ae921957a4d93fa11cee640cd7908eb8","spanId":"f6b0f29825efe585","parentSpanId":"","name":"/movie-validator","kind":2,"startTimeUnixNano":"1740994347431796000","endTimeUnixNano":"1740994348431796000","attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR>StarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}],"status":{"message":"Success","code":1}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
```

{{% /tab %}}
{{% tab title="cat ./agent.out | jq" %}}

```json
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": {
              "stringValue": "cinema-service"
            }
          },
          {
            "key": "deployment.environment",
            "value": {
              "stringValue": "production"
            }
          },
          {
            "key": "host.name",
            "value": {
              "stringValue": "RCASTLEY-M-YQRY.local"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "darwin"
            }
          },
          {
            "key": "otelcol.service.mode",
            "value": {
              "stringValue": "agent"
            }
          }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "cinema.library",
            "version": "1.0.0",
            "attributes": [
              {
                "key": "fintest.scope.attribute",
                "value": {
                  "stringValue": "Starwars, LOTR"
                }
              }
            ]
          },
          "spans": [
            {
              "traceId": "ab984cd113463aa919ac200751fcfc1d",
              "spanId": "db651e116290a8f2",
              "parentSpanId": "",
              "name": "/movie-validator",
              "kind": 2,
              "startTimeUnixNano": "1740994462515044000",
              "endTimeUnixNano": "1740994463515044000",
              "attributes": [
                {
                  "key": "user.name",
                  "value": {
                    "stringValue": "George Lucas"
                  }
                },
                {
                  "key": "user.phone_number",
                  "value": {
                    "stringValue": "+1555-867-5309"
                  }
                },
                {
                  "key": "user.email",
                  "value": {
                    "stringValue": "george@deathstar.email"
                  }
                },
                {
                  "key": "user.account_password",
                  "value": {
                    "stringValue": "LOTR>StarWars1-2-3"
                  }
                },
                {
                  "key": "user.visa",
                  "value": {
                    "stringValue": "4111 1111 1111 1111"
                  }
                },
                {
                  "key": "user.amex",
                  "value": {
                    "stringValue": "3782 822463 10005"
                  }
                },
                {
                  "key": "user.mastercard",
                  "value": {
                    "stringValue": "5555 5555 5555 4444"
                  }
                }
              ],
              "status": {
                "message": "Success",
                "code": 1
              }
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

> [!IMPORTANT]
> それぞれのターミナルウィンドウで `Ctrl-C` を使って `agent` プロセスと `loadgen` プロセスを停止します。

{{% /notice %}}
