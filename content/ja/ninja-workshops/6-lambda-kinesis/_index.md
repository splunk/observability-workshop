---
title: AWS Lambda関数の分散トレーシング
linkTitle: Lambdaトレーシング
description: このワークショップでは、AWS Lambdaで実行される小規模なサーバーレスアプリケーションの分散トレースを構築し、AWS Kinesisを介してメッセージをproduceおよびconsumeする方法を学びます
weight: 6
authors: ["Guy-Francis Kono"]
time: 45 minutes
---

このワークショップでは、AWS Lambda で実行される小規模なサーバーレスアプリケーションの分散トレースを構築し、AWS Kinesis を介してメッセージを produce および consume する方法を学びます。

まず、OpenTelemetry の自動計装がどのようにトレースをキャプチャし、選択した宛先にエクスポートするかを確認します。

次に、手動計装によってコンテキスト伝播を有効にする方法を見ていきます。

このワークショップのために、Splunk は AWS/EC2 上の Ubuntu Linux インスタンスを事前に構成しています。このインスタンスにアクセスするには、ワークショップインストラクターが提供する URL にアクセスしてください。
