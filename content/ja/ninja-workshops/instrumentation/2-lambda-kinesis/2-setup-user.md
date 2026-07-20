---
title: セットアップ（ユーザー）
linkTitle: 2. セットアップ（ユーザー）
weight: 2
time: 10 minutes
---

![Lambda application, not yet manually instrumented](../images/01-Architecture.png)

## Observability Workshopインスタンス

事前設定済みのUbuntuが動作するEC2インスタンスが提供されます。

ワークショップのインストラクターから、割り当てられたワークショップインスタンスへの認証情報が提供されます。

インスタンスには以下の環境変数がすでに設定されているはずです。

- **ACCESS_TOKEN**: Observability Cloudにデータを取り込むためのトークン
- **REALM**: ワークショップで使用するRealm

また、ワークショップ中に使用するAWSキーとシークレットも提供されます。

AWS CLIとTerraformが利用可能か確認しましょう。

## AWS Command Line Interface (awscli)

AWS Command Line Interface（`awscli`）は、AWSリソースとやり取りするためのAPIです。このワークショップでは、デプロイしたリソースとやり取りする特定のスクリプトで使用されます。

Splunkが提供するワークショップインスタンスには、すでに **awscli** がインストールされているはずです。

- 以下のコマンドで、インスタンスに **aws** コマンドがインストールされているか確認します

```bash
which aws
```

期待される出力は以下の通りです。

```bash
/usr/local/bin/aws
```

- インスタンスに **aws** コマンドがインストールされていない場合は、以下のコマンドを実行します

```bash
sudo apt install awscli
```

## Terraform

TerraformはInfrastructure as Code（IaC）プラットフォームで、設定ファイルにリソースを定義することでデプロイ、管理、削除を行います。TerraformはHCLを使用してリソースを定義し、さまざまなプラットフォームや技術向けの複数のプロバイダーをサポートしています。

このワークショップでは、コマンドラインでTerraformを使用して以下のリソースをデプロイします。

1. AWS API Gateway
2. Lambda Functions
3. Kinesis Stream
4. CloudWatch Log Groups
5. S3 Bucket
    - _およびその他のサポートリソース_
  
Splunkが提供するワークショップインスタンスには、すでに **terraform** がインストールされているはずです。

- インスタンスに **terraform** コマンドがインストールされているか確認します

```bash
which terraform
```

期待される出力は以下の通りです。

```bash
terraform () {
        echo "Using API_TOKEN=XXX" >&2
        echo "Using REALM=us1" >&2
        command terraform "$@"
}
```

- インスタンスに **terraform** コマンドがインストールされていない場合は、以下のTerraform推奨インストールコマンドを実行します

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

## ワークショップディレクトリ（Lambda）

ワークショップディレクトリ `lambda` は、本日使用するLambdaベースのサンプルアプリケーションの自動計装と手動計装の両方を完了するために必要なすべての設定ファイルとスクリプトを含むリポジトリです。

- ホームディレクトリにワークショップディレクトリがあることを確認します

```bash
cd ~/workshop/lambda && ls
```

期待される出力は以下のようになります。

```bash
auto  iam_role  manual
```

## AWSとTerraform変数の設定

### AWS変数

AWS CLIでは、サービスによってデプロイされたリソースにアクセスして管理するための認証情報が必要です。このワークショップのTerraformとPythonスクリプトの両方で、タスクを実行するためにこれらの変数が必要です。

- このワークショップ用の _**アクセスキーID**_、_**シークレットアクセスキー**_、_**リージョン**_ を使用して **awscli** を設定します

```bash
aws configure
```

このコマンドを実行すると、以下のようなプロンプトが表示されます。キーIDとシークレットキーを入力し、リージョンを `us-east-1` に設定し、出力形式はデフォルトのままにします。

```bash
AWS Access Key ID [None]: XXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Default region name [None]: us-east-1
Default outoput format [None]:
```

以下のコマンドで動作確認ができます。

```bash
aws lambda list-functions
```

結果が表示されるはずです。空の場合やいくつかの関数が表示される場合がありますが、エラーではないはずです。成功したら、`q` を押して終了します。

### Terraform変数

Terraformは変数の受け渡しをサポートしており、機密データや動的データを.tf設定ファイルにハードコードせずに済み、リソース定義全体で値を再利用できます。

このワークショップでは、TerraformにはOpenTelemetry Lambda Layerの正しい値でLambda関数をデプロイするために必要な変数、Splunk Observability Cloudの取り込み値、および環境とリソースを一意かつすぐに識別可能にするための変数が必要です。

Terraform変数は以下の方法で定義します。

- _**main.tf**_ ファイルまたは _**variables.tf**_ で変数を定義する
- 以下のいずれかの方法で変数の値を設定する
  - ホストレベルで環境変数を設定する（定義と同じ変数名に _**TF_VAR**__ をプレフィックスとして付ける）
  - _**terraform.tfvars**_ ファイルで変数の値を設定する
  - terraform apply実行時に引数として値を渡す

このワークショップでは、_**variables.tf**_ と _**terraform.tfvars**_ ファイルの組み合わせを使用して変数を設定します。

- **vi** または **nano** を使用して、**auto** または **manual** ディレクトリの _**terraform.tfvars**_ ファイルを開きます

```bash
vi ~/workshop/lambda/auto/terraform.tfvars
```

- 変数に値を設定します。**CHANGEME** プレースホルダーをインストラクターから提供された値に置き換えます。

```bash
o11y_access_token = "CHANGEME"
o11y_realm        = "CHANGEME"
otel_lambda_layer = ["CHANGEME"]
prefix            = "CHANGEME"
```

以下の方法で値を取得できます。

- `o11y_access_token`: `export | grep ACCESS_TOKEN` を実行して返された値を使用します
- `o11y_realm`: あなたのRealm（例: `us1`、`eu0` など）
- `otel_lamba_layer`: [こちら](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md)から提供される `us-east-1` の値を使用します
- `prefix`: 名前の短縮形を使用します（すべて小文字）

インストラクターがこれらの値の確認をサポートします。

ファイルを保存してエディタを終了します。

最後に、編集した `terraform.tfvars` ファイルをもう一方のディレクトリにコピーします。

```bash
cp ~/workshop/lambda/auto/terraform.tfvars ~/workshop/lambda/manual
```

## ファイル権限の修正（オプション）

これらのファイルは実行可能であるはずですが、念のため設定します。

```bash
chmod +x ~/workshop/lambda/auto/send_message.py
chmod +x ~/workshop/lambda/manual/send_message.py
```

前提条件の確認が完了したので、ワークショップを開始しましょう！
