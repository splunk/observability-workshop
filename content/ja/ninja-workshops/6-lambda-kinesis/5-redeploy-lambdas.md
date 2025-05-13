---
title: Lambda関数のデプロイとトレースデータの生成
linkTitle: 5. Lambda関数の再デプロイ
weight: 5
---

トレースデータを収集したい関数やサービスに手動計装を適用する方法がわかったので、Lambda関数を再度デプロイして、`producer-lambda`エンドポイントに対するトラフィックを生成していきましょう。

#### `manual` ディレクトリでTerraformを初期化する

新しいディレクトリにいるので、ここでもう一度Terraformを初期化する必要があります。

- `manual` ディレクトリにいることを確認します：

  ```bash
  pwd
  ```

  - _予想される出力は **~/o11y-lambda-workshop/manual** です_

- `manual` ディレクトリにいない場合は、次のコマンドを実行します：

  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- 次のコマンドを実行して、このディレクトリでTerraformを初期化します：

  ```bash
  terraform init
  ```

#### Lambda関数とその他のAWSリソースをデプロイする

それでは、これらのリソースを再度デプロイしましょう！

- 問題がないことを確認するために、**terraform plan** コマンドを実行します。
  ```bash
  terraform plan
  ```
  
- 続いて、**terraform apply** コマンドを使用して **main.tf** ファイルからLambda関数とその他のサポートリソースをデプロイします：
  ```bash
  terraform apply
  ```
  - _**Enter a value:** プロンプトが表示されたら **yes** と応答します_

  - これにより、以下のような出力が得られます：
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

見ての通り、base_urlの最初の部分とログループARN以外は、このワークショップの自動計装部分をこの同じ時点まで実行したときと出力は概ね同じはずです。

#### `producer-lambda` エンドポイント (base_url) にトラフィックを送信する

もう一度、`name` と `superpower` をメッセージとしてエンドポイントに送信します。これはトレースコンテキストとともに、Kinesisストリーム内のレコードに追加されます。

- `manual` ディレクトリにいることを確認します：

  ```bash
  pwd
  ```

  - _予想される出力は **~/o11y-lambda-workshop/manual** です_

- `manual` ディレクトリにいない場合は、次のコマンドを実行します：

  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- `send_message.py` スクリプトをバックグラウンドプロセスとして実行します：

  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```

- 次に、response.logsファイルの内容を確認して、**producer-lambda**エンドポイントへの呼び出しが成功しているか確認します：
  ```bash
  cat response.logs
  ```
  - メッセージが成功していれば、画面に表示される行の中に次の出力が表示されるはずです：

    ```bash
    {"message": "Message placed in the Event Stream: hostname-eventStream"}
    ```

  - 失敗した場合は、次のように表示されます：

    ```bash
    {"message": "Internal server error"}
    ```

> [!IMPORTANT]
> これが発生した場合は、ワークショップ進行役の一人に支援を求めてください。

#### Lambda関数のログの確認

ログがどのようになっているか見てみましょう。

- **producer.logs** ファイルを確認します：
  ```bash
  cat producer.logs
  ```

- そして **consumer.logs** ファイルを確認します：
  ```bash
  cat consumer.logs
  ```

ログを注意深く調べてください。

##### _ワークショップの質問_

> 違いに気づきましたか？

#### `consumer-lambda` ログからのトレース ID のコピー

今回は、consumer-lambdaのロググループが、我々が伝播した`tracecontext`とともに、メッセージを`record`としてログに記録しているのが確認できます。

トレース ID をコピーするには：

- `Kinesis Message`ログの1つを見てみましょう。その中には`data`ディクショナリがあります
- ネストされた`tracecontext`ディクショナリを見るために、`data`をより詳しく見てください
- `tracecontext`ディクショナリ内には、`traceparent`というキーと値のペアがあります
- `traceparent`キーと値のペアには、私たちが探しているトレース IDが含まれています
  - `-`で区切られた4つの値のグループがあります。トレース IDは2番目の文字グループです
- **トレース IDをコピーして保存してください。** このワークショップの後のステップで必要になります

![Lambda Consumer Logs、手動計装](../images/08-Manual-ConsumerLogs.png)
