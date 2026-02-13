---
title: Application Performance Monitoring (APM)
time: 2 minutes
weight: 1
description: このラボでは、Splunk AppDynamics を使用してアプリケーションサービスの健全性を監視する方法を学びます。
---

## 目標

このラボでは、AppDynamicsを使用してアプリケーションサービスの健全性を監視する方法を学びます。このワークショップの他のラボを開始する前に、まずこのラボを完了する必要があります。

このラボを完了すると、以下のことができるようになります：

- AppDynamics Java APM Agentをダウンロードする
- AppDynamics Java APM Agentをインストールする
- サンプルアプリケーションに負荷を発生させる
- AppDynamics APMの基本概念を理解する
- Controllerで収集設定を構成する
- アプリケーションの健全性を監視する
- アプリケーションのパフォーマンス問題をトラブルシューティングして根本原因を特定する
- AppDynamicsがキャプチャしたデータに基づいてAppDynamicsの監視サービスでアラートを監視する

## ワークショップ環境

ワークショップ環境には2つのホストがあります：

- 1つ目のホストはAppDynamics Controllerを実行しており、以降はControllerと呼びます。
- 2つ目のホストはラボで使用するSupercar Traderアプリケーションを実行しています。ここにAppDynamicsエージェントをインストールするホストであり、以降はApplication VMと呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar TraderはJavaベースのWebアプリケーションです。

Supercar-Traderコレクションの目的は、AppDynamics Controllerのための動的なトラフィック（Business Transactions）を生成することです。

![Application VM](images/application-vm.png)
