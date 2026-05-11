---
title: ThousandEyes と Splunk Observability Cloud の統合
linkTitle: ThousandEyes 統合
weight: 5
archetype: chapter
authors: ["Alec Chamberlain"]
time: 120 minutes
description: Kubernetes に ThousandEyes Enterprise Agent をデプロイし、シンセティックデータを Splunk Observability Cloud にストリーミングし、ThousandEyes と Splunk APM 間の双方向ドリルダウンを有効にします。
---

このワークショップでは、**ThousandEyes と Splunk Observability Cloud** を統合して、シンセティックモニタリングとオブザーバビリティデータ全体にわたる統一されたビジビリティを提供する方法を実演します。

## 学習内容

このワークショップを完了すると、以下のことができるようになります

- Kubernetes にコンテナ化されたワークロードとして ThousandEyes Enterprise Agent をデプロイする
- 内部 Kubernetes テストターゲットとして付属の Spring PetClinic アプリケーションをデプロイする
- OpenTelemetry を使用して ThousandEyes メトリクスを Splunk Observability Cloud と統合する
- ThousandEyes と Splunk APM が同じリクエストにリンクできるように分散トレーシングを設定する
- 内部 Kubernetes サービスおよび外部依存関係に対するシンセティックテストを作成する
- Splunk Observability Cloud ダッシュボードでテスト結果を監視する
- ThousandEyes から Splunk APM トレースに移動し、元の ThousandEyes テストに戻る

## セクション

### コアパス

- [概要](./1-overview/_index.md) - ThousandEyes のエージェントタイプとアーキテクチャを理解する
- [デプロイメント](./2-deployment/_index.md) - Kubernetes に Enterprise Agent をデプロイする
- [Splunk 統合](./3-splunk-integration/_index.md) - ThousandEyes メトリクスを Splunk Observability Cloud にストリーミングする
- [分散トレーシング](./4-distributed-tracing/_index.md) - ThousandEyes と Splunk APM 間のサポートされた双方向ドリルダウンを有効にする

### シナリオ拡張

- [Kubernetes テスト](./4-kubernetes-testing/_index.md) - シンセティックモニタリングとトレース相関の両方に役立つ内部テストを作成する
- [RUM](./6-rum-thousandeyes/_index.md) - ThousandEyes のネットワークシグナルと Splunk RUM を相関させてエンドユーザー調査を行う

### サポート

- [トラブルシューティング](./5-troubleshooting/_index.md) - よくある問題と解決策

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
このシナリオは、2つの連携した統合として考えてください。OpenTelemetry ストリームが ThousandEyes メトリクスを Splunk に取り込み、分散トレーシングが Splunk APM から ThousandEyes への逆方向のパスを提供します。
{{% /notice %}}

## 前提条件

- Kubernetes クラスター（v1.16+）
- 選択した namespace にリソースをデプロイするための RBAC 権限
- Enterprise Agent トークンにアクセスできる ThousandEyes アカウント
- インジェストトークンへのアクセスと APM ルックアップ用の API トークンを作成する権限を持つ Splunk Observability Cloud アカウント

## 統合のメリット

ThousandEyes を Splunk Observability Cloud に接続することで、以下のメリットが得られます

- 🔗 **統一されたビジビリティ**: シンセティックテスト結果を RUM、APM トレース、およびインフラストラクチャメトリクスと相関させます
- 📊 **強化されたダッシュボード**: 既存の Splunk オブザーバビリティメトリクスと並べて ThousandEyes データを可視化します
- 🔄 **双方向ドリルダウン**: ThousandEyes Service Map から Splunk トレースに移動し、Splunk APM からリクエストを生成した ThousandEyes テストに戻ることができます
- 🚨 **一元化されたアラート**: Splunk 内で ThousandEyes テスト結果に基づいたアラートを設定します
- 🔍 **根本原因分析**: 問題がネットワーク関連（ThousandEyes）かアプリケーション関連（APM）かを迅速に特定します
- 📈 **包括的な分析**: Splunk の強力な分析エンジンでシンセティックモニタリングのトレンドを分析します
