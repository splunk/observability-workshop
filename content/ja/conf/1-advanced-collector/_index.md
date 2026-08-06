---
title: Advanced OpenTelemetry Collector
description: OpenTelemetry Collectorの設定をゼロから構築し、いくつかの高度な設定シナリオを実践します。
weight: 2
archetype: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 75 minutes
hidden: true
---

このワークショップの目的は、OpenTelemetry Collectorの設定ファイルを作成・変更する力を身につけることです。最小限の `agent.yaml` と `gateway.yaml` ファイルから始め、いくつかの高度な実践的シナリオに対応できるよう段階的に構築していきます。

このワークショップの重要なポイントは、テレメトリデータをサードパーティベンダーのバックエンドに送信するのではなく、ローカルに保存するようOpenTelemetry Collectorを設定する方法を学ぶことです。このアプローチはデバッグやトラブルシューティングを簡素化するだけでなく、本番システムへのデータ送信を避けたいテストや開発環境にも最適です。

このワークショップを最大限に活用するために、以下の知識が必要です。

- OpenTelemetry Collectorとその設定ファイル構造に関する基本的な理解
- YAMLファイルの編集に関する習熟

このワークショップのすべての内容はローカルで実行できるように設計されており、実践的でアクセスしやすい学習体験を提供します。それでは始めましょう！

## ワークショップの概要

このワークショップでは、以下のトピックを扱います。

- **エージェントとゲートウェイのローカルセットアップ**: メトリクス、トレース、ログがエージェントを経由してゲートウェイに送信されることをテストします。
- **エージェントの耐障害性の強化**: フォールトトレランスのための基本設定を行います。
- **Processorの設定**:
  - 特定のSpan（例: ヘルスチェック）を除外してノイズをフィルタリングします。
  - 不要なタグの削除や機密データの処理を行います。
  - エクスポート前にパイプライン内でOTTL（OpenTelemetry Transformation Language）を使用してデータを変換します。
- **Connectorの設定**:
  - 受信した値に基づいてデータを異なるエンドポイントにルーティングします。
  <!--- Convert log and span data to metrics.-->

このワークショップを終える頃には、さまざまな実践的ユースケースに対応するOpenTelemetry Collectorの設定に精通しているでしょう。
