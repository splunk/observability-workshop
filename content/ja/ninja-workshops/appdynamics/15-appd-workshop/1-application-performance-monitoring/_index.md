---
title: Application Performance Monitoring (APM)
time: 2 minutes
weight: 1
description: このラボでは、Splunk AppDynamics を使用してアプリケーションサービスの健全性を監視する方法を学びます。
---

## 目標

このラボでは、AppDynamics を使用してアプリケーションサービスの健全性を監視する方法を学びます。このワークショップの他のラボを始める前に、まずこのラボを完了する必要があります。

このラボを完了すると、以下のことができるようになります

- AppDynamics Java APM Agent をダウンロードする。
- AppDynamics Java APM Agent をインストールする。
- サンプルアプリケーションを負荷で初期化する。
- AppDynamics APM のコアコンセプトを理解する。
- Controller でコレクション設定を構成する。
- アプリケーションの健全性を監視する。
- アプリケーションのパフォーマンス問題をトラブルシューティングして根本原因を特定する。
- AppDynamics がキャプチャしたデータに基づく AppDynamics の監視サービスでアラートを監視する。

## ワークショップ環境

ワークショップ環境には2つのホストがあります

- 最初のホストは AppDynamics Controller を実行しており、以降は Controller と呼びます。
- 2番目のホストはラボで使用する Supercar Trader アプリケーションを実行しています。AppDynamics エージェントをインストールするホストであり、以降は Application VM と呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar Trader は Java ベースの Web アプリケーションです。

Supercar-Trader コレクションの目的は、AppDynamics Controller 向けの動的なトラフィック（Business Transactions）を生成することです。

![Application VM](images/application-vm.png)
