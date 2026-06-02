---
title: Setup
linkTitle: 1. Setup
weight: 1
---

![Lambda application, not yet manually instrumented](../images/01-Architecture.png)

## 前提条件

### Observability Workshop インスタンス

本 Observability Workshop では Splunk Show の `Splunk4Ninjas - Observability` ワークショップテンプレートを使用しており、Ubuntu が稼働する事前構成済みの EC2 インスタンスが提供されます。

ワークショップのインストラクターから、割り当てられたワークショップインスタンスの認証情報が提供されます。

インスタンスには以下の環境変数があらかじめ設定されているはずです。

- **ACCESS_TOKEN**
- **REALM**
  - _これらはワークショップで使用する Splunk Observability Cloud の **Access Token** と **Realm** です。_
  - _OpenTelemetry Collector がこれらの値を使用して、データを正しい Splunk Observability Cloud の組織へ転送します。_

> [!NOTE]
> _代替手段として、Multipass を使用してローカルの observability workshop インスタンスをデプロイすることも可能です。_

### AWS Command Line Interface (awscli)

AWS Command Line Interface（`awscli`）は、AWS リソースとやり取りするための API です。本ワークショップでは、デプロイするリソースに対する操作を行うために、いくつかのスクリプトから利用されます。

Splunk から提供されたワークショップインスタンスには、すでに **awscli** がインストールされているはずです。

- 次のコマンドで、インスタンスに **aws** コマンドがインストールされているかを確認します。

  ```bash
  which aws
  ```

  - _期待される出力は **/usr/local/bin/aws** です。_

- インスタンスに **aws** コマンドがインストールされていない場合は、次のコマンドを実行します。

  ```bash
  sudo apt install awscli
  ```

### Terraform

Terraform は Infrastructure as Code (IaC) のプラットフォームで、構成ファイルにリソースを定義することで、リソースのデプロイ、管理、削除を行います。Terraform はリソースの定義に HCL を使用し、さまざまなプラットフォームや技術に対応した複数のプロバイダーをサポートしています。

本ワークショップでは、コマンドラインから Terraform を使用して以下のリソースをデプロイします。

1. AWS API Gateway
2. Lambda Functions
3. Kinesis Stream
4. CloudWatch Log Groups
5. S3 Bucket
    - _および、その他のサポートリソース_
  
Splunk から提供されたワークショップインスタンスには、すでに **terraform** がインストールされているはずです。

- インスタンスに **terraform** コマンドがインストールされているかを確認します。

  ```bash
  which terraform
  ```

  - _期待される出力は **/usr/local/bin/terraform** です。_

- インスタンスに **terraform** コマンドがインストールされていない場合は、Terraform 推奨の以下のインストールコマンドを実行してください。

  ```bash
  wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

  sudo apt update && sudo apt install terraform
  ```

### Workshop Directory (lambda)

Workshop Directory `lambda` は、本日使用する Lambda ベースのサンプルアプリケーションについて、自動計装と手動計装の両方を実施するために必要な構成ファイルとスクリプトをすべて含むリポジトリです。

- ホームディレクトリにワークショップディレクトリがあることを確認します。

  ```bash
  cd ~/workshop && ls
  ```

  - _期待される出力には **lambda** が含まれます。_

### AWS と Terraform の変数

#### AWS

> ワークショップインストラクター向けの注意事項：対象の AWS アカウントに `lambda-workshop-user` という新しいユーザーを作成してください。
> Terraform で必要な操作を実行するためのフルパーミッションを付与してください。`lambda-workshop-user`
> ユーザーのアクセストークンを作成し、Access Key ID と Secret Access Key をワークショップ参加者に共有してください。ワークショップが完了したら
> ユーザーを削除してください。

AWS CLI でサービスがデプロイしたリソースにアクセスし管理するためには、認証情報が必要です。本ワークショップで使用する Terraform および Python スクリプトは、いずれもタスクを実行するためにこれらの変数を必要とします。

- 本ワークショップ用の _**access key ID**_、_**secret access key**_、_**region**_ を使用して **awscli** を構成します。

  ```bash
  aws configure
  ```

  - _このコマンドを実行すると、以下のようなプロンプトが表示されます。_

      ```bash
      AWS Access Key ID [None]: XXXXXXXXXXXXXXXX
      AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      Default region name [None]: us-east-1
      Default outoput format [None]:
      ```

- インスタンスで **awscli** が構成されていない場合は、次のコマンドを実行し、インストラクターから提供される値を入力してください。

  ```bash
  aws configure
  ```

#### IAM ロールの作成（ワークショップインストラクターのみ）

> ワークショップインストラクター向けの注意事項：このステップで作成する IAM ロールは
> ワークショップ参加者全員で共有されるため、一度だけ実施すれば十分です。

``` bash
cd ~/workshop/lambda/iam_role
terraform init
terraform plan
terraform apply 
```

> ワークショップインストラクター向けの注意事項：ワークショップ完了後は、以下の手順でロールをクリーンアップしてください。

``` bash
cd ~/workshop/lambda/iam_role
terraform destroy
```

#### Terraform

Terraform は変数の受け渡しをサポートしており、機密情報や動的なデータを .tf 構成ファイルにハードコードしないようにするとともに、リソース定義全体でそれらの値を再利用できるようにします。

本ワークショップでは、Terraform は OpenTelemetry Lambda layer の正しい値で Lambda 関数をデプロイするために必要な変数、Splunk Observability Cloud のインジェスト値、および環境やリソースを一意かつ識別しやすくするための値を必要とします。

Terraform の変数は次のように定義します。

- _**main.tf**_ ファイルまたは _**variables.tf**_ で変数を定義する
- 以下のいずれかの方法でその変数の値を設定する
  - ホストレベルで、定義と同じ変数名に _**TF_VAR**__ プレフィックスを付けた環境変数を設定する
  - _**terraform.tfvars**_ ファイルで変数の値を設定する
  - terraform apply を実行する際に値を引数として渡す

本ワークショップでは、_**variables.tf**_ と _**terraform.tfvars**_ ファイルを組み合わせて変数を設定します。

- **vi** または **nano** を使用して、**auto** または **manual** ディレクトリにある _**terraform.tfvars**_ ファイルを開きます。

  ```bash
  vi ~/workshop/lambda/auto/terraform.tfvars
  ```

- 変数に値を設定します。**CHANGEME** のプレースホルダーを、インストラクターから提供された値に置き換えてください。

  ```bash
  o11y_access_token = "CHANGEME"
  o11y_realm        = "CHANGEME"
  otel_lambda_layer = ["CHANGEME"]
  prefix            = "CHANGEME"
  ```

  - _プレースホルダーのみを変更し、該当する場合はクオートやブラケットはそのまま残すように注意してください。_
  - _**otel_lambda_layer** には、[こちら](https://github.com/signalfx/lambda-layer-versions/blob/main/splunk-apm/splunk-apm.md) に記載されている **us-east-1** 用の値を使用してください。_
  - _**prefix** は他の参加者のリソースと区別するために自分で選べる一意の識別子です。たとえば名前を短くしたものを使用することをお勧めします。_
  - _また、**prefix** には小文字のみを使用してください。S3 のような AWS の一部のリソースでは、大文字を使用するとエラーが発生します。_
- ファイルを保存してエディターを終了します。
- 最後に、編集した _**terraform.tfvars**_ ファイルをもう一方のディレクトリにコピーします。

  ```bash
  cp ~/workshop/lambda/auto/terraform.tfvars ~/workshop/lambda/manual
  ```

  - _ワークショップの自動計装と手動計装の両方で同じ値を使用するため、このようにコピーします。_

### ファイル権限

その他のファイルはそのままで問題ありませんが、`auto` および `manual` 両方の **send_message.py** スクリプトは、本ワークショップの一部として実行する必要があります。そのため、想定どおりに実行できるよう適切な権限を付与する必要があります。以下の手順に従って設定してください。

- まず、`lambda` ディレクトリにいることを確認します。

  ```bash
  cd ~/workshop/lambda
  ```

- 次に、以下のコマンドを実行して `send_message.py` スクリプトに実行権限を付与します。

  ```bash
  sudo chmod 755 auto/send_message.py manual/send_message.py
  ```

これで前提条件の準備が整いましたので、ワークショップを開始しましょう！
