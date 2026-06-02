---
title: Observability Cloud 入門
linkTitle: Intro
weight: 1
archetype: chapter
time: 60 minutes
description: 1 時間で、Splunk Observability Cloud を使って、フルにインストルメントされた Kubernetes マイクロサービスアプリケーションに対するハンズオン形式のトラブルシューティングをご案内します。これは入門であり、後続のレッスンの基礎となります。
params:
  images:
    - images/featured-o11y.png
---

## はじめに

Splunk Observability Cloud を使った問題のトラブルシューティングを、ハンズオン形式で体験できます。Kubernetes 上にフルにインストルメントされたマイクロサービスアプリケーションを使い、メトリクス、トレース、ログをリアルタイムに分析します。

## ワークショップの概要

この 1 時間のハンズオンセッションでは、以下の内容を扱います。

- **Generate Real User Data** - Online Boutique のウェブサイトを操作して、メトリクス、トレース、ログを生成します
- **RUM** - パフォーマンスが悪いブラウザセッションを特定し、トラブルシューティングを開始します
- **APM** - フロントエンドの RUM トレースとバックエンドの APM トレースをリンクし、異常やエラーを検出します
- **Log Observer** - 「Related Content」を使って、APM のトレースから関連するログへ移動します
- **Synthetics** - 1 分ごとに実行される Synthetic テストで、24 時間 365 日のモニタリングを設定します

>**Online Boutique を使ってデータを生成しましょう。さあ、ショッピングに出かけましょう！**
