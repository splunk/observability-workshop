---
title: Auto-Instrumentation
linkTitle: 3. Auto-Instrumentation
weight: 3
time: 15 mins
---

ワークショップの最初のパートでは、OpenTelemetry による自動計装がどのように機能するかを説明します。OpenTelemetry Collector が関数の記述言語を自動検出し、それらの関数のトレースキャプチャを開始する仕組みを確認します。

まず、`workshop/lambda/auto` ディレクトリとそのファイルを確認しましょう。ここにワークショップの自動計装に関するすべてのコンテンツが格納されています。

* 以下のコマンドを実行して **workshop/lambda/auto** ディレクトリに移動します:

```bash
cd ~/workshop/lambda/auto
```

* このディレクトリの内容を確認します:

```bash
ls
```

出力には以下のファイルとディレクトリが含まれているはずです:

```bash
handler             outputs.tf          terraform.tf        variables.tf
main.tf             send_message.py     terraform.tfvars
```

`main.tf` ファイルを詳しく見てみましょう:

```bash
cat main.tf
```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

* このテンプレートによって作成される AWS リソースを特定できますか？
* OpenTelemetry の計装が設定されている箇所を特定できますか？
  * ヒント: Lambda 関数の定義を確認してください
* 先ほど設定した環境変数によって提供される計装情報を特定できますか？
{{% /notice %}}

各 Lambda 関数の環境変数が設定されているセクションが表示されるはずです。

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

これらの環境変数を使用して、自動計装をいくつかの方法で設定しています:

* データのエクスポート先となる Splunk Observability Cloud 組織を OpenTelemetry Collector に通知する環境変数を設定しています。

```bash
SPLUNK_ACCESS_TOKEN = var.o11y_access_token
SPLUNK_ACCESS_TOKEN = var.o11y_realm
```

* OpenTelemetry が関数/サービスを識別し、それが属する環境/アプリケーションを特定するための変数も設定しています。

```bash
OTEL_SERVICE_NAME = "producer-lambda" # consumer-lambda in the case of the consumer function
OTEL_RESOURCE_ATTRIBUTES = "deployment.environment=${var.prefix}-lambda-shop"
```

* コード言語に基づいてトレースデータを自動的にキャプチャするために、関数のハンドラーに適用するラッパーを OpenTelemetry に通知する環境変数を設定しています。

```bash
AWS_LAMBDA_EXEC_WRAPPER - "/opt/nodejs-otel-handler"
```

* `producer-lambda` 関数の場合、レコードを送信する Kinesis Stream を関数に通知する環境変数を設定しています。

```bash
KINESIS_STREAM = aws_kinesis_stream.lambda_streamer.name
```

* これらの値は、前提条件セクションで設定した環境変数と、この Terraform 設定ファイルの一部としてデプロイされるリソースから取得されます。

各関数に Splunk OpenTelemetry Lambda レイヤーを設定する引数も表示されるはずです。

```bash
layers = var.otel_lambda_layer
```

* OpenTelemetry Lambda レイヤーは、Lambda 関数の呼び出し時にテレメトリデータを収集、処理、エクスポートするために必要なライブラリと依存関係を含むパッケージです。
* すべての OpenTelemetry 対応言語のライブラリと依存関係を含む汎用の OTel Lambda レイヤーがありますが、関数をさらに軽量にするための言語固有の Lambda レイヤーもあります。
  * 各 AWS リージョンの関連する Splunk OpenTelemetry Lambda レイヤー ARN（Amazon Resource Name）と最新バージョンは[こちら](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md)で確認できます

次に、`producer-lambda` 関数のコードを見てみましょう:

* 以下のコマンドを実行して `producer.mjs` ファイルの内容を表示します:

```bash
cat ~/workshop/lambda/auto/handler/producer.mjs
```

* この NodeJS モジュールには producer 関数のコードが含まれています。
* 基本的に、この関数はメッセージを受信し、そのメッセージをレコードとして対象の Kinesis Stream に送信します。

`auto` ディレクトリの内容を確認できたので、ワークショップのリソースをデプロイし、Lambda 関数からトレースデータを生成しましょう。

{{% exercise title="Lambda 関数のデプロイ" %}}

`main.tf` ファイルで定義されたリソースをデプロイするには、まずそのファイルと同じフォルダで Terraform が初期化されていることを確認する必要があります。

* `auto` ディレクトリに移動します:

```bash
cd ~/workshop/lambda/auto
```

* 以下のコマンドを実行して、このディレクトリで Terraform を初期化します

```bash
terraform init
```

* このコマンドにより、同じフォルダにいくつかの要素が作成されます:
  * `.terraform.lock.hcl` ファイル: リソースの提供に使用するプロバイダーを記録します
    * `.terraform` ディレクトリ: プロバイダーの設定を保存します
  * 上記のファイルに加えて、`apply` サブコマンドで terraform を実行すると、デプロイされたリソースの状態を追跡する `terraform.tfstate` ファイルが作成されます。
  * これらにより、Terraform は `auto` ディレクトリの `main.tf` ファイルで定義されたリソースの作成、状態管理、削除を管理できます

このディレクトリで Terraform を初期化したら、リソースをデプロイしましょう。

* まず、**terraform plan** コマンドを実行して、Terraform が問題なくリソースを作成できることを確認します。

```bash
terraform plan
```

* これにより、リソースのデプロイ計画とデータの出力が表示されます。すべてが意図通りに動作することを確認できます。
  * 計画に表示される値の多くは、作成後に判明するか、セキュリティ上の理由でマスクされていることに注意してください。

* 次に、**terraform apply** コマンドを実行して、**main.tf** ファイルから Lambda 関数とその他のサポートリソースをデプロイします:

```bash
terraform apply
```

* **Enter a value:** プロンプトが表示されたら **yes** と入力します

* 以下の出力が表示されます:

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

* Terraform の出力は **outputs.tf** ファイルで定義されています。
* これらの出力は、ワークショップの他のパートでもプログラム的に使用されます。

{{% /exercise %}}

{{% exercise title="`producer-lambda` にトラフィックを送信する" %}}

デプロイした Lambda 関数からトレースを取得するには、トラフィックを生成する必要があります。`producer-lambda` 関数のエンドポイントにメッセージを送信し、そのメッセージが Kinesis Stream にレコードとして配置され、`consumer-lambda` 関数によって Stream から取得されることを確認します。

* `auto` ディレクトリに移動します:

```bash
cd ~/workshop/lambda/auto
```

`send_message.py` スクリプトは、コマンドラインで入力を受け取り、JSON ディクショナリに追加して、while ループの一部として `producer-lambda` 関数のエンドポイントに繰り返し送信する Python スクリプトです。

* `send_message.py` スクリプトをバックグラウンドプロセスとして実行します
  * `--name` と `--superpower` 引数が必要です

```bash
nohup ./send_message.py --name CHANGEME --superpower CHANGEME &
```

* メッセージが成功した場合、以下のような出力が表示されます

```bash
[1] 179789
nohup: ignoring input and appending output to 'nohup.out'
```

* ここで最も重要な情報は以下の2つです:
  * 1行目のプロセス ID（この例では `79829`）
  * `appending output to nohup.out` メッセージ
    * `nohup` コマンドは、スクリプトがバックグラウンドに送信されたときにハングアップしないようにします。また、コマンドの curl 出力を現在のフォルダと同じフォルダにある nohup.out ファイルにキャプチャします。
    * `&` はシェルプロセスにこのプロセスをバックグラウンドで実行するよう指示し、シェルを解放して他のコマンドを実行できるようにします。

* 次に、`response.logs` ファイルの内容を確認して、`producer-lambda` エンドポイントへのリクエストが成功していることを確認します:

```bash
cat response.logs
```

* メッセージが成功した場合、画面に表示される行の中に以下の出力が含まれているはずです:

```bash
{"message": "Message placed in the Event Stream: {prefix}-lambda_stream"}
```

* 失敗した場合は、以下が表示されます:

```bash
{"message": "Internal server error"}
```

{{< notice warning >}}
この場合は、ワークショップのファシリテーターに支援を依頼してください。
{{< /notice >}}

{{% /exercise %}}

{{% exercise title="Lambda 関数のログを確認する" %}}

次に、Lambda 関数のログを確認しましょう。

* **producer-lambda** のログを確認するには、**producer.logs** ファイルを確認します:

```bash
cat producer.logs
```

* **consumer-lambda** のログを確認するには、**consumer.logs** ファイルを確認します:

```bash
cat consumer.logs
```

ログを注意深く確認してください。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

* OpenTelemetry がロードされているのが確認できますか？`splunk-extension-wrapper` を含む行を探してください。
  * `head -n 50 producer.logs` または `head -n 50 consumer.logs` を実行して、**splunk-extension-wrapper** がロードされている様子を確認してみてください。

{{% /notice %}}

{{% /exercise %}}
