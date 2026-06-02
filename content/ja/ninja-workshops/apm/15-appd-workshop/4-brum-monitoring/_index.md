---
title: Browser Real User Monitoring (BRUM)
time: 2 minutes
weight: 4
description: このLearning Labでは、AppDynamicsを使用してブラウザベースのアプリケーションのヘルスを監視する方法を学びます。
---

## 目的

このLearning Labでは、AppDynamicsを使用してブラウザベースのアプリケーションのヘルスを監視する方法を学びます。

このラボを完了すると、以下を実施できるようになります。

- Controllerでブラウザアプリケーションを作成する
- Browser Real User Monitoring (BRUM) エージェントを構成して、Webアプリケーションのヘルスを監視する
- パフォーマンス問題のトラブルシューティングを行い、トランザクションのブラウザ側とサーバー側のどちらで発生しているかにかかわらず、根本原因を特定する

## ワークショップ環境

ワークショップ環境には2つのホストがあります。

- 1つ目のホストはAppDynamics Controllerを実行しており、以降はControllerと呼びます。
- 2つ目のホストはラボで使用するSupercar Traderアプリケーションを実行しています。AppDynamicsエージェントをインストールするホストであり、以降はApplication VMと呼びます。

## Controller

このワークショップでは、 [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar TraderはJavaベースのWebアプリケーションです。

Supercar-Traderコレクションの目的は、AppDynamics Controller向けに動的なトラフィック（ビジネストランザクション）を生成することです。

![Application VM](images/application-vm.png)
