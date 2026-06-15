---
title: Auto-Instrumentation
linkTitle: 2. Auto-Instrumentation
weight: 2
---

## Auto-Instrumentation

自動計装コードが含まれる auto ディレクトリに移動します。

{{< tabs >}} {{% tab title="Command" %}}

```
cd ~/o11y-lambda-lab/auto
```

{{% /tab %}} {{< /tabs >}}

このディレクトリ内のファイルの内容を確認します。serverless.yml テンプレートを見てみましょう。

{{< tabs >}} {{% tab title="Command" %}}

```
cat serverless.yml
```

{{% /tab %}} {{< /tabs >}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}

* このテンプレートによって作成される AWS エンティティを特定できますか？
* OpenTelemetry の計装がどこで設定されているか特定できますか？
* 環境変数によって提供されている計装情報を判別できますか？

{{% /notice %}}

各関数に Splunk OpenTelemetry Lambda レイヤーが追加されていることが確認できるはずです。

```
layers:
      - arn:aws:lambda:us-east-1:254067382080:layer:splunk-apm:70
```

各 AWS リージョンの関連するレイヤー ARN（Amazon Resource Name）と最新バージョンはこちらで確認できます: <https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md>

環境変数が設定されているセクションも確認できるはずです。

```
environment:
  AWS_LAMBDA_EXEC_WRAPPER: /opt/nodejs-otel-handler
  OTEL_RESOURCE_ATTRIBUTES: deployment.environment=${self:custom.prefix}-apm-lambda
  OTEL_SERVICE_NAME: consumer-lambda
  SPLUNK_ACCESS_TOKEN: ${self:custom.accessToken}
  SPLUNK_REALM: ${self:custom.realm}
```

環境変数を使用して、自動計装の設定とエンリッチメントを行っています。

ここでは、Splunk APM Layer 内の NodeJS ラッパーの場所、環境名、サービス名、Splunk Org の認証情報など、最小限の情報を提供しています。トレースデータは Splunk Observability Cloud に直接送信しています。代わりに、Gateway モードで設定された OpenTelemetry Collector にトレースをエクスポートすることもできます。

関数コードを確認してみましょう。

{{< tabs >}} {{% tab title="Command" %}}

```
cat handler.js
```

{{% /tab %}} {{< /tabs >}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}

* producer 関数のコードを特定できますか？
* consumer 関数のコードを特定できますか？
{{% /notice %}}

コード内に Splunk や OpenTelemetry への言及がないことに注目してください。計装は Lambda レイヤーと環境変数のみを使用して追加しています。

## Lambda のデプロイ

以下のコマンドを実行して Lambda Functions をデプロイします:

{{< tabs >}} {{% tab title="Deploy Command" %}}

```
sls deploy
```

{{% /tab %}} {{% tab title="Expected Output" %}}

```
Deploying hostname-lambda-lab to stage dev (us-east-1)
...
...
endpoint: POST - https://randomstring.execute-api.us-east-1.amazonaws.com/dev/producer
functions:
  producer: hostname-lambda-lab-dev-producer (1.6 kB)
  consumer: hostname-lambda-lab-dev-consumer (1.6 kB)
```

{{% /tab %}} {{< /tabs >}}

このコマンドは serverless.yml テンプレートの指示に従って、Lambda 関数と Kinesis ストリームを作成します。実行には1〜2分かかる場合があります。

{{% notice style="note" %}} serverless.yml は実際には CloudFormation テンプレートです。CloudFormation は AWS の Infrastructure as Code サービスです。詳細はこちらをご覧ください - <https://aws.amazon.com/cloudformation/> {{% /notice %}}

サーバーレス関数の詳細を確認します:

{{< tabs >}} {{% tab title="Command" %}}

```
sls info
```

{{% /tab %}} {{< /tabs >}}

エンドポイントの値をメモしてください:
![2-auto-1-endpoint-value](../images/2-auto-1-endpoint-value.png)

## トラフィックの送信

curl コマンドを使用して producer 関数にペイロードを送信します。コマンドオプション -d の後にメッセージペイロードを指定します。

name の値をあなたの名前に変更し、Lambda 関数にあなたの超能力を伝えてみてください。YOUR_ENDPOINT を前のステップで取得したエンドポイントに置き換えてください。

{{< tabs >}} {{% tab title="Command" %}}

```
curl -d '{ "name": "CHANGE_ME", "superpower": "CHANGE_ME" }' YOUR_ENDPOINT
```

{{% /tab %}} {{< /tabs >}}

例:

```
curl -d '{ "name": "Kate", "superpower": "Distributed Tracing" }' https://xvq043lj45.execute-api.us-east-1.amazonaws.com/dev/producer
```

メッセージが正常に送信された場合、以下の出力が表示されます:

```
{"message":"Message placed in the Event Stream: hostname-eventSteam"}
```

失敗した場合は、以下が表示されます:

```
{"message": "Internal server error"}
```

この場合は、ラボのファシリテーターに支援を依頼してください。

成功メッセージが表示されたら、さらに負荷を生成します: そのメッセージを5回以上再送信してください。送信するたびに成功メッセージが表示されるはずです。

Lambda のログ出力を確認します:

Producer 関数のログ:

{{< tabs >}} {{% tab title="Producer Function Logs" %}}

```
sls logs -f producer
```

{{% /tab %}} {{< /tabs >}}

Consumer 関数のログ:

{{< tabs >}} {{% tab title="Consumer Function Logs" %}}

```
sls logs -f consumer
```

{{% /tab %}} {{< /tabs >}}

ログを注意深く確認してください。

{{% notice title="Workshop Question" style="tip" icon="question" %}}
OpenTelemetry がロードされていることが確認できますか？splunk-extension-wrapper を含む行に注目してください。
{{% /notice %}}
