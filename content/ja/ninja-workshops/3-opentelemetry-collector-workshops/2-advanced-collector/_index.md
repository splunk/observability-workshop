---
title: Advanced OpenTelemetry Collector
description: Practice setting up the OpenTelemetry Collector configuration from scratch and go though several advanced configuration scenarios's.
weight: 2
archetype: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 75 minutes
---

このワークショップの目標は、OpenTelemetry Collector の設定ファイルを作成・変更する自信を身につけることです。最小限の `agent.yaml` と `gateway.yaml` ファイルから始めて、いくつかの高度な実践的シナリオに対応できるよう段階的に構築していきます。

このワークショップの主な焦点は、テレメトリーデータをサードパーティベンダーのバックエンドに送信するのではなく、ローカルに保存するように OpenTelemetry Collector を設定する方法を学ぶことです。このアプローチはデバッグやトラブルシューティングを簡素化するだけでなく、本番システムにデータを送信したくないテストや開発環境にも最適です。

このワークショップを最大限に活用するために、以下のスキルが必要です：

- OpenTelemetry Collector とその設定ファイル構造の基本的な理解
- YAML ファイルの編集スキル

このワークショップのすべての内容はローカルで実行できるように設計されており、実践的で取り組みやすい学習体験を提供します。さっそく構築を始めましょう！

## ワークショップ概要

このワークショップでは、以下のトピックをカバーします：

- **エージェントとゲートウェイのローカルセットアップ**: メトリクス、トレース、ログがエージェントを経由してゲートウェイに送信されることをテストします。
- **エージェントの耐障害性の強化**: フォールトトレランスのための基本設定。
- **プロセッサの設定**:
  - 特定のスパン（例：ヘルスチェック）を除外してノイズをフィルタリングします。
  - 不要なタグを削除し、機密データを処理します。
  - パイプラインでエクスポート前に OTTL（OpenTelemetry Transformation Language）を使用してデータを変換します。
- **コネクタの設定**:
  - 受信した値に基づいてデータを異なるエンドポイントにルーティングします。
  <!--- Convert log and span data to metrics.-->

このワークショップを終了する頃には、様々な実践的なユースケースに対応した OpenTelemetry Collector の設定に精通しているでしょう。
