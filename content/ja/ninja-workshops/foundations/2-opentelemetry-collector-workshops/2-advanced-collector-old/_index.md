---
title: 高度なCollector設定
description: OpenTelemetry Collectorの設定をゼロから構築し、いくつかの高度な設定シナリオを実践します。
weight: 2
archetype: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 90 minutes
hidden: true
---

このワークショップの目標は、OpenTelemetry Collectorの設定ファイルを作成・変更する自信を身につけることです。最小限の `agent.yaml` ファイルから始め、段階的に構築して、いくつかの高度な実践的シナリオに対応できるようにします。

このワークショップの重要なポイントは、テレメトリデータをサードパーティベンダーのバックエンドに送信するのではなく、ローカルに保存するようにOpenTelemetry Collectorを設定する方法を学ぶことです。このアプローチはデバッグやトラブルシューティングを簡素化するだけでなく、本番システムへのデータ送信を避けたいテストや開発環境にも最適です。

このワークショップを最大限に活用するために、以下の知識が必要です

- OpenTelemetry Collectorとその設定ファイル構造の基本的な理解
- YAMLファイルの編集スキル

このワークショップのすべての内容はローカルで実行できるように設計されており、実践的でアクセスしやすい学習体験を提供します。さっそく始めましょう！

## ワークショップの概要

このワークショップでは、以下のトピックをカバーします

- **ローカルでのエージェントセットアップ**: メタデータの追加、debug Exporterとfile Exporterの導入
- **ゲートウェイの設定**: エージェントからゲートウェイへのトラフィックルーティング
- **FileLog Receiverの設定**: さまざまなログファイルからのログデータ収集
- **エージェントの耐障害性の強化**: フォールトトレランスのための基本設定
- **Processorの設定**:
  - 特定のSpan（例: ヘルスチェック）をドロップしてノイズを除去
  - 不要なタグの削除と機密データの処理
  - エクスポート前にパイプラインでOTTL（OpenTelemetry Transformation Language）を使用してデータを変換
- **Connectorの設定**:
  - 受信した値に基づいてデータを異なるエンドポイントにルーティング
  - ログおよびSpanデータをメトリクスに変換

このワークショップを終える頃には、さまざまな実践的ユースケースに対応するOpenTelemetry Collectorの設定に精通しているでしょう。
