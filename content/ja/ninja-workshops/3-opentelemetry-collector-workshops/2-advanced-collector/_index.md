---
title: Advanced OpenTelemetry Collector
description: OpenTelemetry Collector の設定をゼロから行う練習を行い、いくつかの高度な設定シナリオを体験します。
weight: 2
archetype: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 75 minutes
---

このワークショップの目的は、OpenTelemetry Collector の設定ファイルを作成・変更する際の自信を深めることです。最小限の `agent.yaml` と `gateway.yaml` ファイルから始め、いくつかの高度な実際のシナリオに対応できるよう段階的に構築していきます。

このワークショップの重要なポイントは、テレメトリーデータをサードパーティベンダーのバックエンドに送信するのではなく、ローカルに保存するよう OpenTelemetry Collector を設定する方法を学ぶことです。このアプローチはデバッグやトラブルシューティングを簡素化するだけでなく、本番システムへのデータ送信を避けたいテストや開発環境にも最適です。

このワークショップを最大限に活用するために、以下の知識が必要です

- OpenTelemetry Collector とその設定ファイル構造の基本的な理解
- YAML ファイルの編集スキル

このワークショップのすべての内容はローカルで実行できるよう設計されており、実践的でアクセスしやすい学習体験を提供します。それでは、構築を始めましょう！

### ワークショップの概要

このワークショップでは、以下のトピックを取り上げます

- **Agent と Gateway をローカルでセットアップ**: メトリクス、トレース、ログが Agent 経由で Gateway に送られることをテストします。
- **Agent の耐障害性を強化**: フォールトトレランスのための基本設定を行います。
- **Processor の設定**:
  - 特定のスパン（例：ヘルスチェック）をドロップしてノイズをフィルタリングします。
  - 不要なタグを削除し、機密データを処理します。
  - エクスポート前にパイプラインで OTTL（OpenTelemetry Transformation Language）を使用してデータを変換します。
- **Connector の設定**:
  - 受信した値に基づいて、データを異なるエンドポイントにルーティングします。
  <!--- Convert log and span data to metrics.-->

このワークショップを終了すると、さまざまな実際のユースケースに対応する OpenTelemetry Collector の設定に精通しているでしょう。
