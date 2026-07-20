---
title: Database Monitoring
time: 2 minutes
weight: 5
description: このラボでは、AppDynamics Database Visibility Monitoringについて学びます。
---

## 目標

このラボでは、AppDynamics Database Visibility Monitoringについて学びます。

このラボを完了すると、以下のことができるようになります。

- AppDynamics Database Visibility Agentをダウンロードする
- AppDynamics Database Visibility Agentをインストールする
- ControllerでDatabase Collectorを構成する
- データベースの正常性をモニタリングする
- データベースのパフォーマンス問題をトラブルシューティングする

## ワークショップ環境

ラボ環境には2つのホストがあります。

- 最初のホストはAppDynamics Controllerを実行しており、以降はControllerと呼びます。
- 2番目のホストはラボで使用するSupercar Traderアプリケーションを実行しています。このホストにAppDynamicsエージェントをインストールします。以降はApplication VMと呼びます。

## Controller VM

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar TraderはJavaベースのWebアプリケーションです。

Supercar-Traderコレクションの目的は、AppDynamics Controllerに対して動的なトラフィック（ビジネストランザクション）を生成することです。

![Application](images/application-vm.png)
