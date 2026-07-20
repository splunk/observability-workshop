---
draft: true
title: Context Propagation
linkTitle: Context Propagation
weight: 5
layout: chapter
time: 90 minutes
authors: ["Diana Omuoyo"]
description: プロキシやメッセージバスがW3Cトレースコンテキストをドロップすると、分散トレーシングはサイレントに破損します。このワークショップでは、一般的なコンテキストと相関の断絶を含むサンプルEコマースアプリケーションを使用します
aliases:
  - /ninja-workshops/20-context-propagation/
---

## 概要

このワークショップでは、天文機器のストアフロントである **Cosmic Observatory Shop** をデプロイし、Splunk RUMとSplunk APMで計装します。

必要なW3Cヘッダーが以下の **3つ** のレイヤーで除去された際に、サービスマップとトレースが断片化する様子を観察します。

1. **Edge NGINX gateway** - W3Cトレースヘッダーをドロップ（frontend-api → order API）
2. **Payment gateway proxy** - 計装済みNode.jsプロキシがヘッダーをドロップ（frontend-api → payment API）
3. **RabbitMQ message bus** - AMQPヘッダーにトレースコンテキストがない非同期のpayment → fulfillment

その後、問題を修正して、すべてのサービスおよびインフラストラクチャレイヤーにわたるエンドツーエンドのコンテキスト伝播を復元します。

## アーキテクチャ | 期待される出力

目標は、3つのレイヤーにわたる伝播の問題を解決し、断絶した状態から

![servicemap1](./images/servicemap-b4.png)

完全に統合され相関付けられたビューへ移行することです（以下はプレースホルダー画像）

![servicemap2](./images/servicemap-aft.png)
