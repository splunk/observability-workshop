---
title: AWS Lambda 関数の分散トレーシング
linkTitle: Lambda Tracing
description: AWS Kinesis ストリームで接続された AWS Lambda の producer と consumer にまたがる分散トレースを構築します。
weight: 6
authors: ["Guy-Francis Kono"]
time: 45 minutes
aliases:
  - /ninja-workshops/6-lambda-kinesis/
---

このワークショップでは、AWS Lambda 上で動作する小規模なサーバーレスアプリケーションについて、AWS Kinesis を介してメッセージを producer と consumer 間でやり取りする際の分散トレースを構築する方法を学びます。

最初に、OpenTelemetry の自動インストルメンテーションがトレースをキャプチャし、任意のターゲットへエクスポートする仕組みを確認します。

次に、手動インストルメンテーションによってコンテキスト伝搬を有効化する方法を確認します。

このワークショップのために、Splunk では事前構成済みの Ubuntu Linux インスタンスを AWS/EC2 上に用意しています。このインスタンスにアクセスするには、ワークショップリーダーから提供される URL にアクセスしてください。
