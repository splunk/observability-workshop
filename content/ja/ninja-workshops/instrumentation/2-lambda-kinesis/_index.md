---
title: AWS Lambda関数の分散トレーシング
linkTitle: Lambda Tracing
description: AWS Kinesisストリームで接続されたAWS Lambdaのプロデューサーとコンシューマーにまたがる分散トレースを構築します。
weight: 2
authors: ["Kate Hymers", "Guy-Francis Kono", "Updates: Bill Grant"]
time: 45 minutes
aliases:
  - /ninja-workshops/6-lambda-kinesis/
---

このワークショップでは、AWS Lambda上で動作する小規模なサーバーレスアプリケーションに対して、AWS Kinesisを介したメッセージの生成と消費における分散トレースを構築する方法を学びます。

まず、OpenTelemetryの自動計装がどのようにトレースをキャプチャし、任意のターゲットにエクスポートするかを確認します。

次に、手動計装によってコンテキスト伝播を有効にする方法を確認します。

このワークショップでは、Splunkが事前設定済みのAWS/EC2上のUbuntu Linuxインスタンスを用意しています。インスタンスにアクセスするには、ワークショップの講師が提供するURLにアクセスしてください。
