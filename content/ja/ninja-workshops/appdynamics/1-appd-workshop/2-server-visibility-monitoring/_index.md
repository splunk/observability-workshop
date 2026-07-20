---
title: Server Visibility Monitoring
time: 2 minutes
weight: 2
description: このラボでは、AppDynamics Server Visibility MonitoringとService Availability Monitoringについて学びます。
---

{{% notice title="前提条件" style="primary"  icon="lightbulb" %}}
これはApplication Performance Monitoringラボの続きです。アプリケーションが実行中で、過去1時間にわたって負荷がかかっていることを確認してください。必要に応じて、Generate Application Loadセクションに戻り、ロードジェネレーターを再起動してください。
{{% /notice %}}

## 目的

このラボでは、AppDynamics Server Visibility MonitoringとService Availability Monitoringについて学びます。

このラボを完了すると、以下のことができるようになります。

- AppDynamics Server Visibility Agentをダウンロードする。
- AppDynamics Server Visibility Agentをインストールする。
- サーバーの正常性をモニタリングする。
- エージェントの拡張ハードウェアメトリクスを理解する。
- アプリケーションパフォーマンスに影響を与えている基盤インフラストラクチャの問題を素早く確認する。

## ワークショップ環境

ラボ環境には2つのホストがあります。

- 最初のホストはAppDynamics Controllerを実行しており、以降はControllerと呼びます。
- 2番目のホストはラボで使用するSupercar Traderアプリケーションを実行しています。このホストにAppDynamicsエージェントをインストールします。以降はApplication VMと呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar TraderはJavaベースのWebアプリケーションです。

Supercar-Traderコレクションの目的は、AppDynamics Controllerに対して動的なトラフィック（ビジネストランザクション）を生成することです。

![Application VM](images/application-vm.png)
