---
title: Browser Real User Monitoring (BRUM)
time: 2 minutes
weight: 4
description: このラーニングラボでは、AppDynamics を使用してブラウザベースのアプリケーションの健全性を監視する方法を学びます。
---

## 目標

このラーニングラボでは、AppDynamics を使用してブラウザベースのアプリケーションの健全性を監視する方法を学びます。

このラボを完了すると、以下のことができるようになります

- Controller でブラウザアプリケーションを作成する
- Browser Real User Monitoring (BRUM) エージェントを設定して、Web アプリケーションの健全性を監視する
- パフォーマンスの問題をトラブルシューティングし、ブラウザ側またはサーバー側のどちらで発生しているかに関わらず、根本原因を特定する

## ワークショップ環境

ワークショップ環境には2つのホストがあります

- 最初のホストは AppDynamics Controller を実行しており、以降は Controller と呼びます。
- 2番目のホストはラボで使用する Supercar Trader アプリケーションを実行しています。このホストに AppDynamics エージェントをインストールするため、以降は Application VM と呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar Trader は Java ベースの Web アプリケーションです。

Supercar-Trader コレクションの目的は、AppDynamics Controller のために動的なトラフィック（ビジネストランザクション）を生成することです。

![Application VM](images/application-vm.png)
