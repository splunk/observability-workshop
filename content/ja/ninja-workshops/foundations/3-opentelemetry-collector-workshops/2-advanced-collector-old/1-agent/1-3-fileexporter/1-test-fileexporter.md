---
title: 1.3.1 File Exporter のテスト
linkTitle: 1.3.1 File Exporter のテスト
weight: 1
---

{{% notice title="演習" style="green" icon="running" %}}

**Agent を再起動する**: **Agent ターミナル** ウィンドウを開き、変更した構成を使って `agent` を (再) 起動します。

{{% tabs %}}
{{% tab title="Start the Agent" %}}

```bash
../otelcol --config=agent.yaml
```

{{% /tab %}}
{{% tab title="Agent Output" %}}

```text
2025-01-13T12:43:51.747+0100 info service@v0.120.0/service.go:261 Everything is ready. Begin running and processing data.
```

{{% /tab %}}
{{% /tabs %}}

**トレースを送信する**: **Spans ターミナル** ウィンドウから別のスパンを送信し、これまでと同じ出力がコンソールに表示されることを確認します。

```bash { title="Start Load Generator" }
../loadgen -count 1
```

ここで **Agent ターミナル** ウィンドウの `agent` を `Ctrl-C` で停止し、`agent.out` ファイルが書き出されたことを確認できるようにします。

**`agent.out` ファイルが書き出されたことを確認する**: 現在のディレクトリに `agent.out` という名前のファイルが書き出されているか確認します。

```text { title="Updated Directory Structure" }
.
├── agent.out    # OTLP/Json output created by the File Exporter
└── agent.yaml
```

**スパンの形式を確認する**:

1. File Exporter が `agent.out` にスパンを書き出す際に使用する形式を確認します。
2. 出力は **OTLP/JSON** 形式の 1 行になります。
3. `agent.out` の内容を表示するには、`cat ./agent.out` コマンドを使用できます。より読みやすい整形済みの表示にするには、`cat ./agent.out | jq` のように `jq` に出力をパイプしてください。

{{% tabs %}}
{{% tab title="cat ./agent.out" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"cinema-service"}},{"key":"deployment.environment","value":{"stringValue":"production"}},{"key":"host.name","value":{"stringValue":"workshop-instance"}},{"key":"os.type","value":{"stringValue":"linux"}},{"key":"otelcol.service.mode","value":{"stringValue":"agent"}}]},"scopeSpans":[{"scope":{"name":"cinema.library","version":"1.0.0","attributes":[{"key":"fintest.scope.attribute","value":{"stringValue":"Starwars, LOTR"}}]},"spans":[{"traceId":"d824a28db5aa5f5a3011f19c452e5af0","spanId":"ab4cde146f77eacf","parentSpanId":"","name":"/movie-validator","kind":2,"startTimeUnixNano":"1741256991405300000","endTimeUnixNano":"1741256992405300000","attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.password","value":{"stringValue":"LOTR>StarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}},{"key":"payment.amount","value":{"doubleValue":56.24}}],"status":{"message":"Success","code":1}}]}],"schemaUrl":"https://opentelemetry.io/schemas/1.6.1"}]}
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
              "traceId": "d824a28db5aa5f5a3011f19c452e5af0",
              "spanId": "ab4cde146f77eacf",
              "parentSpanId": "",
              "name": "/movie-validator",
              "kind": 2,
              "startTimeUnixNano": "1741256991405300000",
              "endTimeUnixNano": "1741256992405300000",
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
                  "key": "user.password",
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
                },
                {
                  "key": "payment.amount",
                  "value": {
                    "doubleValue": 56.24
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

{{% /notice %}}
