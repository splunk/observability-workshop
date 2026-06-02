---
title: Lambda 関数のデプロイとトレースデータの生成
linkTitle: 5. Lambda 関数の再デプロイ
weight: 5
---

トレースデータを取得したい関数やサービスに手動インストルメンテーションを適用する方法がわかったので、改めて Lambda 関数をデプロイして、`producer-lambda` エンドポイントに対してトラフィックを生成しましょう。

#### `manual` ディレクトリで Terraform を初期化する

新しいディレクトリにいるので、ここでもう一度 Terraform を初期化する必要があります。

- `manual` ディレクトリにいることを確認します:

  ```bash
  pwd
  ```

  - _期待される出力は **~/workshop/lambda/manual** です_

- `manual` ディレクトリにいない場合は、次のコマンドを実行します:

  ```bash
  cd ~/workshop/lambda/manual
  ```

- 次のコマンドを実行して、このディレクトリで Terraform を初期化します

  ```bash
  terraform init
  ```

#### Lambda 関数とその他の AWS リソースをデプロイする

それでは、これらのリソースを再度デプロイしましょう！

- **terraform plan** コマンドを実行し、問題がないことを確認します。

  ```bash
  terraform plan
  ```
  
- 続けて **terraform apply** コマンドを実行し、**main.tf** ファイルから Lambda 関数とその他のサポートリソースをデプロイします:

  ```bash
  terraform apply
  ```

  - _**Enter a value:** プロンプトが表示されたら **yes** と回答します_

  - 次のような出力が得られます:

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

ご覧のとおり、base_url の最初の部分とロググループ ARN を除けば、出力はこのワークショップの自動インストルメンテーションのセクションで同じところまで実行したときとほぼ同じになるはずです。

#### `producer-lambda` エンドポイント (base_url) にトラフィックを送信する

もう一度、`name` と `superpower` をメッセージとしてエンドポイントに送信します。これによりトレースコンテキストとともに Kinesis Stream のレコードに追加されます。

- `manual` ディレクトリにいることを確認します:

  ```bash
  pwd
  ```

  - _期待される出力は **~/workshop/lambda/manual** です_

- `manual` ディレクトリにいない場合は、次のコマンドを実行します:

  ```bash
  cd ~/workshop/lambda/manual
  ```

- `send_message.py` スクリプトをバックグラウンドプロセスとして実行します:

  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```

- 次に、response.logs ファイルの内容を確認し、**producer-lambda** エンドポイントへの呼び出しが成功しているか確認します:

  ```bash
  cat response.logs
  ```

  - メッセージが成功した場合、画面に表示される行の中に次のような出力が見えるはずです:

    ```bash
    {"message": "Message placed in the Event Stream: hostname-eventStream"}
    ```

  - 失敗した場合は、次のように表示されます:

    ```bash
    {"message": "Internal server error"}
    ```

> [!IMPORTANT]
> このような場合は、ワークショップのファシリテーターのいずれかに支援を求めてください。

#### Lambda 関数のログを表示する

ログがどのようになっているか確認しましょう。

- **producer.logs** ファイルを確認します:

  ```bash
  cat producer.logs
  ```

- そして **consumer.logs** ファイルを確認します:

  ```bash
  cat consumer.logs
  ```

ログを注意深く調べてください。

##### _ワークショップの質問_

> 違いに気づきましたか？

#### `consumer.logs` ファイルから Trace ID をコピーする

今回は、consumer-lambda ロググループが、伝播した `tracecontext` とともにメッセージを `record` として記録していることがわかります。

Trace ID をコピーするには:

- `Kinesis Message` ログのいずれかを確認します。その中に `data` ディクショナリがあります
- `data` をさらに詳しく見ると、ネストされた `tracecontext` ディクショナリがあります
- `tracecontext` ディクショナリ内には、`traceparent` キーと値のペアがあります
- `traceparent` キーと値のペアには、私たちが探している Trace ID が含まれています
  - `-` で区切られた 4 つの値のグループがあります。Trace ID は 2 番目のグループの文字列です
- **Trace ID をコピーして保存してください。** このワークショップの後のステップで必要になります

![Lambda Consumer Logs, Manual Instruamentation](../images/08-Manual-ConsumerLogs.png)
