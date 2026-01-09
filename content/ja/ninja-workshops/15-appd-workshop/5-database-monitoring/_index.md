---
title: Database Monitoring
time: 2 minutes
weight: 5
description: このラボでは、AppDynamics Database Visibility Monitoring について学びます。
---

## 目標

このラボでは、AppDynamics Database Visibility Monitoring について学びます。

このラボを完了すると、以下のことができるようになります：

- AppDynamics Database Visibility Agent のダウンロード
- AppDynamics Database Visibility Agent のインストール
- Controller での Database Collector の構成
- データベースの健全性監視
- データベースパフォーマンス問題のトラブルシューティング

## ワークショップ環境

ラボ環境には2つのホストがあります：

- 1つ目のホストは AppDynamics Controller を実行しており、以降は Controller と呼びます。
- 2つ目のホストはラボで使用する Supercar Trader アプリケーションを実行しています。このホストに AppDynamics エージェントをインストールし、以降は Application VM と呼びます。

## Controller VM

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar Trader は Java ベースの Web アプリケーションです。

Supercar-Trader コレクションの目的は、AppDynamics Controller 向けに動的なトラフィック（ビジネストランザクション）を生成することです。

![Application](images/application-vm.png)
