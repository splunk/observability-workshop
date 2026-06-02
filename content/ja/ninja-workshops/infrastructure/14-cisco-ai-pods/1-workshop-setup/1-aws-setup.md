---
title: AWS Setup
linkTitle: 1. AWS Setup
weight: 1
time: 10 minutes
---

## AWS で Red Hat OpenShift サービスを有効化する

AWS アカウントに OpenShift をデプロイするために、まず [AWS console](https://us-east-1.console.aws.amazon.com/rosa/home?region=us-east-1#/) を使用して Red Hat OpenShift サービスを有効化する必要があります。

次に、画面の指示に従って AWS アカウントと Red Hat アカウントを連携させます。

## EC2 インスタンスをプロビジョニングする

Red Hat クラスターのデプロイに使用する EC2 インスタンスをプロビジョニングしましょう。これにより、Mac OS 上で ROSA コマンドラインインターフェースを実行する際の制約を回避できます。

ワークショップを作成する際には、Ubuntu 24.04 LTS を使用した t3.xlarge インスタンスタイプを使用しましたが、より小さいインスタンスタイプでも利用可能です。

インスタンスが起動したら、ssh で接続してください。

## GitHub リポジトリをクローンする

EC2 インスタンスに GitHub リポジトリをクローンします。

``` bash
git clone https://github.com/splunk/observability-workshop.git

cd observability-workshop/workshop/cisco-ai-pods 
```
