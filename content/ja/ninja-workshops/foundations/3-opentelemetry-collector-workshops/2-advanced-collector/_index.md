---
title: Advanced OpenTelemetry Collector
description: OpenTelemetry Collector の設定をゼロから構築する練習を行い、いくつかの高度な設定シナリオを通して学習します。
weight: 2
type: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 75 minutes
---

このワークショップの目的は、OpenTelemetry Collector の設定ファイルの作成と変更に自信を持てるようにすることです。最小限の `agent.yaml` と `gateway.yaml` ファイルから始めて、段階的に拡張しながら、いくつかの高度な実践的シナリオに対応できるように構築していきます。

このワークショップで重視するポイントは、テレメトリーデータをサードパーティベンダーのバックエンドに送信するのではなく、ローカルに保存するように OpenTelemetry Collector を設定する方法を学ぶことです。このアプローチはデバッグやトラブルシューティングを容易にするだけでなく、本番システムへのデータ送信を避けたいテストや開発環境にも最適です。

このワークショップを最大限に活用するためには、以下が必要です。

- OpenTelemetry Collector とその設定ファイル構造に関する基本的な理解。
- YAML ファイルの編集に関する習熟。

このワークショップのすべての内容は、ローカルで実行できるように設計されており、ハンズオン形式でアクセスしやすい学習体験を提供します。それでは、構築を始めていきましょう！

## Workshop Overview

このワークショップでは、以下のトピックを取り上げます。

- **agent と gateway をローカルにセットアップする**: メトリクス、トレース、ログが agent を経由して gateway に送られることをテストします。
- **agent のレジリエンス強化**: フォールトトレランスのための基本的な設定。
- **プロセッサーの設定**:
  - 特定のスパン（例：ヘルスチェック）を破棄することでノイズをフィルタリングします。
  - 不要なタグを削除し、機密データを取り扱います。
  - エクスポート前に、パイプライン内で OTTL（OpenTelemetry Transformation Language）を使ってデータを変換します。
- **コネクターの設定**:
  - 受信した値に基づいて、異なるエンドポイントへデータをルーティングします。
  <!--- Convert log and span data to metrics.-->

このワークショップを終える頃には、さまざまな実践的なユースケースに対応した OpenTelemetry Collector の設定に慣れているはずです。
