---
title: セットアップ（インストラクター）
linkTitle: 1. セットアップ（インストラクター）
weight: 1
time: 5 minutes
---

インストラクターがユーザーをセットアップし、各ユーザーにterraformの実行と必要なアーティファクトのビルドに使用できる `access key id` と `secret access key` を提供します。

### 前提条件

受講者全員に `Splunk4Ninjas - Observability` インスタンスが必要です。

クラスの準備として、インストラクターのマシンには以下が必要です。

* AWS CLI
* Terraform

AWSアクセスポータルにアクセスしたら、**access keys** をクリックして、次のステップを実行する前にターミナルにコピーします。

![Access Keys](../images/14_aws_keys.png)

### IAMロールの作成（ワークショップインストラクターのみ）

``` bash
# Copy access keys into terminal first before running these steps
cd ~/workshop/lambda/iam_role
terraform init
terraform plan
terraform apply
# enter yes

# Then display the secret
terraform output -raw workshop_secret_access_key
```

### クラスへの提供情報

* `workshop_access_key_id`: `terraform apply` の実行後に表示されます
* `workshop_secret_access_key`: `terraform output` で後から出力したキーです

ダブルクォートの末尾やその他の余分な文字がないか注意してください。

### クリーンアップ

{{< notice warning >}}
ワークショップ完了後、以下の手順でクリーンアップすることが重要です。そうしないと、AWSへのアクセスが開いたままになったり、Lambdaやその他のリソースが実行中のままになる可能性があります。
{{< /notice >}}

``` bash
cd ~/workshop/lambda/iam_role
terraform destroy
```

ワークショップ中に受講者が削除しなかったアーティファクトもクリーンアップする必要があります。以下を確認してください。

1. AWS API Gateway
2. Lambda Functions
3. Kinesis Stream
4. CloudWatch Log Groups
5. S3 Bucket
