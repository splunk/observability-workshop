---
title: Advanced OpenTelemetry Collector
description: OpenTelemetry Collectorの設定をゼロから構築し、いくつかの高度な設定シナリオを実践します。
weight: 2
type: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 75 minutes
---

このワークショップの目標は、OpenTelemetry Collectorの設定ファイルを作成・変更する自信を身につけることです。最小限の `agent.yaml` と `gateway.yaml` ファイルから始め、段階的に構築して、いくつかの高度な実践的シナリオに対応できるようにします。

このワークショップの重要なポイントは、テレメトリデータをサードパーティベンダーのバックエンドに送信するのではなく、ローカルに保存するようにOpenTelemetry Collectorを設定する方法を学ぶことです。このアプローチはデバッグやトラブルシューティングを簡素化するだけでなく、本番システムへのデータ送信を避けたいテストや開発環境にも最適です。

このワークショップを最大限に活用するために、以下の知識が必要です

- OpenTelemetry Collectorとその設定ファイル構造の基本的な理解
- YAMLファイルの編集スキル

このワークショップのすべての内容はローカルで実行できるように設計されており、実践的でアクセスしやすい学習体験を提供します。さっそく始めましょう！

## ワークショップの概要

このワークショップでは、以下のトピックを扱います

- **エージェントとゲートウェイのローカルセットアップ**: メトリクス、トレース、ログがエージェントを経由してゲートウェイに送信されることをテストします。
- **エージェントの耐障害性の強化**: フォールトトレランスのための基本設定を行います。
- **Processorの設定**:
  - 特定のSpan（例: ヘルスチェック）を削除してノイズをフィルタリングします。
  - 不要なタグを削除し、機密データを処理します。
  - エクスポート前にパイプラインでOTTL（OpenTelemetry Transformation Language）を使用してデータを変換します。
- **Connectorの設定**:
  - 受信した値に基づいてデータを異なるエンドポイントにルーティングします。
  <!--- Convert log and span data to metrics.-->

このワークショップを終える頃には、さまざまな実践的ユースケースに対応するOpenTelemetry Collectorの設定に精通しているでしょう。
