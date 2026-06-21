---
title: Lambda 関数のデプロイとトレースデータの生成
linkTitle: 6. Lambda 関数の再デプロイ
weight: 6
---

手動インストルメンテーションを関数やサービスに適用してトレースデータをキャプチャする方法がわかったので、Lambda 関数を再度デプロイし、`producer-lambda` エンドポイントにトラフィックを生成しましょう。

新しいディレクトリにいるため、ここでも再度 Terraform を初期化する必要があります。

{{% exercise title="Lambda 関数の再デプロイ" %}}

* 以下のコマンドを実行して `workshop/lambda/manual` ディレクトリに移動します

```bash
cd ~/workshop/lambda/manual
```

* 以下のコマンドを実行して、この新しいディレクトリで Terraform を初期化します

```bash
terraform init
```

それでは、リソースも再度デプロイしましょう！

* **terraform plan** コマンドを実行し、問題がないことを確認します。

```bash
terraform plan
```
  
* 続いて **terraform apply** コマンドを実行し、**main.tf** ファイルから Lambda 関数やその他のサポートリソースをデプロイします

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

ご覧のとおり、base_url の最初の部分とロググループの ARN を除けば、出力はこのワークショップの自動インストルメンテーションのセクションで同じポイントまで実行したときとほぼ同じです。

{{% /exercise %}}

{{% exercise title="`producer-lambda` にトラフィックを送信する" %}}

もう一度、`name` と `superpower` をメッセージとしてエンドポイントに送信します。これにより、トレースコンテキストとともに Kinesis Stream のレコードに追加されます。

* 以下のコマンドを実行して `workshop/lambda/manual` ディレクトリに移動します

```bash
cd ~/workshop/lambda/manual
```

* `send_message.py` スクリプトをバックグラウンドプロセスとして実行します

```bash
nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
```

* 次に、response.logs ファイルの内容を確認して、**producer-lambda** エンドポイントへの呼び出しが成功しているか確認します

```bash
cat response.logs
```

* メッセージが成功した場合、画面に表示される行の中に以下の出力が表示されます

```bash
{"message": "Message placed in the Event Stream: hostname-eventStream"}
```

* 失敗した場合は、以下が表示されます

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

* そして **consumer.logs** ファイルを確認します

```bash
cat consumer.logs
```

ログを注意深く確認してください。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
違いに気づきましたか？
{{% /notice %}}

#### `consumer.logs` ファイルからトレース ID をコピーする

今回は、consumer-lambda ロググループが、伝播した `tracecontext` とともにメッセージを `record` としてログに記録していることがわかります。

トレース ID をコピーするには

* `Kinesis Message` ログの1つを確認します。その中に `data` ディクショナリがあります
* `data` をさらに詳しく見ると、ネストされた `tracecontext` ディクショナリがあります
* `tracecontext` ディクショナリの中に `traceparent` キーバリューペアがあります
* `traceparent` キーバリューペアに、探しているトレース ID が含まれています
  * `-` で区切られた4つのグループの値があります。トレース ID は2番目のグループの文字列です
* **トレース ID をコピーして保存してください。** このワークショップの後のステップで必要になります

![Lambda Consumer Logs, Manual Instruamentation](../images/08-Manual-ConsumerLogs.png)

{{% /exercise %}}
