---
title: ThousandEyes と Splunk Observability Cloud の統合
linkTitle: ThousandEyes 統合
weight: 5
archetype: chapter
authors: ["Alec Chamberlain"]
time: 120 minutes
description: Kubernetes に ThousandEyes Enterprise Agent をデプロイし、シンセティックデータを Splunk Observability Cloud にストリーミングし、ThousandEyes と Splunk APM 間の双方向ドリルダウンを有効にします。
---

このワークショップでは、**ThousandEyes と Splunk Observability Cloud** を統合して、シンセティック監視とオブザーバビリティデータ全体にわたる統一された可視性を提供する方法を説明します。

## 学習内容

このワークショップを終了すると、以下のことができるようになります：

- Kubernetesにコンテナ化されたワークロードとしてThousandEyes Enterprise Agentをデプロイする
- OpenTelemetryを使用してThousandEyesメトリクスをSplunk Observability Cloudと統合する
- ThousandEyesとSplunk APMが同じリクエストにリンクできるように分散トレーシングを構成する
- 内部Kubernetesサービスと外部依存関係のシンセティックテストを作成する
- Splunk Observability Cloudダッシュボードでテスト結果を監視する
- ThousandEyesからSplunk APMトレースに移動し、元のThousandEyesテストに戻る

## セクション

### コアパス

- [概要](./1-overview/_index.md) - ThousandEyesエージェントの種類とアーキテクチャを理解する
- [デプロイメント](./2-deployment/_index.md) - KubernetesにEnterprise Agentをデプロイする
- [Splunk 統合](./3-splunk-integration/_index.md) - ThousandEyesメトリクスをSplunk Observability Cloudにストリーミングする
- [分散トレーシング](./4-distributed-tracing/_index.md) - ThousandEyesとSplunk APM間のサポートされた双方向ドリルダウンを有効にする

### シナリオ拡張

- [Kubernetes テスト](./4-kubernetes-testing/_index.md) - シンセティック監視とトレース相関の両方に役立つ内部テストを作成する
- [RUM](./6-rum-thousandeyes/_index.md) - エンドユーザー調査のためにThousandEyesネットワークシグナルとSplunk RUMを相関させる

### サポート

- [トラブルシューティング](./5-troubleshooting/_index.md) - よくある問題と解決策

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
このシナリオは2つの接続された統合と考えてください：OpenTelemetryストリームはThousandEyesメトリクスをSplunkに取り込み、分散トレーシングはSplunk APMからThousandEyesに戻る逆方向のパスを提供します。
{{% /notice %}}

## 前提条件

- Kubernetesクラスター（v1.16以上）
- 選択したnamespaceにリソースをデプロイするためのRBAC権限
- Enterprise AgentトークンにアクセスできるThousandEyesアカウント
- インジェストトークンへのアクセスとAPMルックアップ用のAPIトークンを作成する権限を持つSplunk Observability Cloudアカウント

## 統合のメリット

ThousandEyesをSplunk Observability Cloudに接続することで、以下のメリットが得られます：

- 🔗 **統一された可視性**: シンセティックテスト結果をRUM、APMトレース、インフラストラクチャメトリクスと相関させる
- 📊 **強化されたダッシュボード**: ThousandEyesデータを既存のSplunkオブザーバビリティメトリクスと並べて可視化する
- 🔄 **双方向ドリルダウン**: ThousandEyes Service MapからSplunkトレースに移動し、Splunk APMからリクエストを生成したThousandEyesテストに戻る
- 🚨 **一元化されたアラート**: Splunk内でThousandEyesテスト結果に基づいてアラートを構成する
- 🔍 **根本原因分析**: 問題がネットワーク関連（ThousandEyes）かアプリケーション関連（APM）かを迅速に特定する
- 📈 **包括的な分析**: Splunkの強力な分析エンジンでシンセティック監視のトレンドを分析する

{{% children depth="1" type="card" description="true" %}}
