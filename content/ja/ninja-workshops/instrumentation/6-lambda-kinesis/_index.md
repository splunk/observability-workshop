---
title: AWS Lambda Functions の分散トレーシング
linkTitle: Lambda Tracing
description: AWS Kinesis ストリームで接続された AWS Lambda のプロデューサーとコンシューマー間で分散トレースを構築します。
weight: 6
authors: ["Kate Hymers", "Guy-Francis Kono", "Updates: Bill Grant"]
time: 45 minutes
aliases:
  - /ninja-workshops/6-lambda-kinesis/
---

このワークショップでは、AWS Lambda 上で動作する小規模なサーバーレスアプリケーションに対して、AWS Kinesis を介したメッセージの生成と消費を含む分散トレースを構築する方法を学びます。

まず、OpenTelemetry の自動計装がトレースをキャプチャし、選択したターゲットにエクスポートする仕組みを確認します。

次に、手動計装でコンテキスト伝播を有効にする方法を確認します。

このワークショップでは、Splunk が事前設定済みの Ubuntu Linux インスタンスを AWS/EC2 に用意しています。インスタンスにアクセスするには、ワークショップの講師が提供する URL にアクセスしてください。
