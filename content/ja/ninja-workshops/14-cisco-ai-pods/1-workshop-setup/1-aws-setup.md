---
title: AWSセットアップ
linkTitle: 1. AWSセットアップ
weight: 1
time: 10 minutes
---

## AWSでRed Hat OpenShiftサービスを有効にする

AWSアカウントにOpenShiftをデプロイするには、まず[AWSコンソール](https://us-east-1.console.aws.amazon.com/rosa/home?region=us-east-1#/)を使用してRed Hat OpenShiftサービスを有効にする必要があります。

次に、AWSアカウントをRed Hatアカウントに接続する手順に従ってください。

## EC2インスタンスのプロビジョニング

Red Hatクラスターをデプロイするために使用するEC2インスタンスをプロビジョニングしましょう。これにより、Mac OSでROSAコマンドラインインターフェースを実行する際の制限を回避できます。

このワークショップの作成時にはUbuntu 24.04 LTSを使用したt3.xlargeインスタンスタイプを使用しましたが、より小さなインスタンスタイプも使用できます。

インスタンスが起動したら、sshで接続してください。

## GitHubリポジトリのクローン

GitHubリポジトリをEC2インスタンスにクローンします：

``` bash
git clone https://github.com/splunk/observability-workshop.git

cd observability-workshop/workshop/cisco-ai-pods
```
