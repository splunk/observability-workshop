---
title: Advanced OpenTelemetry Collector
description: OpenTelemetry Collector の設定をゼロから構築し、いくつかの高度な設定シナリオを実践します。
weight: 2
archetype: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 75 minutes
---

このワークショップの目標は、OpenTelemetry Collector の設定ファイルを作成・変更する自信を身につけることです。最小限の `agent.yaml` と `gateway.yaml` ファイルから始めて、段階的に拡張しながら、いくつかの高度な実践的シナリオに対応できるよう構築していきます。

このワークショップの重要なポイントは、テレメトリデータをサードパーティベンダーのバックエンドに送信するのではなく、ローカルに保存するよう OpenTelemetry Collector を設定する方法を学ぶことです。このアプローチにより、デバッグとトラブルシューティングが簡素化されるだけでなく、本番システムにデータを送信したくないテストや開発環境にも最適です。

このワークショップを最大限に活用するために、以下の知識があることが望ましいです:

- OpenTelemetry Collector とその設定ファイル構造の基本的な理解
- YAML ファイルの編集スキル

このワークショップのすべての内容はローカルで実行できるように設計されており、実践的でアクセスしやすい学習体験を提供します。それでは、構築を始めましょう！

## ワークショップ概要

このワークショップでは、以下のトピックを扱います:

- **Agent と Gateway のローカルセットアップ**: メトリクス、トレース、ログが Agent を経由して Gateway に送信されることをテストします。
- **Agent の回復力強化**: フォールトトレランスのための基本設定を行います。
- **Processor の設定**:
  - 特定のスパン（例: ヘルスチェック）を削除してノイズをフィルタリングします。
  - 不要なタグを削除し、機密データを処理します。
  - OTTL（OpenTelemetry Transformation Language）を使用して、エクスポート前にパイプライン内でデータを変換します。
- **Connector の設定**:
  - 受信した値に基づいて、データを異なるエンドポイントにルーティングします。
  <!--- Convert log and span data to metrics.-->

このワークショップを終える頃には、さまざまな実践的ユースケースに対応した OpenTelemetry Collector の設定に精通しているでしょう。
