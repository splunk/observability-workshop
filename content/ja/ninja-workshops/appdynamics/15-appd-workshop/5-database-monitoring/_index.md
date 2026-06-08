---
title: Database Monitoring
time: 2 minutes
weight: 5
description: このラボでは、AppDynamics Database Visibility Monitoring について学びます。
---

## 目標

このラボでは、AppDynamics Database Visibility Monitoring について学びます。

このラボを完了すると、以下のことができるようになります

- AppDynamics Database Visibility Agent をダウンロードする。
- AppDynamics Database Visibility Agent をインストールする。
- Controller で Database Collector を構成する。
- データベースの健全性を監視する。
- データベースのパフォーマンス問題をトラブルシューティングする。

## ワークショップ環境

ラボ環境には2つのホストがあります

- 最初のホストは AppDynamics Controller を実行しており、以降は Controller と呼びます。
- 2番目のホストはラボで使用する Supercar Trader アプリケーションを実行しています。このホストに AppDynamics エージェントをインストールします。以降は Application VM と呼びます。

## Controller VM

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar Trader は Java ベースの Web アプリケーションです。

Supercar-Trader コレクションの目的は、AppDynamics Controller 用の動的なトラフィック（ビジネストランザクション）を生成することです。

![Application](images/application-vm.png)
