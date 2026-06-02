---
title: Observability Cloud (1時間)
weight: 1
authors: ["Robert Castley", "Pieter Hagen"]
time: 60 minutes
description: 凝縮版。完全に計装された Kubernetes マイクロサービスアプリケーションを対象としたハンズオン形式のトラブルシューティングを通じて、Splunk Observability Cloud のエッセンスを 1 時間で体験できます。
show_toc: false
params:
  images:
    - images/featured-o11y.png
difficulty: Rookie
---

## はじめに

Splunk Observability Cloud を使用したトラブルシューティングをハンズオン形式で体験します。Kubernetes 上で完全に計装されたマイクロサービスアプリケーションを対象に、メトリクス、トレース、ログをリアルタイムで分析しながら作業を進めます。

## ワークショップ概要

この 1 時間のハンズオンセッションでは、以下の内容を扱います。

- **実ユーザーデータの生成** - Online Boutique ウェブサイトを閲覧して、メトリクス、トレース、ログを生成します
- **RUM** - パフォーマンスの低いブラウザーセッションを特定し、トラブルシューティングを開始します
- **APM** - フロントエンドの RUM トレースとバックエンドの APM トレースを連携させ、異常やエラーを検出します
- **Log Observer** - "Related Content" を使用して、APM トレースから関連するログへ遷移します
- **Synthetics** - 1 分ごとに実行される合成テストにより、24 時間 365 日の監視を設定します

>**Online Boutique を使ってデータを生成しましょう。買い物に出かけます！**
