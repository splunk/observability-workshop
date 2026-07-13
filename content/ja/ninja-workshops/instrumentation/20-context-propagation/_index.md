---
draft: true
title: Context Propagation
linkTitle: Context Propagation
weight: 20
layout: chapter
time: 90 minutes
authors: ["Diana Omuoyo"]
description: プロキシやメッセージバスがW3Cトレースコンテキストを破棄すると、分散トレーシングはサイレントに壊れます。このワークショップでは、よくあるコンテキストと相関の断絶を含むサンプルEコマースアプリケーションを使用します
aliases:
  - /ninja-workshops/20-context-propagation/
---

## 概要

このワークショップでは、天文機器のストアフロントである **Cosmic Observatory Shop** をデプロイし、Splunk RUMとSplunk APMで計装します。

必要なW3Cヘッダーが以下の **3つ** のレイヤーで除去された場合に、サービスマップとトレースが断片化される様子を観察します。

1. **Edge NGINX gateway** - W3Cトレースヘッダーを破棄（frontend-api → order API）
2. **Payment gateway proxy** - 計装済みのNode.jsプロキシがヘッダーを破棄（frontend-api → payment API）
3. **RabbitMQ message bus** - AMQPヘッダーにトレースコンテキストがない非同期のpayment → fulfillment

その後、問題を修正して、すべてのサービスおよびインフラストラクチャレイヤーにわたるエンドツーエンドのコンテキスト伝搬を復元します。

## アーキテクチャ | 期待される出力

```text
Browser (RUM)
    → Frontend → Frontend API (BFF)
         ├─ catalog path ──► Catalog API
         └─ purchase workflow ──► Edge Gateway → Order API
                              └─► Payment Gateway → Payment API → RabbitMQ → Fulfillment Worker
                                        ▲                    ▲              ▲
                                   Break #1              Break #2       Break #3
                                   (Step 06)             (Step 07)      (Step 08)
```

それでは始めましょう！
