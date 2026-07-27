---
title: セットアップ
linkTitle: 1. セットアップ
weight: 1
---

![手動計装されていないLambdaアプリケーション](../images/01-Architecture.png)

## 前提条件

### Observability ワークショップインスタンス

Observabilityワークショップは、多くの場合、Splunkが提供する事前設定済みのUbuntu EC2インスタンス上で実施されます。

ワークショップのインストラクターから、割り当てられたワークショップインスタンスの認証情報が提供されます。

インスタンスには以下の環境変数が既に設定されているはずです

- **ACCESS_TOKEN**
- **REALM**
  - _これらはワークショップ用の Splunk Observability Cloud の **Access Token** と **Realm** です。_
  - _これらは OpenTelemetry Collector によって、データを正しい Splunk Observability Cloud 組織に転送するために使用されます。_

> [!NOTE]\
> _また、Multipass を使用してローカルの Observability ワークショップインスタンスをデプロイすることもできます。_

### AWS Command Line Interface (awscli)

AWS Command Line Interface、または `awscli` は、AWSリソースと対話するために使用されるAPIです。このワークショップでは、特定のスクリプトがデプロイするリソースと対話するために使用されます。

Splunkが提供するワークショップインスタンスには、既に **awscli** がインストールされているはずです。

- インスタンスに **aws** コマンドがインストールされているか、次のコマンドで確認します

  ```bash
  which aws
  ```

  - _予想される出力は **/usr/local/bin/aws** です_

- インスタンスに **aws** コマンドがインストールされていない場合は、次のコマンドを実行します

  ```bash
  sudo apt install awscli
  ```

### Terraform

Terraformは、リソースを構成ファイルで定義することで、デプロイ、管理、破棄するためのInfrastructure as Code（IaC）プラットフォームです。TerraformはHCLを使用してこれらのリソースを定義し、さまざまなプラットフォームやテクノロジのための複数のプロバイダーをサポートしています。

このワークショップでは、コマンドラインでTerraformを使用して、以下のリソースをデプロイします

1. AWS API Gateway
2. Lambda関数
3. Kinesis Stream
4. CloudWatchロググループ
5. S3バケット
   - _およびその他のサポートリソース_

Splunkが提供するワークショップインスタンスには、既に **terraform** がインストールされているはずです。

- インスタンスに **terraform** コマンドがインストールされているか確認します

  ```bash
  which terraform
  ```

  - _予想される出力は **/usr/local/bin/terraform** です_

- インスタンスに **terraform** コマンドがインストールされていない場合は、以下のTerraformが推奨するインストールコマンドを実行してください

  ```bash
  wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

  sudo apt update && sudo apt install terraform
  ```

### ワークショップディレクトリ (o11y-lambda-workshop)

ワークショップディレクトリ `o11y-lambda-workshop` は、今日使用する例のLambdaベースのアプリケーションの自動計装と手動計装の両方を完了するための、すべての設定ファイルとスクリプトを含むリポジトリです。

- ホームディレクトリにワークショップディレクトリがあることを確認します

  ```bash
  cd && ls
  ```

  - _予想される出力には **o11y-lambda-workshop** が含まれるはずです_

- **o11y-lambda-workshop** ディレクトリがホームディレクトリにない場合は、次のコマンドでクローンします

```bash
git clone https://github.com/gkono-splunk/o11y-lambda-workshop.git
```

### AWS & Terraform 変数

#### AWS

AWSのCLIでは、サービスによってデプロイされたリソースにアクセスし管理するための認証情報が必要です。このワークショップでは、TerraformとPythonスクリプトの両方がタスクを実行するためにこれらの変数を必要とします。

- このワークショップのために **awscli** を _**access key ID**_、_**secret access key**_ および _**region**_ で構成します

  ```bash
  aws configure
  ```

  - _このコマンドは以下のようなプロンプトを表示するはずです：_

    ```bash
    AWS Access Key ID [None]: XXXXXXXXXXXXXXXX
    AWS Secret Acces Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    Default region name [None]: us-east-1
    Default outoput format [None]:
    ```

- インスタンスで **awscli** が設定されていない場合は、次のコマンドを実行し、インストラクターから提供される値を入力してください。

  ```bash
  aws configure
  ```

#### Terraform

Terraformでは、機密情報や動的データを.tf設定ファイルにハードコーディングさせない、またはそれらの値をリソース定義全体で再利用できるようにするため、変数の受け渡しをサポートしています。

このワークショップでは、OpenTelemetry Lambda layerの適切な値でLambda関数をデプロイするため、Splunk Observability Cloudの取り込み値のため、そして環境とリソースを独自で即座に認識できるようにするための変数をTerraformで必要とします。

Terraform変数(variable)は以下の方法で定義されます

- 変数を _**main.tf**_ ファイルまたは _**variables.tf**_ に定義する
- 以下のいずれかの方法で変数の値を設定する
  - ホストレベルで環境変数を設定し、その定義と同じ変数名を使用して、接頭辞として _**TF_VAR**_ をつける
  - _**terraform.tfvars**_ ファイルに変数の値を設定する
  - terraform apply実行時に引数として値を渡す

このワークショップでは、_**variables.tf**_ と _**terraform.tfvars**_ ファイルの組み合わせを使用して変数を設定します。

- **vi** または **nano** のいずれかを使用して、**auto** または **manual** ディレクトリにある _**terraform.tfvars**_ ファイルを開きます

  ```bash
  vi ~/o11y-lambda-workshop/auto/terraform.tfvars
  ```

- 変数に値を設定します。**CHANGEME** プレースホルダーをインストラクターから提供された値に置き換えてください。

  ```bash
  o11y_access_token = "CHANGEME"
  o11y_realm        = "CHANGEME"
  otel_lambda_layer = ["CHANGEME"]
  prefix            = "CHANGEME"
  ```

  - _引用符（"）や括弧 ( [ ] ) はそのまま残し、プレースホルダー`CHANGEME` のみを変更してください。_
  - _**prefix**_ は、他の参加者のリソースと区別するため、任意の文字列で設定する固有の識別子です。氏名やメールアドレスのエイリアスを使用することをお勧めします。
  - _**prefix** には小文字のみを使用してください。S3 のような特定の AWS リソースでは、大文字を使用するとエラーが発生します。_

- ファイルを保存してエディタを終了します。
- 最後に、編集した _**terraform.tfvars**_ ファイルを他のディレクトリにコピーします。

  ```bash
  cp ~/o11y-lambda-workshop/auto/terraform.tfvars ~/o11y-lambda-workshop/manual
  ```

  - _これは、自動計装と手動計装の両方の部分で同じ値を使用するためです_

### ファイル権限

他のすべてのファイルはそのままでよいですが、`auto` と `manual` の両方にある**send_message.py**スクリプトは、ワークショップの一部として実行する必要があります。そのため、期待通りに実行するには、適切な権限が必要です。以下の手順に従って設定してください。

- まず、`o11y-lambda-workshop` ディレクトリにいることを確認します

  ```bash
  cd ~/o11y-lambda-workshop
  ```

- 次に、以下のコマンドを実行して `send_message.py` スクリプトに実行権限を設定します

  ```bash
  sudo chmod 755 auto/send_message.py manual/send_message.py
  ```

これで前提条件が整いましたので、ワークショップを始めることができます！
