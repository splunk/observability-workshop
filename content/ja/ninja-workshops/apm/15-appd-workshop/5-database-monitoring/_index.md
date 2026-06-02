---
title: Database Monitoring
time: 2 minutes
weight: 5
description: このラボでは、AppDynamics Database Visibility Monitoring について学習します。
---

## 目的

このラボでは、AppDynamics Database Visibility Monitoring について学習します。

このラボを完了すると、次のことができるようになります。

- AppDynamics Database Visibility Agent をダウンロードする。
- AppDynamics Database Visibility Agent をインストールする。
- Controller で Database Collector を構成する。
- データベースのヘルス状態を監視する。
- データベースのパフォーマンス問題をトラブルシュートする。

## ワークショップ環境

ラボ環境には 2 台のホストがあります。

- 1 台目のホストでは AppDynamics Controller が稼働しており、以降このホストを Controller と呼びます。
- 2 台目のホストではラボで使用する Supercar Trader アプリケーションが稼働しています。AppDynamics エージェントをインストールするホストであり、以降このホストを Application VM と呼びます。

## Controller VM

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar Trader は Java ベースの Web アプリケーションです。

Supercar-Trader collection の目的は、AppDynamics Controller 向けに動的なトラフィック（ビジネストランザクション）を生成することです。

![Application](images/application-vm.png)
