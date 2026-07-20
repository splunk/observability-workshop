---
title: Lambda関数のデプロイとトレースデータの生成
linkTitle: 6. Lambda関数の再デプロイ
weight: 6
---

手動計装を関数やサービスに適用してトレースデータをキャプチャする方法がわかったので、Lambda関数を再度デプロイし、`producer-lambda`エンドポイントにトラフィックを送信しましょう。

新しいディレクトリにいるため、ここでもTerraformを初期化する必要があります。

{{% exercise title="Lambda関数の再デプロイ" %}}

* 以下のコマンドを実行して `workshop/lambda/manual` ディレクトリに移動します

```bash
cd ~/workshop/lambda/manual
```

* 以下のコマンドを実行して、この新しいディレクトリでTerraformを初期化します

```bash
terraform init
```

続けてリソースもデプロイしましょう。

* **terraform plan** コマンドを実行し、問題がないことを確認します。

```bash
terraform plan
```
  
* **terraform apply** コマンドを実行して、 **main.tf** ファイルからLambda関数とその他のサポートリソースをデプロイします

```bash
terraform apply
```

* **Enter a value:** プロンプトが表示されたら **yes** と入力します

* 以下のような出力が表示されます

```bash
Outputs:

base_url = "https://______.amazonaws.com/serverless_stage/producer"
consumer_function_name = "_____-consumer"
consumer_log_group_arn = "arn:aws:logs:us-east-1:############:log-group:/aws/lambda/______-consumer"
consumer_log_group_name = "/aws/lambda/______-consumer"
environment = "______-lambda-shop"
lambda_bucket_name = "lambda-shop-______-______"
producer_function_name = "______-producer"
producer_log_group_arn = "arn:aws:logs:us-east-1:############:log-group:/aws/lambda/______-producer"
producer_log_group_name = "/aws/lambda/______-producer"
```

ご覧のとおり、base_urlの最初の部分とロググループARNを除けば、出力はこのワークショップの自動計装パートで同じポイントまで実行したときとほぼ同じです。

{{% /exercise %}}

{{% exercise title="`producer-lambda` にトラフィックを送信する" %}}

もう一度、`name`と`superpower`をメッセージとしてエンドポイントに送信します。これにより、トレースコンテキストとともにKinesis Streamのレコードに追加されます。

* 以下のコマンドを実行して `workshop/lambda/manual` ディレクトリに移動します

```bash
cd ~/workshop/lambda/manual
```

* `send_message.py`スクリプトをバックグラウンドプロセスとして実行します

```bash
nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
```

* 次に、response.logsファイルの内容を確認して、 **producer-lambda** エンドポイントへの呼び出しが成功しているか確認します

```bash
cat response.logs
```

* メッセージが成功した場合、画面に表示される行の中に以下の出力が表示されます

```bash
{"message": "Message placed in the Event Stream: hostname-eventStream"}
```

* 失敗した場合は以下が表示されます

```bash
{"message": "Internal server error"}
```

{{< notice warning >}}
この場合は、ワークショップのファシリテーターに支援を求めてください。
{{< /notice >}}

{{% /exercise %}}

{{% exercise title="ログの確認" %}}

ログがどのようになっているか確認しましょう。

* **producer.logs** ファイルを確認します

```bash
cat producer.logs
```

* **consumer.logs** ファイルも確認します

```bash
cat consumer.logs
```

ログを注意深く確認してください。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
違いに気づきましたか？
{{% /notice %}}

#### `consumer.logs` ファイルからTrace IDをコピーする

今回は、consumer-lambdaロググループが、伝播した `tracecontext` とともにメッセージを `record` として記録していることがわかります。

Trace IDをコピーするには以下の手順を行います

* `Kinesis Message` ログの1つを確認します。その中に `data` ディクショナリがあります
* `data` をよく見ると、ネストされた `tracecontext` ディクショナリがあります
* `tracecontext` ディクショナリの中に `traceparent` のキーと値のペアがあります
* `traceparent` のキーと値のペアに、目的のTrace IDが含まれています
  * `-` で区切られた4つのグループの値があります。Trace IDは2番目のグループの文字列です
* **Trace IDをコピーして保存してください。** このワークショップの後のステップで必要になります

![Lambda Consumer Logs, Manual Instruamentation](../images/08-Manual-ConsumerLogs.png)

{{% /exercise %}}
