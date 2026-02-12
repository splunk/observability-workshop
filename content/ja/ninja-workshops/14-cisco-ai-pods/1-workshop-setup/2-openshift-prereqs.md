---
title: OpenShiftの前提条件
linkTitle: 2. OpenShiftの前提条件
weight: 2
time: 15 minutes
---

以下の手順は、AWSにOpenShiftクラスターをデプロイする前に必要です。

## Red Hatログインの作成

最初に行う必要があるのは、Red Hatのアカウントを作成することです。[こちら](https://www.redhat.com/wapps/ugc/register.html?_flowId=register-flow&_flowExecutionKey=e1s1)のフォームに記入して作成できます。

## AWS CLIのインストール

以前プロビジョニングしたEC2インスタンスにAWS CLIをインストールするには、以下のコマンドを実行します：

``` bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
```

以下のコマンドを使用して、正常にインストールされたことを確認します：

``` bash
aws --version
```

以下のような結果が返されるはずです：

````
aws-cli/2.30.5 Python/3.13.7 Linux/6.14.0-1011-aws exe/x86_64.ubuntu.24
````

お好みの方法でAWSアカウントにログインしてください。ガイダンスについては[ドキュメント](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html)を参照してください。例えば、`aws configure`コマンドを実行してログインできます。

`aws ec2 describe-instances`などのコマンドを実行して、正常にログインできていることを確認してください。

次に、以下のコマンドでアカウントIDを確認します：

``` bash
aws sts get-caller-identity
```

ELB (Elastic Load Balancing)のサービスロールが存在するかどうかを確認します：

``` bash
aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing"
```

ロールが存在しない場合は、以下のコマンドを実行して作成します：

``` bash
aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
```

## ROSA CLIのインストール

デプロイにはROSAコマンドラインインターフェース (CLI)を使用します。手順は[Red Hatドキュメント](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws_classic_architecture/4/html-single/install_rosa_classic_clusters/index#rosa-installing-and-configuring-the-rosa-cli_rosa-installing-cli)に基づいています。

お使いのオペレーティングシステム用のROSA CLIの最新リリースは[こちら](https://console.redhat.com/openshift/downloads)からダウンロードできます。

または、以下のコマンドを使用してCLIバイナリをEC2インスタンスに直接ダウンロードすることもできます：

````
curl -L -O https://mirror.openshift.com/pub/cgw/rosa/latest/rosa-linux.tar.gz
````

コンテンツを解凍します：

````
tar -xvzf rosa-linux.tar.gz
````

結果のファイル(`rosa`)をパスに含まれている場所に移動します。例えば：

``` bash
sudo mv rosa /usr/local/bin/rosa
```

以下のコマンドを実行してRed Hatアカウントにログインし、コマンド出力の指示に従ってください：

````
rosa login --use-device-code
````

## OpenShift CLI (oc)のインストール

以下のコマンドを使用して、OpenShift CLIバイナリをEC2インスタンスに直接ダウンロードできます：

````
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
````

コンテンツを解凍します：

````
tar -xvzf openshift-client-linux.tar.gz
````

結果のファイル(`oc`と`kubectl`)をパスに含まれている場所に移動します。例えば：

``` bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## アカウント全体のロールとポリシーの作成

以下のコマンドを使用して、必要なアカウント全体のロールとポリシーを作成します：

``` bash
rosa create account-roles --mode auto
```

## ROSA HCP用のAWS VPCの作成

OpenShiftクラスターをデプロイするために、Hosted Control Plane (HCP)デプロイオプションを使用します。これを行うには、以下のコマンドを使用してAWSアカウントに新しいVPCを作成する必要があります：

> 注意: リージョンを環境に合わせて更新してください。

``` bash
rosa create network network-template --param Region=us-east-2 --param Name=rosa-network-stack --template-dir='.'
```

> 重要: このコマンドの結果として作成されたサブネットIDをメモしておいてください。クラスターを作成する際に必要になります。また、ネットワークを削除する場合に後で必要になるCloudFormationスタック名もメモしておいてください。

> 注意: デフォルトでは、各AWSリージョンはElastic IPアドレスが5つに制限されています。「The maximum number of addresses has been reached.」というエラーが発生した場合は、AWSに連絡してこの制限の引き上げをリクエストするか、ROSA用のVPCを作成するために別のAWSリージョンを選択する必要があります。

## OpenID Connect設定の作成

Red Hat OpenShift Service on AWSクラスターを作成する前に、以下のコマンドでOpenID Connect (OIDC)設定を作成しましょう：

``` bash
rosa create oidc-config --mode=auto --yes
```

> 重要: 作成されたoidc-provider idをメモしておいてください。
