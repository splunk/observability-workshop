---
title: ThousandEyes と Splunk Observability Cloud の統合
linkTitle: ThousandEyes Integration
weight: 5
archetype: chapter
authors: ["Alec Chamberlain"]
time: 120 minutes
description: Kubernetes で ThousandEyes Enterprise Agent を実行し、シンセティクスを Splunk Observability Cloud にストリーミングし、ThousandEyes テストと Splunk APM トレース間を横断的に分析します。
---

このワークショップでは、**ThousandEyes と Splunk Observability Cloud** を統合し、シンセティックモニタリングとオブザーバビリティデータ全体にわたる統一的な可視性を提供する方法を説明します。

## 学習内容

このワークショップを完了すると、以下のことができるようになります

- ThousandEyes Enterprise Agent をコンテナ化されたワークロードとして Kubernetes にデプロイする
- 付属の Spring PetClinic アプリケーションを Kubernetes 内部のテストターゲットとしてデプロイする
- OpenTelemetry を使用して ThousandEyes メトリクスを Splunk Observability Cloud と統合する
- ThousandEyes と Splunk APM が同じリクエストにリンクできるように分散トレーシングを設定する
- Kubernetes 内部サービスおよび外部依存関係に対するシンセティックテストを作成する
- Splunk Observability Cloud ダッシュボードでテスト結果を監視する
- ThousandEyes から Splunk APM トレースへ移動し、元の ThousandEyes テストに戻る

## セクション

### コアパス

- [概要](./1-overview/_index.md) - ThousandEyes のエージェントタイプとアーキテクチャを理解する
- [デプロイメント](./2-deployment/_index.md) - Kubernetes に Enterprise Agent をデプロイする
- [Splunk 統合](./3-splunk-integration/_index.md) - ThousandEyes メトリクスを Splunk Observability Cloud にストリーミングする
- [分散トレーシング](./4-distributed-tracing/_index.md) - ThousandEyes と Splunk APM 間のサポートされた双方向ドリルダウンを有効にする

### シナリオ拡張

- [Kubernetes テスト](./4-kubernetes-testing/_index.md) - シンセティックモニタリングとトレース相関の両方に役立つ内部テストを作成する
- [RUM](./6-rum-thousandeyes/_index.md) - ThousandEyes のネットワークシグナルと Splunk RUM を相関させ、エンドユーザー調査に活用する

### サポート

- [トラブルシューティング](./5-troubleshooting/_index.md) - よくある問題と解決策

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
このシナリオは2つの接続された統合として考えてください：OpenTelemetry ストリームが ThousandEyes メトリクスを Splunk に取り込み、分散トレーシングが Splunk APM から ThousandEyes への逆方向のパスを提供します。
{{% /notice %}}

## 前提条件

- Kubernetes クラスター（v1.16+）
- 選択した名前空間にリソースをデプロイするための RBAC 権限（注：このワークショップでは default 名前空間を使用します）
- Enterprise Agent トークンにアクセスできる ThousandEyes アカウント
- インジェストトークンへのアクセスと APM ルックアップ用の API トークンを作成する権限を持つ Splunk Observability Cloud アカウント

## 統合のメリット

ThousandEyes を Splunk Observability Cloud に接続することで、以下のメリットが得られます

- 🔗 **統一的な可視性**: シンセティックテスト結果を RUM、APM トレース、インフラストラクチャメトリクスと相関させる
- 📊 **強化されたダッシュボード**: 既存の Splunk オブザーバビリティメトリクスと並べて ThousandEyes データを可視化する
- 🔄 **双方向ドリルダウン**: ThousandEyes Service Map から Splunk トレースへ、また Splunk APM からリクエストを生成した ThousandEyes テストへ移動する
- 🚨 **一元化されたアラート**: Splunk 内で ThousandEyes テスト結果に基づいたアラートを設定する
- 🔍 **根本原因分析**: 問題がネットワーク関連（ThousandEyes）かアプリケーション関連（APM）かを迅速に特定する
- 📈 **包括的な分析**: Splunk の強力な分析エンジンでシンセティックモニタリングのトレンドを分析する
