---
title: Application Performance Monitoring (APM)
time: 2 minutes
weight: 1
description: このラボでは、Splunk AppDynamics を使用してアプリケーションサービスの健全性を監視する方法を学びます。
---

## 目的

このラボでは、AppDynamics を使用してアプリケーションサービスの健全性を監視する方法を学びます。本ワークショップの他のラボを開始する前に、まずこのラボを完了する必要があります。

このラボを完了すると、以下のことができるようになります。

- AppDynamics Java APM Agent をダウンロードする。
- AppDynamics Java APM Agent をインストールする。
- サンプルアプリケーションに負荷をかけて初期化する。
- AppDynamics APM のコアコンセプトを理解する。
- Controller でコレクション設定を構成する。
- アプリケーションの健全性を監視する。
- アプリケーションパフォーマンスの問題をトラブルシューティングし、根本原因を特定する。
- AppDynamics によって収集されたデータに基づいて、AppDynamics の監視サービスのアラートを監視する。

## ワークショップ環境

ワークショップ環境には 2 つのホストがあります。

- 1 つ目のホストは AppDynamics Controller を実行しており、以降「Controller」と呼びます。
- 2 つ目のホストはラボで使用する Supercar Trader アプリケーションを実行しています。AppDynamics エージェントをインストールするホストであり、以降「Application VM」と呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar Trader は Java ベースの Web アプリケーションです。

Supercar-Trader collection の目的は、AppDynamics Controller のために動的なトラフィック（Business Transactions）を生成することです。

![Application VM](images/application-vm.png)
