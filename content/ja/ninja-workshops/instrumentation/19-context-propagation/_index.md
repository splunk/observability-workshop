---
draft: true
title: 手動トレース伝播
linkTitle: 手動トレース伝播
weight: 19
layout: chapter
time: 90 minutes
authors: ["Diana Omuoyo"]
description: Splunk OpenTelemetry でコンテナ化された Python アプリケーションを計装し、W3C ヘッダーが除去された際の断片化されたトレースを観察し、手動コンテキスト伝播で問題を修正します。
aliases:
  - /ninja-workshops/19-context-propagation/
---

**Splunk Distribution of the OpenTelemetry Collector** のデプロイ、**Splunk OpenTelemetry Python** エージェントによるマイクロサービスの計装、リバースプロキシが `traceparent` を除去した際の分散トレースの断裂を再現し、手動コンテキスト伝播を使用してエンドツーエンドのトレース連続性を復元する方法を学びます — **Splunk Observability Cloud** で検証します。

このワークショップでは、以下の内容をハンズオンで体験します:

- Phase 0 - W3C Trace Context がヘッダー除去境界で断裂する理由を理解する
- Phase 1 - **k3d** (Kubernetes) 上にコンテナ化されたリファレンスアーキテクチャをデプロイする
- Phase 2 - Python マイクロサービスアプリケーションを最初にデプロイし、エンドツーエンドのリクエストを検証する
- Phase 3 - **splunk-otel-collector** をデプロイし、Python サービスを計装して Splunk Observability Cloud にデータをエクスポートする
- Phase 4 - Splunk APM で**断片化されたトレース**を観察し (Step 1)、手動伝播で**接続されたトレース**を復元する (Step 2)
- Phase 5 - まとめとクリーンアップ

それでは始めましょう！
