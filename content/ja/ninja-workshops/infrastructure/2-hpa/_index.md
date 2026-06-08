---
title: Kubernetes における Horizontal Pod Autoscaling の監視
linkTitle: Horizontal Pod Autoscaling
description: Splunk OpenTelemetry Collector を使用して Kubernetes HPA を監視し、スケールアップおよびスケールダウンイベントをリアルタイムで確認します。
weight: 2
authors: ["Robert Castley"]
time: 45 minutes
aliases:
  - /ninja-workshops/2-hpa/
product: "Observability Cloud"
---

このハンズオンワークショップでは、Splunk OpenTelemetry Collector を使用して Kubernetes Horizontal Pod Autoscaling (HPA) を監視する方法を学びます。PHP/Apache アプリケーションとロードジェネレーターをデプロイしてオートスケーリングイベントをトリガーし、スケーリングのライフサイクル全体を観察します。

実践的な演習を通じて、OpenTelemetry Receivers、Kubernetes Namespaces、ReplicaSets、および HPA のメカニズムを探索しながら、すべてを Splunk Observability Cloud で監視します。Kubernetes Navigator の使いこなし、カスタムダッシュボードの構築、メトリクスとイベントの分析、スケーリングアクティビティに対するアラートを設定するディテクターの構成を習得します。

このワークショップでは、Splunk が事前設定済みの AWS/EC2 上の Ubuntu Linux インスタンスを用意しています。

ワークショップで使用するインスタンスにアクセスするには、ワークショップリーダーから提供された URL にアクセスしてください。
