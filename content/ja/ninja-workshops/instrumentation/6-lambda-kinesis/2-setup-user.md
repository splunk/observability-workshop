---
title: セットアップ（ユーザー）
linkTitle: 2. セットアップ（ユーザー）
weight: 2
time: 10 minutes
---

![Lambda application, not yet manually instrumented](../images/01-Architecture.png)

## Observability Workshop インスタンス

事前設定済みの Ubuntu を実行する EC2 インスタンスが提供されます。

ワークショップのインストラクターが、割り当てられたワークショップインスタンスへの認証情報を提供します。

インスタンスには以下の環境変数がすでに設定されているはずです

- **ACCESS_TOKEN**: Observability Cloud にデータを取り込むためのトークン
- **REALM**: このワークショップで使用するレルム

また、ワークショップ中に使用する AWS キーとシークレットも提供されます。

AWS CLI と Terraform が利用可能であることを確認しましょう。

## AWS Command Line Interface (awscli)

AWS Command Line Interface（`awscli`）は、AWS リソースとやり取りするために使用される API です。このワークショップでは、デプロイするリソースとやり取りするために特定のスクリプトで使用されます。

Splunk が提供するワークショップインスタンスには、すでに **awscli** がインストールされているはずです。

- 以下のコマンドで、インスタンスに **aws** コマンドがインストールされているか確認します

```bash
which aws
```

期待される出力は以下のとおりです

```bash
/usr/local/bin/aws
```

- インスタンスに **aws** コマンドがインストールされていない場合は、以下のコマンドを実行します

```bash
sudo apt install awscli
```

## Terraform

Terraform は Infrastructure as Code（IaC）プラットフォームで、設定ファイルにリソースを定義することでデプロイ、管理、削除を行います。Terraform は HCL を使用してリソースを定義し、さまざまなプラットフォームやテクノロジー向けの複数のプロバイダーをサポートしています。

このワークショップでは、コマンドラインで Terraform を使用して以下のリソースをデプロイします

1. AWS API Gateway
2. Lambda Functions
3. Kinesis Stream
4. CloudWatch Log Groups
5. S3 Bucket
    - _およびその他のサポートリソース_
  
Splunk が提供するワークショップインスタンスには、すでに **terraform** がインストールされているはずです。

- インスタンスに **terraform** コマンドがインストールされているか確認します

```bash
which terraform
```

期待される出力は以下のとおりです

```bash
terraform () {
        echo "Using API_TOKEN=XXX" >&2
        echo "Using REALM=us1" >&2
        command terraform "$@"
}
```

- インスタンスに **terraform** コマンドがインストールされていない場合は、以下の Terraform 推奨のインストールコマンドに従ってください

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

## Workshop ディレクトリ（Lambda）

Workshop ディレクトリ `lambda` は、本日使用する Lambda ベースのサンプルアプリケーションの自動インストルメンテーションと手動インストルメンテーションの両方を完了するために必要な、すべての設定ファイルとスクリプトを含むリポジトリです。

- ホームディレクトリにワークショップディレクトリがあることを確認します

```bash
cd ~/workshop/lambda && ls
```

期待される出力は以下のようになります

```bash
auto  iam_role  manual
```

## AWS と Terraform の変数設定

### AWS 変数

AWS CLI では、サービスによってデプロイされたリソースにアクセスして管理するための認証情報が必要です。このワークショップでは、Terraform と Python スクリプトの両方がタスクを実行するためにこれらの変数を必要とします。

- このワークショップ用の _**access key ID**_、_**secret access key**_、_**region**_ で **awscli** を設定します

```bash
aws configure
```

このコマンドは以下のようなプロンプトを表示します。キー ID とシークレットキーを入力し、リージョンを `us-east-1` に設定し、出力形式はデフォルトのままにします

```bash
AWS Access Key ID [None]: XXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Default region name [None]: us-east-1
Default outoput format [None]:
```

以下のコマンドで動作を確認できます

```bash
aws lambda list-functions
```

結果が表示されるはずです。空の場合もあれば、いくつかの関数が表示される場合もありますが、エラーにはならないはずです。成功したら、`q` を押して終了します。

### Terraform 変数

Terraform は、機密データや動的データを .tf 設定ファイルにハードコーディングしないようにするため、またリソース定義全体で値を再利用可能にするために、変数の受け渡しをサポートしています。

このワークショップでは、Terraform は Lambda 関数を OpenTelemetry Lambda レイヤーの正しい値でデプロイするため、Splunk Observability Cloud の取り込み値のため、そして環境とリソースを一意で即座に識別可能にするために変数を必要とします。

Terraform 変数は以下の方法で定義されます

- _**main.tf**_ ファイルまたは _**variables.tf**_ で変数を定義します
- 以下のいずれかの方法で変数の値を設定します
  - ホストレベルで環境変数を設定します。定義と同じ変数名に _**TF_VAR**__ をプレフィックスとして付けます
  - _**terraform.tfvars**_ ファイルで変数の値を設定します
  - terraform apply 実行時に引数として値を渡します

このワークショップでは、_**variables.tf**_ と _**terraform.tfvars**_ ファイルの組み合わせを使用して変数を設定します。

- **vi** または **nano** を使用して、**auto** または **manual** ディレクトリ内の _**terraform.tfvars**_ ファイルを開きます

```bash
vi ~/workshop/lambda/auto/terraform.tfvars
```

- 変数に値を設定します。**CHANGEME** プレースホルダーをインストラクターから提供された値に置き換えてください。

```bash
o11y_access_token = "CHANGEME"
o11y_realm        = "CHANGEME"
otel_lambda_layer = ["CHANGEME"]
prefix            = "CHANGEME"
```

以下の方法でこれらの値を取得できます

- `o11y_access_token`: `export | grep ACCESS_TOKEN` を実行すると、返された値を使用できます
- `o11y_realm`: お使いのレルム（例`us1`、`eu0` など）
- `otel_lamba_layer`: [こちら](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md)から提供される `us-east-1` の値を使用します
- `prefix`: 名前の短縮形を使用します（すべて小文字）

インストラクターがこれらの値の確認をお手伝いします。

ファイルを保存してエディタを終了します。

最後に、編集した `terraform.tfvars` ファイルをもう一方のディレクトリにコピーします。

```bash
cp ~/workshop/lambda/auto/terraform.tfvars ~/workshop/lambda/manual
```

## ファイル権限の修正（オプション）

これらのファイルは実行可能であるはずですが、念のため設定しておきましょう

```bash
chmod +x ~/workshop/lambda/auto/send_message.py
chmod +x ~/workshop/lambda/manual/send_message.py
```

前提条件の準備が完了しましたので、ワークショップを開始しましょう！
