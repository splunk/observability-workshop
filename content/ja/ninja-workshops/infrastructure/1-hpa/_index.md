---
title: KubernetesにおけるHorizontal Pod Autoscalingのモニタリング
linkTitle: Horizontal Pod Autoscaling
description: Splunk OpenTelemetry CollectorでKubernetes HPAをモニタリングし、スケールアップおよびスケールダウンイベントをリアルタイムで監視します。
weight: 1
authors: ["Robert Castley"]
time: 45 minutes
aliases:
  - /ninja-workshops/2-hpa/
product: "Observability Cloud"
---

このハンズオンワークショップでは、Splunk OpenTelemetry Collectorを使用してKubernetes Horizontal Pod Autoscaling（HPA）をモニタリングする方法を学びます。PHP/Apacheアプリケーションとロードジェネレーターをデプロイしてオートスケーリングイベントをトリガーし、スケーリングのライフサイクル全体を観察します。

実践的な演習を通じて、OpenTelemetry Receiver、Kubernetes Namespace、ReplicaSet、およびHPAの仕組みを探りながら、すべてをSplunk Observability Cloudでモニタリングします。Kubernetes Navigatorの使いこなし、カスタムダッシュボードの構築、メトリクスとイベントの分析、スケーリングアクティビティに対するアラートを設定するDetectorの構成を習得します。

このワークショップでは、SplunkがAWS/EC2上に事前設定済みのUbuntu Linuxインスタンスを用意しています。

ワークショップで使用するインスタンスにアクセスするには、ワークショップの講師から提供されるURLにアクセスしてください。
