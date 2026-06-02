---
title: Server Visibility Monitoring
time: 2 minutes
weight: 2
description: このラボでは、AppDynamics Server Visibility Monitoring と Service Availability Monitoring について学びます。
---

{{% notice title="前提条件" style="primary"  icon="lightbulb" %}}
これは Application Performance Monitoring ラボの続きです。アプリケーションが稼働しており、過去 1 時間分の負荷がかかっていることを確認してください。必要に応じて Generate Application Load セクションに戻り、負荷生成ツールを再起動してください。
{{% /notice %}}

## Objectives

このラボでは、AppDynamics Server Visibility Monitoring と Service Availability Monitoring について学びます。

このラボを完了すると、次のことができるようになります。

- AppDynamics Server Visibility Agent をダウンロードする。
- AppDynamics Server Visibility Agent をインストールする。
- サーバーのヘルス状態を監視する。
- エージェントが提供する拡張ハードウェアメトリクスを理解する。
- アプリケーションのパフォーマンスに影響を及ぼす基盤インフラストラクチャの問題を素早く把握する。

## Workshop Environment

ラボ環境には 2 台のホストがあります。

- 1 台目のホストでは AppDynamics Controller が稼働しており、以降は Controller と呼びます。
- 2 台目のホストでは、ラボで使用する Supercar Trader アプリケーションが稼働しています。このホストには AppDynamics エージェントをインストールするため、以降は Application VM と呼びます。

## Controller

このワークショップでは [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を使用します。

![Controller](images/controller-vm.png)

## Application VM

Supercar Trader は Java ベースの Web アプリケーションです。

Supercar-Trader コレクションの目的は、AppDynamics Controller 向けに動的なトラフィック (ビジネストランザクション) を生成することです。

![Application VM](images/application-vm.png)
