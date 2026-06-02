---
title: 前提条件
weight: 2
---

## 必要なツール

このワークショップを開始する前に、以下のツールがインストールされていることを確認してください:

### AWS CLI

```bash
# Check installation
aws --version

# Should output: aws-cli/2.x.x or higher
```

### kubectl

```bash
# Check installation
kubectl version --client

# Should output: Client Version: v1.28.0 or higher
```

### eksctl

```bash
# Check installation
eksctl version

# Should output: 0.150.0 or higher
```

### Helm

```bash
# Check installation
helm version

# Should output: version.BuildInfo{Version:"v3.x.x"}
```

## AWS の要件

- 以下を作成する権限を持つ AWS アカウント:
  - EKS クラスター
  - VPC とサブネット
  - EC2 インスタンス
  - IAM ロールとポリシー
  - Elastic Network Interfaces
- 認証情報が設定された AWS CLI（`aws configure`）

## Splunk Observability Cloud

以下が必要です:

- Splunk Observability Cloud アカウント
- インジェスト権限を持つ **Access Token**
- **Realm** 識別子（例: us1, us2, eu0）

{{% notice title="Splunk 認証情報の取得" style="tip" %}}
Splunk Observability Cloud で:

1. **Settings** → **Access Tokens** に移動します
2. **Ingest** 権限を持つ新しいトークンを作成します
3. URL からリアルムを確認します: `https://app.<realm>.signalfx.com`
{{% /notice %}}

## コストに関する考慮事項

### AWS コスト（概算）

- **EKS Control Plane**: 約 $73/月
- **EC2 Nodes (2x m5.xlarge)**: 約 $280/月
- **Data Transfer**: 変動あり
- **EBS Volumes**: 約 $20/月

**推定合計**: ラボ環境で約 $380-400/月

### Splunk コスト

- メトリクス量（DPM - Data Points per Minute）に基づきます
- テスト用の無料トライアルが利用可能です

{{% notice title="警告" style="warning" %}}
継続的な課金を避けるため、ワークショップ完了後にリソースをクリーンアップすることを忘れないでください。
{{% /notice %}}

## 所要時間の目安

- **EKS クラスター作成**: 15〜20 分
- **Cilium インストール**: 10〜15 分
- **インテグレーション設定**: 10 分
- **合計**: 約 90 分
