---
title: AWS Setup
linkTitle: 1. AWS Setup
weight: 1
time: 10 minutes
---

## AWS で Red Hat OpenShift Service を有効にする

AWS アカウントに OpenShift をデプロイするには、まず [AWS コンソール](https://us-east-1.console.aws.amazon.com/rosa/home?region=us-east-1#/) を使用して Red Hat OpenShift サービスを有効にする必要があります。

次に、AWS アカウントと Red Hat アカウントを接続する手順に従ってください。

## EC2 インスタンスのプロビジョニング

Red Hat クラスターのデプロイに使用する EC2 インスタンスをプロビジョニングします。これにより、Mac OS で ROSA コマンドラインインターフェースを実行する際の制限を回避できます。

このワークショップの作成時には、Ubuntu 24.04 LTS を使用した t3.xlarge インスタンスタイプを使用しましたが、より小さいインスタンスタイプも使用できます。

インスタンスが起動したら、ssh で接続します。

## GitHub リポジトリのクローン

GitHub リポジトリを EC2 インスタンスにクローンします

``` bash
git clone https://github.com/splunk/observability-workshop.git

cd observability-workshop/workshop/cisco-ai-pods
```
