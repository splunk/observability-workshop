---
title: Kubernetes における Horizontal Pod Autoscaling のモニタリング
linkTitle: Horizontal Pod Autoscaling
description: Splunk OpenTelemetry Collector で Kubernetes HPA をモニタリングし、スケールアップおよびスケールダウンのイベントをリアルタイムで観察します。
weight: 2
authors: ["Robert Castley"]
time: 45 minutes
aliases:
  - /ninja-workshops/2-hpa/
---

このハンズオンワークショップでは、Splunk OpenTelemetry Collector を使用して Kubernetes の Horizontal Pod Autoscaling (HPA) をモニタリングする方法を学びます。PHP/Apache アプリケーションと負荷生成ツールをデプロイして自動スケーリングイベントを発生させ、スケーリングのライフサイクル全体を観察します。

実践的な演習を通じて、OpenTelemetry Receiver、Kubernetes Namespace、ReplicaSet、および HPA の仕組みを探求しながら、すべてを Splunk Observability Cloud でモニタリングします。Kubernetes Navigator を使いこなし、カスタムダッシュボードを構築し、メトリクスとイベントを分析し、スケーリングアクティビティに対するアラートを通知する Detector を設定します。

このワークショップ用に、Splunk が AWS/EC2 上に Ubuntu Linux インスタンスを事前構成して用意しています。

ワークショップで使用するインスタンスへのアクセス方法については、ワークショップリーダーから提供される URL をご確認ください。
