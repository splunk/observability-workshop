---
title: Server Visibility Monitoring
time: 2 minutes
weight: 2
description: このラボでは、AppDynamics Server Visibility Monitoring と Service Availability Monitoring について学びます。
---

{{% notice title="前提条件" style="primary"  icon="lightbulb" %}}
このラボはApplication Performance Monitoringラボの続きです。アプリケーションが実行中であり、過去1時間にわたって負荷がかかっていることを確認してください。必要に応じて、Generate Application Loadセクションに戻ってロードジェネレーターを再起動してください。
{{% /notice %}}

## 目標

このラボでは、AppDynamics Server Visibility MonitoringとService Availability Monitoringについて学びます。

このラボを完了すると、以下のことができるようになります：

- AppDynamics Server Visibility Agentをダウンロードする
- AppDynamics Server Visibility Agentをインストールする
- サーバーの健全性を監視する
- エージェントの拡張ハードウェアメトリクスを理解する
- アプリケーションパフォーマンスに影響を与えている基盤インフラストラクチャの問題を迅速に確認する

## ワークショップ環境

ラボ環境には2つのホストがあります：

- 1つ目のホストはAppDynamics Controllerを実行しており、以降はControllerと呼びます。
- 2つ目のホストはラボで使用するSupercar Traderアプリケーションを実行しています。このホストにAppDynamicsエージェントをインストールし、以降はApplication VMと呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar TraderはJavaベースのWebアプリケーションです。

Supercar-Traderコレクションの目的は、AppDynamics Controllerに対して動的なトラフィック（ビジネストランザクション）を生成することです。

![Application VM](images/application-vm.png)
