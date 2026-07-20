---
title: Browser Real User Monitoring (BRUM)
time: 2 minutes
weight: 4
description: このラーニングラボでは、AppDynamicsを使用してブラウザベースのアプリケーションの健全性をモニタリングする方法を学びます。
---

## 目的

このラーニングラボでは、AppDynamicsを使用してブラウザベースのアプリケーションの健全性をモニタリングする方法を学びます。

このラボを完了すると、以下のことができるようになります。

- Controllerでブラウザアプリケーションを作成する
- Browser Real User Monitoring（BRUM）エージェントを設定して、Webアプリケーションの健全性をモニタリングする
- パフォーマンスの問題をトラブルシューティングし、ブラウザ側またはサーバー側のどちらで発生しているかに関わらず根本原因を特定する

## ワークショップ環境

ワークショップ環境には2つのホストがあります。

- 最初のホストはAppDynamics Controllerを実行しており、以降はControllerと呼びます。
- 2番目のホストはラボで使用するSupercar Traderアプリケーションを実行しています。このホストにAppDynamicsエージェントをインストールするため、以降はApplication VMと呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar TraderはJavaベースのWebアプリケーションです。

Supercar-Traderコレクションの目的は、AppDynamics Controllerに対して動的なトラフィック（ビジネストランザクション）を生成することです。

![Application VM](images/application-vm.png)
