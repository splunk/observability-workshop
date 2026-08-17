---
title: Database Monitoring
time: 2 minutes
weight: 5
description: このラボでは、AppDynamics Database Visibility Monitoring について学びます。
---

## 目標

このラボでは、AppDynamics Database Visibility Monitoringについて学びます。

このラボを完了すると、以下のことができるようになります

- AppDynamics Database Visibility Agentのダウンロード
- AppDynamics Database Visibility Agentのインストール
- ControllerでのDatabase Collectorの構成
- データベースの健全性監視
- データベースパフォーマンス問題のトラブルシューティング

## ワークショップ環境

ラボ環境には2つのホストがあります

- 1つ目のホストはAppDynamics Controllerを実行しており、以降はControllerと呼びます。
- 2つ目のホストはラボで使用するSupercar Traderアプリケーションを実行しています。このホストにAppDynamicsエージェントをインストールし、以降はApplication VMと呼びます。

## Controller VM

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar TraderはJavaベースのWebアプリケーションです。

Supercar-Traderコレクションの目的は、AppDynamics Controller向けに動的なトラフィック（ビジネストランザクション）を生成することです。

![Application](images/application-vm.png)
