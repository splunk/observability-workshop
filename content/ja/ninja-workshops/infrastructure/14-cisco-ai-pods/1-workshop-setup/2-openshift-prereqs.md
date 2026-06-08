---
title: OpenShift の前提条件
linkTitle: 2. OpenShift の前提条件
weight: 2
time: 15 minutes
---

以下の手順は、AWS に OpenShift クラスターをデプロイする前に必要です。

## Red Hat ログインの作成

最初に行う必要があるのは、Red Hat のアカウントを作成することです。[こちらのフォーム](https://www.redhat.com/wapps/ugc/register.html?_flowId=register-flow&_flowExecutionKey=e1s1)に記入して作成できます。

## AWS CLI のインストール

以前にプロビジョニングした EC2 インスタンスに AWS CLI をインストールするには、以下のコマンドを実行します

``` bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
```

以下のコマンドを使用して、正常にインストールされたことを確認します

``` bash
aws --version
```

以下のような出力が返されるはずです

```test
aws-cli/2.30.5 Python/3.13.7 Linux/6.14.0-1011-aws exe/x86_64.ubuntu.24
```

お好みの方法で AWS アカウントにログインしてください。詳しくは[ドキュメント](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html)を参照してください。例えば、`aws configure` コマンドを実行してログインできます。

`aws ec2 describe-instances` などのコマンドを実行して、正常にログインできていることを確認します。

次に、アカウント ID を確認します

``` bash
aws sts get-caller-identity
```

ELB (Elastic Load Balancing) のサービスロールが存在するかどうかを確認します

``` bash
aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing"
```

ロールが存在しない場合は、以下のコマンドを実行して作成します

``` bash
aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
```

## ROSA CLI のインストール

デプロイメントには ROSA コマンドラインインターフェース (CLI) を使用します。手順は [Red Hat ドキュメント](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws_classic_architecture/4/html-single/install_rosa_classic_clusters/index#rosa-installing-and-configuring-the-rosa-cli_rosa-installing-cli)に基づいています。

お使いのオペレーティングシステム向けの最新リリースの ROSA CLI は[こちら](https://console.redhat.com/openshift/downloads)からダウンロードできます。

または、以下のコマンドを使用して、CLI バイナリを EC2 インスタンスに直接ダウンロードすることもできます

```bash
curl -L -O https://mirror.openshift.com/pub/cgw/rosa/latest/rosa-linux.tar.gz
```

コンテンツを展開します

```bash
tar -xvzf rosa-linux.tar.gz
```

生成されたファイル (`rosa`) をパスに含まれる場所に移動します。例

```bash
sudo mv rosa /usr/local/bin/rosa
```

以下のコマンドを実行して Red Hat アカウントにログインし、コマンド出力の指示に従います

```bash
rosa login --use-device-code
```

## OpenShift CLI (oc) のインストール

以下のコマンドを使用して、OpenShift CLI バイナリを EC2 インスタンスに直接ダウンロードできます

```bash
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
```

コンテンツを展開します

```bash
tar -xvzf openshift-client-linux.tar.gz
```

生成されたファイル (`oc` と `kubectl`) をパスに含まれる場所に移動します。例

```bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## アカウント全体のロールとポリシーの作成

以下のコマンドを使用して、必要なアカウント全体のロールとポリシーを作成します

``` bash
rosa create account-roles --mode auto
```

## ROSA HCP 用の AWS VPC の作成

OpenShift クラスターのデプロイには、Hosted Control Plane (HCP) デプロイメントオプションを使用します。これを行うには、以下のコマンドを使用して AWS アカウントに新しい VPC を作成する必要があります

> [!NOTE]
> お使いの環境に合わせてリージョンを更新してください。

``` bash
rosa create network network-template --param Region=us-east-2 --param Name=rosa-network-stack --template-dir='.'
```

> [!IMPORTANT]
> このコマンドの結果として作成されるサブネット ID をメモしておいてください。クラスターを作成する際に必要になります。また、ネットワークを削除する際に必要となる CloudFormation スタック名もメモしておいてください。

---

> [!NOTE]
> デフォルトでは、各 AWS リージョンの Elastic IP アドレスは 5 つに制限されています。
> 次のエラーが表示された場合
> "The maximum number of addresses has been reached."
> AWS に連絡してこの制限の引き上げをリクエストするか、ROSA 用の VPC を作成する別の AWS リージョンを選択する必要があります。

## OpenID Connect 設定の作成

Red Hat OpenShift Service on AWS クラスターを作成する前に、以下のコマンドで OpenID Connect (OIDC) 設定を作成します

``` bash
rosa create oidc-config --mode=auto --yes
```

> [!IMPORTANT]
> 作成された oidc-provider ID をメモしておいてください。
