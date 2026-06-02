---
title: Advanced Collector Configuration
description: ゼロから OpenTelemetry Collector の設定を行う方法を実践し、いくつかの高度な設定シナリオを学習します。
weight: 2
archetype: chapter
authors: ["Robert Castley", "Charity Anderson", "Pieter Hagen", "Geoff Higginbottom"]
time: 90 minutes
hidden: true
---

このワークショップの目的は、OpenTelemetry Collector の設定ファイルの作成と編集に自信を持っていただくことです。最小限の `agent.yaml` ファイルから始めて、段階的に高度で実践的なシナリオに対応できるよう拡張していきます。

このワークショップで重点を置くのは、サードパーティベンダーのバックエンドに送信するのではなく、テレメトリデータをローカルに保存するように OpenTelemetry Collector を設定する方法です。このアプローチはデバッグやトラブルシューティングを簡素化するだけでなく、本番システムへのデータ送信を避けたいテストや開発環境にも最適です。

このワークショップを最大限に活用するために、以下の知識が必要です。

- OpenTelemetry Collector とその設定ファイル構造に関する基本的な理解
- YAML ファイルの編集に関する習熟

このワークショップのすべての内容はローカルで実行できるように設計されており、ハンズオン形式でアクセスしやすい学習体験を提供します。それでは早速、構築を始めましょう。

## Workshop Overview

このワークショップでは、以下のトピックを扱います。

- **エージェントをローカルにセットアップする**: メタデータを追加し、debug および file exporter を導入します。
- **gateway を設定する**: エージェントから gateway へトラフィックをルーティングします。
- **FileLog receiver を設定する**: さまざまなログファイルからログデータを収集します。
- **エージェントのレジリエンス向上**: フォールトトレランスのための基本設定を行います。
- **processor を設定する**:
  - 特定の span (例: ヘルスチェック) を除外してノイズをフィルタリングします。
  - 不要なタグを削除し、機密データを処理します。
  - エクスポート前のパイプラインで OTTL (OpenTelemetry Transformation Language) を使用してデータを変換します。
- **Connector を設定する**:
  - 受信した値に基づいてデータを異なるエンドポイントへルーティングします。
  - ログと span のデータを metric に変換します。

このワークショップを終える頃には、さまざまな実践的ユースケースに対応した OpenTelemetry Collector の設定方法に習熟しているでしょう。
