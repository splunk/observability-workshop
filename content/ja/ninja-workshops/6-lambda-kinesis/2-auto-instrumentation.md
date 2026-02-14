---
title: 自動計装
linkTitle: 2. 自動計装
weight: 2
---

ワークショップの最初の部分では、OpenTelemetryによる自動計装がどのようにしてOpenTelemetry Collectorに関数がどの言語で書かれているかを自動検出させ、それらの関数のトレースの取得を開始させるかを示します。

### 自動計装ワークショップディレクトリとコンテンツ

まず、`o11y-lambda-workshop/auto` ディレクトリとそのファイルの一部を見てみましょう。ここにはワークショップの自動計装部分のすべてのコンテンツがあります。

#### `auto` ディレクトリ

- 以下のコマンドを実行して **o11y-lambda-workshop/auto** ディレクトリに移動します：

  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- このディレクトリの内容を確認します：

  ```bash
  ls
  ```

  - _出力には以下のファイルとディレクトリが含まれるはずです：_

    ```bash
    handler             outputs.tf          terraform.tf        variables.tf
    main.tf             send_message.py     terraform.tfvars
    ```

  - _出力には以下のファイルとディレクトリが含まれるはずです：_

    ```bash
    get_logs.py    main.tf       send_message.py
    handler        outputs.tf    terraform.tf
    ```

#### `main.tf` ファイル

- `main.tf` ファイルをより詳しく見てみましょう：

  ```bash
  cat main.tf
  ```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

- このテンプレートによってどのAWSリソースが作成されているか特定できますか？
- OpenTelemetry計装がどこでセットアップされているか特定できますか？
  - _ヒント: Lambda 関数の定義を調べてください_
- 以前に設定した環境変数によってどの計装情報が提供されているか判断できますか？
  {{% /notice %}}

各Lambda関数の環境変数が設定されているセクションが見つかるはずです。

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

これらの環境変数を使用することで、いくつかの方法で自動計装を構成しています：

- 環境変数を設定して、データのエクスポート先となるSplunk Observability Cloud組織をOpenTelemetry collectorに伝えています。

  ```bash
  SPLUNK_ACCESS_TOKEN = var.o11y_access_token
  SPLUNK_ACCESS_TOKEN = var.o11y_realm
  ```

- また、OpenTelemetryが関数/サービスを識別し、それが属する環境/アプリケーションを認識するのに役立つ変数も設定しています。

  ```bash
  OTEL_SERVICE_NAME = "producer-lambda" # consumer関数の場合はconsumer-lambda
  OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
  ```

- コード言語に基づいて、関数のハンドラーに自動的にトレースデータを取得するために適用する必要があるラッパーをOpenTelemetryに知らせる環境変数を設定しています。

  ```bash
  AWS_LAMBDA_EXEC_WRAPPER - "/opt/nodejs-otel-handler"
  ```

- `producer-lambda` 関数の場合、レコードを配置するKinesisストリームを関数に知らせるための環境変数を設定しています。

  ```bash
  KINESIS_STREAM = aws_kinesis_stream.lambda_streamer.name
  ```

- これらの値は、「前提条件」セクションで設定した環境変数、および、このTerraform構成ファイルの一部としてデプロイされるリソースから取得されます。

また、各関数にSplunk OpenTelemetry Lambda layerを設定する引数も確認できるはずです

```bash
layers = var.otel_lambda_layer
```

- OpenTelemetry Lambda layerは、Lambda関数の呼び出し時に計測データを収集、処理、およびエクスポートするために必要なライブラリと依存関係を含むパッケージです。

- すべてのOpenTelemetryサポート言語のライブラリと依存関係を持つ一般的なOTel Lambda layerがありますが、関数をさらに軽量化するための言語固有のLambda layerも存在します。
  - _各 AWS リージョンの関連する Splunk OpenTelemetry Lambda layer ARN（Amazon Resource Name）と最新バージョンは[こちら](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md)で確認できます_

#### `producer.mjs` ファイル

次に、`producer-lambda` 関数のコードを見てみましょう：

- 以下のコマンドを実行して `producer.mjs` ファイルの内容を表示します：

  ```bash
  cat ~/o11y-lambda-workshop/auto/handler/producer.mjs
  ```

  - このNodeJSモジュールにはプロデューサー関数のコードが含まれています。
  - 基本的に、この関数はメッセージを受け取り、そのメッセージを対象のKinesisストリームにレコードとして配置します

### Lambda 関数のデプロイとトレースデータの生成

`auto` ディレクトリの内容に慣れたところで、ワークショップ用のリソースをデプロイし、Lambda関数からトレースデータを生成していきます。

#### `auto` ディレクトリで Terraform を初期化する

`main.tf` ファイルで定義されたリソースをデプロイするには、まずTerraformがそのファイルと同じフォルダで初期化されていることを確認する必要があります。

- `auto` ディレクトリにいることを確認します:

  ```bash
  pwd
  ```

  - _予想される出力は **~/o11y-lambda-workshop/auto** です_

- `auto` ディレクトリにいない場合は、次のコマンドを実行します：

  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- 次のコマンドを実行して、このディレクトリでTerraformを初期化します

  ```bash
  terraform init
  ```

  - このコマンドは同じフォルダにいくつかの要素を作成します：
    - `.terraform.lock.hcl` ファイル：リソースを提供するために使用するプロバイダーを記録します
    - `.terraform` ディレクトリ：プロバイダーの構成を保存します
  - 上記のファイルに加えて、`apply` サブコマンドを使用してterraformを実行すると、デプロイされたリソースの状態を追跡するために `terraform.tfstate` ファイルが作成されます。
  - これらにより、Terraformは `auto` ディレクトリの `main.tf` ファイル内で定義されたとおりに、リソースの作成、状態、破棄を管理できます

#### Lambda 関数とその他の AWS リソースをデプロイする

このディレクトリでTerraformを初期化したら、リソースのデプロイに進むことができます。

- まず、**terraform plan** コマンドを実行して、Terraformが問題なくリソースを作成できることを確認します。

  ```bash
  terraform plan
  ```

  - _これにより、リソースをデプロイするプランといくつかのデータが出力され、意図したとおりに動作することを確認できます。_
  - _プランに表示される値の一部は、作成後に判明するか、セキュリティ上の理由でマスクされていることに注意してください。_

- 次に、**terraform apply** コマンドを実行して、**main.tf** ファイルからLambda関数とその他のサポートリソースをデプロイします：

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

    - _Terraform 出力は **outputs.tf** ファイルで定義されています。_
    - _これらの出力は、ワークショップの他の部分でもプログラム的に使用されます。_

#### `producer-lambda` URL (`base_url`) にトラフィックを送信する

デプロイしたLambda関数からトレースを取得し始めるには、トラフィックを生成する必要があります。`producer-lambda` 関数のエンドポイントにメッセージを送信し、それをKinesisストリームにレコードとして配置し、その後 `consumer-lambda` 関数によってストリームから取得されるようにします。

- `auto` ディレクトリにいることを確認します：

  ```bash
  pwd
  ```

  - _予想される出力は **~/o11y-lambda-workshop/auto** です_

- `auto` ディレクトリにいない場合は、次のコマンドを実行します

  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

`send_message.py` スクリプトは、コマンドラインで入力を受け取り、JSONディクショナリに追加し、whileループの一部として `producer-lambda` 関数のエンドポイントに繰り返し送信するPythonスクリプトです。

- Run the `send_message.py` script as a background process

  - _`--name` と `--superpower` 引数が必要です_

  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```

  - メッセージが成功した場合は、以下のような出力が表示されるはずです

    ```bash
    [1] 79829
    user@host manual % appending output to nohup.out
    ```

    - _ここで重要な情報は 2 つあります:_
      - _1 行目のプロセス ID（この例では `79829`）、および_
      - _`appending output to nohup.out` メッセージ_
    - _`nohup` コマンドはスクリプトがバックグラウンドに送られた時に切断されないようにします。また、コマンドからの curl 出力を、現在いるフォルダと同じフォルダにある nohup.out ファイルにキャプチャします。_
    - _`&` はシェルプロセスにこのプロセスをバックグラウンドで実行するよう指示し、シェルが他のコマンドを実行できるようにします。_

- 次に、`response.logs` ファイルの内容を確認して、`producer-lambda` エンドポイントへのリクエストが成功したことを確認します：

  ```bash
  cat response.logs
  ```

  - メッセージが成功していれば、画面に印刷された行の中に次の出力が表示されるはずです：

  ```bash
  {"message": "Message placed in the Event Stream: {prefix}-lambda_stream"}
  ```

  - 失敗した場合は、次のように表示されます：

  ```bash
  {"message": "Internal server error"}
  ```

> [!IMPORTANT]
> この場合は、ワークショップ進行役の一人に支援を求めてください。

#### Lambda 関数のログを表示する

次に、Lambda関数のログを確認しましょう。

- **producer-lambda** ログを表示するには、**producer.logs** ファイルを確認します：

  ```bash
  cat producer.logs
  ```

- **consumer-lambda** ログを表示するには、**consumer.logs** ファイルを確認します：

  ```bash
  cat consumer.logs
  ```

ログを注意深く調べてください。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

- OpenTelemetryが読み込まれているのが見えますか？`splunk-extension-wrapper` のある行に注目してください
  - - _**splunk-extension-wrapper**が読み込まれているのを見るために `head -n 50 producer.logs` または `head -n 50 consumer.logs` の実行を検討してください。_

{{% /notice %}}
