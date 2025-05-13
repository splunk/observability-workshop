---
title: 自動計装
linkTitle: 2. 自動計装
weight: 2
---

ワークショップの最初の部分では、OpenTelemetryによる自動計装がどのようにしてOpenTelemetry Collectorに関数がどの言語で書かれているかを自動検出させ、それらの関数のトレースの取得を開始させるかを示します。

### 自動計装ワークショップディレクトリとコンテンツ
まず、`o11y-lambda-workshop/auto`ディレクトリとそのファイルの一部を見てみましょう。ここにはワークショップの自動計装部分のすべてのコンテンツがあります。

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
  - _ヒント: Lambda関数の定義を調べてください_
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

- `producer-lambda`関数の場合、レコードを配置するKinesisストリームを関数に知らせるための環境変数を設定しています。
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
  - _各AWSリージョンの関連するSplunk OpenTelemetry Lambda layer ARN（Amazon Resource Name）と最新バージョンは[こちら](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md)で確認できます_

#### `producer.mjs` ファイル
次に、`producer-lambda`関数のコードを見てみましょう：

- 以下のコマンドを実行して`producer.mjs`ファイルの内容を表示します：
  ```bash
  cat ~/o11y-lambda-workshop/auto/handler/producer.mjs
  ```
  - このNodeJSモジュールにはプロデューサー関数のコードが含まれています。
  - 基本的に、この関数はメッセージを受け取り、そのメッセージを対象のKinesisストリームにレコードとして配置します

### Lambda関数のデプロイとトレースデータの生成
`auto`ディレクトリの内容に慣れたところで、ワークショップ用のリソースをデプロイし、Lambda関数からトレースデータを生成していきます。

#### `auto`ディレクトリでTerraformを初期化する
`main.tf`ファイルで定義されたリソースをデプロイするには、まずTerraformがそのファイルと同じフォルダで初期化されていることを確認する必要があります。

- Ensure you are in the `auto` directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/o11y-lambda-workshop/auto**_

- If you are not in the `auto` directory, run the following command:
  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- Run the following command to initialize Terraform in this directory
  ```bash
  terraform init
  ```
  - This command will create a number of elements in the same folder:
    - `.terraform.lock.hcl` file: to record the providers it will use to provide resources
    - `.terraform` directory: to store the provider configurations
  - In addition to the above files, when terraform is run using the `apply` subcommand, the `terraform.tfstate` file will be created to track the state of your deployed resources.
  - These enable Terraform to manage the creation, state and destruction of resources, as defined within the `main.tf` file of the `auto` directory

#### Deploy the Lambda functions and other AWS resources
Once we've initialized Terraform in this directory, we can go ahead and deploy our resources.

- First, run the **terraform plan** command to ensure that Terraform will be able to create your resources without encountering any issues.
  ```bash
  terraform plan
  ```
  - _This will result in a plan to deploy resources and output some data, which you can review to ensure everything will work as intended._
  - _Do note that a number of the values shown in the plan will be known post-creation, or are masked for security purposes._

- Next, run the **terraform apply** command to deploy the Lambda functions and other supporting resources from the **main.tf** file:
  ```bash
  terraform apply
  ```
  - _Respond **yes** when you see the **Enter a value:** prompt_

  - This will result in the following outputs:
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
    - _Terraform outputs are defined in the **outputs.tf** file._
    - _These outputs will be used programmatically in other parts of our workshop, as well._

#### Send some traffic to the `producer-lambda` URL (`base_url`)

To start getting some traces from our deployed Lambda functions, we would need to generate some traffic. We will send a message to our `producer-lambda` function's endpoint, which should be put as a record into our Kinesis Stream, and then pulled from the Stream by the `consumer-lambda` function.

- Ensure you are in the `auto` directory:
  ```bash
  pwd
  ```
  - _The expected output would be **~/o11y-lambda-workshop/auto**_

- If you are not in the `auto` directory, run the following command
  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

The `send_message.py` script is a Python script that will take input at the command line, add it to a JSON dictionary, and send it to your `producer-lambda` function's endpoint repeatedly, as part of a while loop.

- Run the `send_message.py` script as a background process
  - _It requires the `--name` and `--superpower` arguments_
  ```bash
  nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
  ```
  - You should see an output similar to the following if your message is successful
    ```bash
    [1] 79829
    user@host manual % appending output to nohup.out
    ```
    - _The two most import bits of information here are:_
      - _The process ID on the first line (`79829` in the case of my example), and_
      - _The `appending output to nohup.out` message_
    - _The `nohup` command ensures the script will not hang up when sent to the background. It also captures the curl output from our command in a nohup.out file in the same folder as the one you're currently in._
    - _The `&` tells our shell process to run this process in the background, thus freeing our shell to run other commands._

- Next, check the contents of the `response.logs` file, to ensure your output confirms your requests to your `producer-lambda` endpoint are successful:
  ```bash
  cat response.logs
  ```
  - You should see the following output among the lines printed to your screen if your message is successful:
  ```bash
  {"message": "Message placed in the Event Stream: {prefix}-lambda_stream"}
  ```

  - If unsuccessful, you will see:
  ```bash
  {"message": "Internal server error"}
  ```

> [!IMPORTANT]
> If this occurs, ask one of the workshop facilitators for assistance.

#### View the Lambda Function Logs
Next, let's take a look at the logs for our Lambda functions.

- To view your **producer-lambda** logs, check the **producer.logs** file:
  ```bash
  cat producer.logs
  ```

- To view your **consumer-lambda** logs, check the **consumer.logs** file:
  ```bash
  cat consumer.logs
  ```

Examine the logs carefully.

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

- OpenTelemetryが読み込まれているのが見えますか？`splunk-extension-wrapper`のある行に注目してください
  - - _**splunk-extension-wrapper**が読み込まれているのを見るために`head -n 50 producer.logs`または`head -n 50 consumer.logs`の実行を検討してください。_

{{% /notice %}}
