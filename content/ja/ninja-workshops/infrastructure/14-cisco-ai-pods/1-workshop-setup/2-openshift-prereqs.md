---
title: OpenShift Prerequisites
linkTitle: 2. OpenShift Prerequisites
weight: 2
time: 15 minutes
---

以下の手順は、AWS に OpenShift クラスターをデプロイする前に必要となるものです。

## Create a Red Hat Login

最初に行う必要があるのは、Red Hat のアカウント作成です。
[こちら](https://www.redhat.com/wapps/ugc/register.html?_flowId=register-flow&_flowExecutionKey=e1s1)
のフォームに入力することで作成できます。

## Install the AWS CLI

事前にプロビジョニングした EC2 インスタンスに AWS CLI をインストールするには、以下のコマンドを実行します。

``` bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
```

以下のコマンドを使用して、正常にインストールされたことを確認します。

``` bash
aws --version
```

次のような出力が返されるはずです。

````
aws-cli/2.30.5 Python/3.13.7 Linux/6.14.0-1011-aws exe/x86_64.ubuntu.24
````

任意の方法で AWS アカウントにログインします。手順については
[ドキュメント](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html)
を参照してください。例えば、`aws configure` コマンドを実行してログインできます。

`aws ec2 describe-instances` などのコマンドを実行して、正常にログインできているか確認します。

その後、以下のコマンドでアカウントの ID を確認します。

``` bash
aws sts get-caller-identity
```

ELB（Elastic Load Balancing）のサービスロールが存在するかを確認します。

``` bash
aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing"
```

ロールが存在しない場合は、以下のコマンドを実行して作成します。

``` bash
aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
```

## Install the ROSA CLI

デプロイには ROSA コマンドラインインターフェース（CLI）を使用します。手順は
[Red Hat のドキュメント](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws_classic_architecture/4/html-single/install_rosa_classic_clusters/index#rosa-installing-and-configuring-the-rosa-cli_rosa-installing-cli)
に基づいています。

お使いのオペレーティングシステム向けの ROSA CLI の最新リリースは
[こちら](https://console.redhat.com/openshift/downloads)からダウンロードできます。

代わりに、以下のコマンドを使用して CLI バイナリを EC2 インスタンスに直接ダウンロードすることもできます。

````
curl -L -O https://mirror.openshift.com/pub/cgw/rosa/latest/rosa-linux.tar.gz
````

内容を展開します。

````
tar -xvzf rosa-linux.tar.gz
````

展開されたファイル（`rosa`）を、パスに含まれる場所に移動します。例えば次のようにします。

``` bash
sudo mv rosa /usr/local/bin/rosa
```

以下のコマンドを実行して Red Hat アカウントにログインし、コマンド出力の指示に従います。

````
rosa login --use-device-code
````

## Install the OpenShift CLI (oc)

以下のコマンドを使用して、OpenShift CLI バイナリを EC2 インスタンスに直接ダウンロードできます。

````
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
````

内容を展開します。

````
tar -xvzf openshift-client-linux.tar.gz
````

展開されたファイル（`oc` および `kubectl`）を、パスに含まれる場所に移動します。例えば次のようにします。

``` bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## Create Account-Wide Roles and Policies

以下のコマンドを使用して、必要なアカウント全体のロールとポリシーを作成します。

``` bash
rosa create account-roles --mode auto
```

## Create an AWS VPC for ROSA HCP

OpenShift クラスターのデプロイには、Hosted Control Plane（HCP）デプロイオプションを使用します。
これを行うには、以下のコマンドを使用して AWS アカウントに新しい VPC を作成する必要があります。

> Note: お使いの環境に合わせてリージョンを更新してください。

``` bash
rosa create network network-template --param Region=us-east-2 --param Name=rosa-network-stack --template-dir='.'
```

> Important: このコマンドの結果として作成されるサブネット ID は、クラスター作成時に必要になるので
> メモしておいてください。また、後でネットワークを削除する際に必要になるため、CloudFormation
> スタック名もメモしておいてください。

> Note: デフォルトでは、各 AWS リージョンは 5 つの Elastic IP アドレスに制限されています。
> 以下のエラーが表示された場合：
> "The maximum number of addresses has been reached."
> AWS に連絡してこの上限の引き上げをリクエストするか、
> ROSA 用の VPC を作成する別の AWS リージョンを選択する必要があります。

## Create an OpenID Connect configuration

Red Hat OpenShift Service on AWS クラスターを作成する前に、以下のコマンドで
OpenID Connect（OIDC）設定を作成します。

``` bash
rosa create oidc-config --mode=auto --yes
```

> Important: 作成された oidc-provider id をメモしておいてください。
