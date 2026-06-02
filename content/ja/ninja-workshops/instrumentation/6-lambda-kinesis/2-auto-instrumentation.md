---
title: Auto-Instrumentation
linkTitle: 2. Auto-Instrumentation
weight: 2
---

このワークショップの最初のパートでは、OpenTelemetry による auto-instrumentation を使用して、OpenTelemetry Collector が関数の記述言語を自動検出し、それらの関数のトレースの取得を開始する方法を実演します。

### Auto-Instrumentation ワークショップのディレクトリと内容

まず、`workshop/lambda/auto` ディレクトリとそのファイルのいくつかを見てみましょう。ここには、ワークショップの auto-instrumentation 部分のすべてのコンテンツが格納されています。

#### `auto` ディレクトリ

- 次のコマンドを実行して **workshop/lambda/auto** ディレクトリに移動します:

  ```bash
  cd ~/workshop/lambda/auto
  ```

- このディレクトリの内容を確認します:

  ```bash
  ls
  ```

  - _出力には次のファイルとディレクトリが含まれているはずです:_

    ```bash
    handler             outputs.tf          terraform.tf        variables.tf
    main.tf             send_message.py     terraform.tfvars
    ```

  - _出力には次のファイルとディレクトリが含まれているはずです:_

    ```bash
    get_logs.py    main.tf       send_message.py
    handler        outputs.tf    terraform.tf
    ```

#### `main.tf` ファイル

- `main.tf` ファイルの内容を詳しく見てみます:

  ```bash
  cat main.tf
  ```

{{% notice title="Workshop Questions" style="tip" icon="question" %}}

- このテンプレートによってどの AWS リソースが作成されているか分かりますか？
- OpenTelemetry instrumentation がどこで設定されているか分かりますか？
  - _ヒント: lambda 関数の定義をよく確認してください_
- 先ほど設定した環境変数によって、どの instrumentation 情報が提供されているか判別できますか？
{{% /notice %}}

各 lambda 関数の環境変数が設定されているセクションが確認できるはずです。

  ```bash
  environment {
    variables = {
      SPLUNK_ACCESS_TOKEN = var.o11y_access_token
      SPLUNK_REALM = var.o11y_realm
      OTEL_SERVICE_NAME = "producer-lambda"
      OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
      AWS_LAMBDA_EXEC_WRAPPER = "/opt/nodejs-otel-handler"
      KINESIS_STREAM = aws_kinesis_stream.lambda_streamer.name
    }
  }
  ```

これらの環境変数を使用することで、いくつかの方法で auto-instrumentation を構成しています:

- データのエクスポート先となる Splunk Observability Cloud のオーガニゼーションを OpenTelemetry collector に通知するための環境変数を設定しています。

  ```bash
  SPLUNK_ACCESS_TOKEN = var.o11y_access_token
  SPLUNK_ACCESS_TOKEN = var.o11y_realm
  ```

- また、OpenTelemetry が関数/サービスとそれが属する環境/アプリケーションを識別するのに役立つ変数も設定しています。

  ```bash
  OTEL_SERVICE_NAME = "producer-lambda" # consumer-lambda in the case of the consumer function
  OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
  ```

- コード言語に基づいて、関数のハンドラーに適用するラッパーを OpenTelemetry に伝える環境変数を設定しており、これによりトレースデータが自動的に取得されます。

  ```bash
  AWS_LAMBDA_EXEC_WRAPPER - "/opt/nodejs-otel-handler"
  ```

- `producer-lambda` 関数の場合、レコードの送信先となる Kinesis Stream を関数に伝える環境変数を設定しています。

  ```bash
  KINESIS_STREAM = aws_kinesis_stream.lambda_streamer.name
  ```

- これらの値は、Prerequisites セクションで設定した環境変数と、この Terraform 構成ファイルの一部としてデプロイされるリソースから取得されます。

また、各関数に Splunk OpenTelemetry Lambda layer を設定する引数も確認できるはずです。

  ```bash
  layers = var.otel_lambda_layer
  ```

- OpenTelemetry Lambda layer は、Lambda 関数の呼び出し時にテレメトリデータを収集、処理、エクスポートするために必要なライブラリと依存関係を含むパッケージです。

- すべての OpenTelemetry サポート言語のライブラリと依存関係を含む汎用 OTel Lambda layer がある一方で、関数をさらに軽量化するための言語固有の Lambda layer も存在します。
  - _各 AWS リージョンに対応する Splunk OpenTelemetry Lambda layer の ARN (Amazon Resource Name) と最新バージョンは [こちら](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md) で確認できます_

#### `producer.mjs` ファイル

次に、`producer-lambda` 関数のコードを見てみましょう:

- 次のコマンドを実行して `producer.mjs` ファイルの内容を表示します:

  ```bash
  cat ~/workshop/lambda/auto/handler/producer.mjs
  ```

  - この NodeJS モジュールには producer 関数のコードが含まれています。
  - 基本的に、この関数はメッセージを受信し、そのメッセージをレコードとしてターゲットの Kinesis Stream に送信します。

### Lambda 関数のデプロイとトレースデータの生成

`auto` ディレクトリの内容を理解したところで、ワークショップ用のリソースをデプロイし、Lambda 関数からトレースデータを生成できます。

#### `auto` ディレクトリで Terraform を初期化する

`main.tf` ファイルで定義されたリソースをデプロイするには、まずそのファイルと同じフォルダで Terraform が初期化されていることを確認する必要があります。

- `auto` ディレクトリにいることを確認します:

  ```bash
  pwd
  ```

  - _期待される出力は **~/workshop/lambda/auto** です_

- `auto` ディレクトリにいない場合は、次のコマンドを実行します:

  ```bash
  cd ~/workshop/lambda/auto
  ```

- 次のコマンドを実行して、このディレクトリで Terraform を初期化します

  ```bash
  terraform init
  ```

  - このコマンドは、同じフォルダにいくつかの要素を作成します:
    - `.terraform.lock.hcl` ファイル: リソースの提供に使用するプロバイダーを記録します
    - `.terraform` ディレクトリ: プロバイダー構成を保存します
  - 上記のファイルに加えて、terraform を `apply` サブコマンドで実行すると、デプロイされたリソースの状態を追跡するための `terraform.tfstate` ファイルが作成されます。
  - これらにより、`auto` ディレクトリの `main.tf` ファイル内で定義されているとおりに、Terraform がリソースの作成、状態管理、破棄を管理できるようになります。

#### Lambda 関数とその他の AWS リソースをデプロイする

このディレクトリで Terraform を初期化したら、リソースをデプロイできます。

- まず、**terraform plan** コマンドを実行して、Terraform が問題なくリソースを作成できることを確認します。

  ```bash
  terraform plan
  ```

  - _これにより、リソースをデプロイするためのプランが作成され、いくつかのデータが出力されます。これを確認して、すべてが意図したとおりに動作するか確かめることができます。_
  - _プランに表示される値の多くは作成後にしか分からないか、セキュリティ上の理由でマスクされていることに注意してください。_

- 次に、**terraform apply** コマンドを実行して、**main.tf** ファイルから Lambda 関数とその他のサポートリソースをデプロイします:

  ```bash
  terraform apply
  ```

  - _**Enter a value:** プロンプトが表示されたら **yes** と応答してください_

  - 結果として次の出力が得られます:

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

    - _Terraform の出力は **outputs.tf** ファイルで定義されています。_
    - _これらの出力は、ワークショップの他の部分でもプログラム的に使用されます。_

#### `producer-lambda` URL (`base_url`) にトラフィックを送信する

デプロイした Lambda 関数からトレースを取得するには、トラフィックを生成する必要があります。`producer-lambda` 関数のエンドポイントにメッセージを送信し、それが Kinesis Stream にレコードとして配置され、`consumer-lambda` 関数によって Stream から取り出されます。

- `auto` ディレクトリにいることを確認します:

  ```bash
  pwd
  ```

  - _期待される出力は **~/workshop/lambda/auto** です_

- `auto` ディレクトリにいない場合は、次のコマンドを実行します

  ```bash
  cd ~/workshop/lambda/auto
  ```

`send_message.py` スクリプトは、コマンドラインから入力を受け取り、JSON 辞書に追加し、while ループの一部として `producer-lambda` 関数のエンドポイントに繰り返し送信する Python スクリプトです。

- `send_message.py` スクリプトをバックグラウンドプロセスとして実行します
  - _`--name` と `--superpower` 引数が必要です_

  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```

  - メッセージが正常に送信されると、次のような出力が表示されるはずです

    ```bash
    [1] 79829
    user@host manual % appending output to nohup.out
    ```

    - _ここで最も重要な情報は次の 2 つです:_
      - _最初の行のプロセス ID (この例では `79829`)_
      - _`appending output to nohup.out` メッセージ_
    - _`nohup` コマンドは、バックグラウンドに送信されたスクリプトがハングアップしないようにします。また、現在のフォルダと同じフォルダにある nohup.out ファイルにコマンドの curl 出力をキャプチャします。_
    - _`&` は、シェルプロセスにこのプロセスをバックグラウンドで実行するよう指示し、シェルが他のコマンドを実行できるようにします。_

- 次に、`response.logs` ファイルの内容を確認して、`producer-lambda` エンドポイントへのリクエストが成功していることを出力で確認します:

  ```bash
  cat response.logs
  ```

  - メッセージが正常に送信された場合、画面に出力される行の中に次の出力が表示されるはずです:

  ```bash
  {"message": "Message placed in the Event Stream: {prefix}-lambda_stream"}
  ```

  - 失敗した場合は、次のように表示されます:

  ```bash
  {"message": "Internal server error"}
  ```

> [!IMPORTANT]
> このような場合は、ワークショップのファシリテーターに支援を求めてください。

#### Lambda 関数のログを表示する

次に、Lambda 関数のログを見てみましょう。

- **producer-lambda** のログを表示するには、**producer.logs** ファイルを確認します:

  ```bash
  cat producer.logs
  ```

- **consumer-lambda** のログを表示するには、**consumer.logs** ファイルを確認します:

  ```bash
  cat consumer.logs
  ```

ログを注意深く調べてください。

{{% notice title="Workshop Question" style="tip" icon="question" %}}

- OpenTelemetry がロードされているのが見えますか？`splunk-extension-wrapper` の行に注目してください
  - - _`head -n 50 producer.logs` または `head -n 50 consumer.logs` を実行して、**splunk-extension-wrapper** がロードされている様子を確認してみましょう。_

{{% /notice %}}
