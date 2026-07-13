---
title: Observability Cloudの紹介
linkTitle: イントロ
weight: 1
archetype: chapter
time: 60 minutes
description: 1時間で、Splunk Observability Cloudを使用して、完全に計装されたKubernetesマイクロサービスアプリケーションに対するハンズオントラブルシューティングを体験します。これは後続のレッスンの導入と基礎となります。
params:
  images:
    - images/featured-o11y.png
---

## はじめに

Splunk Observability Cloudを使用して問題のトラブルシューティングを行うハンズオン体験を行います。完全に計装されたマイクロサービスアプリケーション — **Astronomy Shop** — がKubernetes上で動作し、メトリクス、トレース、ログをリアルタイム分析のために送信しています。

<!-- Along the classic troubleshooting path you'll also meet the newest members of the platform: the **AI Assistant** and the **AI Troubleshooting Agent**, which turn plain-English questions and firing alerts into evidence-backed root cause analysis. -->

## ワークショップの概要

この1時間のハンズオンセッションでは、以下の内容をカバーします

- **実際のユーザーデータの生成** - Astronomy Shopのウェブサイトを閲覧して、メトリクス、トレース、ログを生成します
- **RUM** - パフォーマンスの低いブラウザセッションを特定し、トラブルシューティングを開始します
- **APM** - フロントエンドのRUMトレースをバックエンドのAPMトレースにリンクし、異常やエラーを検出します
- **Log Observer** - 「Related Content」を使用して、APMトレースから関連するログに移動します
- **Synthetics** - 毎分実行されるSyntheticテストで24時間365日のモニタリングを設定します
<!-- - **AI-Assisted Troubleshooting** - Let the AI Assistant and AI Troubleshooting Agent accelerate root cause analysis
 -->
>**Astronomy Shopを使って、データを生成しましょう。さあ、買い物に行きましょう！** 🛰️
