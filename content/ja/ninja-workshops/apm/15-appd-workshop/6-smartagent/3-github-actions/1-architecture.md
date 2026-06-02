---
title: アーキテクチャと設計
weight: 1
time: 5 minutes
---

## システムアーキテクチャ

GitHub Actions ベースの Smart Agent デプロイメントシステムは、AWS VPC 内のセルフホストランナーを使用して、SSH 経由で複数のターゲットホストへのデプロイメントを調整します。

### 高レベルアーキテクチャ

```mermaid
graph TB
    subgraph Internet
        GH[GitHub.com<br/>Repository & Actions]
        User[Developer<br/>Local Machine]
    end

    subgraph AWS["AWS VPC (172.31.0.0/16)"]
        subgraph SG["Security Group: smartagent-lab"]
            Runner[Self-hosted Runner<br/>EC2 Instance<br/>172.31.1.x]
            
            subgraph Targets["Target Hosts"]
                T1[Target Host 1<br/>Ubuntu EC2<br/>172.31.1.243]
                T2[Target Host 2<br/>Ubuntu EC2<br/>172.31.1.48]
                T3[Target Host 3<br/>Ubuntu EC2<br/>172.31.1.5]
            end
        end
    end

    User -->|git push| GH
    GH <-->|HTTPS:443<br/>Poll for jobs| Runner
    Runner -->|SSH:22<br/>Private IPs| T1
    Runner -->|SSH:22<br/>Private IPs| T2
    Runner -->|SSH:22<br/>Private IPs| T3

    style GH fill:#24292e,color:#fff
    style User fill:#0366d6,color:#fff
    style Runner fill:#28a745,color:#fff
    style T1 fill:#ffd33d,color:#000
    style T2 fill:#ffd33d,color:#000
    style T3 fill:#ffd33d,color:#000
```

## ネットワークアーキテクチャ

すべてのインフラストラクチャは、共有のセキュリティグループを持つ単一の AWS VPC 上で稼働します。セルフホストランナーは、プライベート IP を介してターゲットホストと通信します。

### VPC レイアウト

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS VPC (172.31.0.0/16)                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │          Security Group: smartagent-lab                   │  │
│  │  Rules:                                                   │  │
│  │  - Inbound: SSH (22) from same security group            │  │
│  │  - Outbound: HTTPS (443) to GitHub                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Self-hosted │    │  Target EC2  │    │  Target EC2  │       │
│  │   Runner    │    │              │    │              │       │
│  │             │───▶│ Private IP:  │    │ Private IP:  │       │
│  │ 172.31.1.x  │SSH │ 172.31.1.243 │    │ 172.31.1.48  │       │
│  │             │───▶│              │    │              │       │
│  │ Polls GitHub│    │ Ubuntu 20.04 │    │ Ubuntu 20.04 │       │
│  └─────────────┘    └──────────────┘    └──────────────┘       │
│         │                    │                    │             │
│         │                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                              │                                  │
└──────────────────────────────┼──────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │   AppDynamics    │
                    │    Controller    │
                    │  (SaaS/On-Prem)  │
                    └──────────────────┘
```

## ワークフロー実行フロー

### 完全なデプロイメントシーケンス

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant Runner as Self-hosted Runner
    participant Target as Target Host(s)

    Dev->>GH: 1. Push code or trigger workflow
    GH->>GH: 2. Workflow event triggered
    Runner->>GH: 3. Poll for jobs (HTTPS:443)
    GH->>Runner: 4. Assign job to runner
    Runner->>Runner: 5. Execute prepare job<br/>(load host matrix)
    
    par Parallel Execution
        Runner->>Target: 6a. SSH to Host 1<br/>(port 22)
        Runner->>Target: 6b. SSH to Host 2<br/>(port 22)
        Runner->>Target: 6c. SSH to Host 3<br/>(port 22)
    end
    
    Target->>Target: 7. Execute commands<br/>(install/uninstall/stop/clean)
    Target-->>Runner: 8. Return results
    Runner-->>GH: 9. Report job status
    GH-->>Dev: 10. Notify completion
```

## コンポーネントの詳細

### GitHub リポジトリ

**保管対象:**

- 11 個のワークフロー YAML ファイル
- Smart Agent インストールパッケージ
- 設定ファイル (config.ini)

**シークレット:**

- SSH 秘密鍵

**変数:**

- ホストリスト (DEPLOYMENT_HOSTS)
- ユーザー/グループ設定 (オプション)

### セルフホストランナー

**配置場所:**

- AWS VPC (ターゲットと同じ)
- プライベートネットワークアクセス

**役割:**

- GitHub のワークフロージョブをポーリング
- ワークフローステップの実行
- ターゲットホストへの SSH 接続
- ファイル転送 (SCP)
- 並列実行
- エラー収集

**要件:**

- Ubuntu/Amazon Linux 2
- GitHub への送信 HTTPS (443)
- ターゲットホストへの送信 SSH (22)
- SSH 鍵認証

**アクセス:**

- GitHub への送信 HTTPS (443)
- ターゲットホストへの送信 SSH (22)
- SSH 鍵認証を使用

### ターゲットホスト

**前提条件:**

- Ubuntu 20.04 以上
- SSH サーバーが稼働中
- sudo 権限を持つユーザー
- 認証済み SSH 鍵

**デプロイ後:**

```
/opt/appdynamics/
└── appdsmartagent/
    ├── smartagentctl
    ├── config.ini
    └── agents/
        ├── machine/
        ├── java/
        ├── node/
        └── db/
```

## セキュリティアーキテクチャ

### セキュリティレイヤー

1. **AWS VPC の分離**
   - ホスト用のプライベートサブネット
   - インターネットへの直接アクセスは不要
   - VPC フローログを有効化

2. **セキュリティグループ**
   - SSH (22) は同一セキュリティグループ内のみ
   - GitHub アクセス用の送信 HTTPS (443)
   - ステートフルなファイアウォールルール

3. **SSH 鍵認証**
   - パスワード認証なし
   - 鍵は GitHub Secrets に保存
   - ランナー上の一時的な鍵ファイル
   - ワークフロー終了後に鍵を削除

4. **GitHub のセキュリティ**
   - リポジトリのアクセス制御
   - ブランチ保護ルール
   - シークレットがログに出力されることはない
   - 環境変数のマスキング

5. **ネットワークセキュリティ**
   - プライベート IP 通信のみ
   - パブリック IP は不要
   - ランナーをターゲットと同一の VPC に配置

## ワークフローのカテゴリ

このシステムには、4 つのカテゴリに整理された 11 個のワークフローが含まれています。

```
GitHub Actions Workflows (11 Total)
├── Deployment (1 workflow)
│   └── Deploy Smart Agent (Batched)
├── Agent Installation (4 workflows)
│   ├── Install Node Agent (Batched)
│   ├── Install Machine Agent (Batched)
│   ├── Install DB Agent (Batched)
│   └── Install Java Agent (Batched)
├── Agent Uninstallation (4 workflows)
│   ├── Uninstall Node Agent (Batched)
│   ├── Uninstall Machine Agent (Batched)
│   ├── Uninstall DB Agent (Batched)
│   └── Uninstall Java Agent (Batched)
└── Smart Agent Management (2 workflows)
    ├── Stop and Clean Smart Agent (Batched)
    └── Cleanup All Agents (Batched)
```

## バッチ処理戦略

すべてのワークフローは、あらゆる規模のデプロイメントに対応するため、自動バッチ処理を採用しています。

### バッチ処理の仕組み

```
HOST LIST (1000 hosts)              BATCH_SIZE = 256

Host 001: 172.31.1.1                ┌──────────────────┐
Host 002: 172.31.1.2      ────────▶ │   BATCH 1        │
    ...                              │   Hosts 1-256    │ ───┐
Host 256: 172.31.1.256               │   Sequential     │    │
                                     └──────────────────┘    │
Host 257: 172.31.1.257               ┌──────────────────┐    │
Host 258: 172.31.1.258   ────────▶  │   BATCH 2        │    │ SEQUENTIAL
    ...                              │   Hosts 257-512  │    │ EXECUTION
Host 512: 172.31.1.512               │   Sequential     │    │
                                     └──────────────────┘    │
Host 513: 172.31.1.513               ┌──────────────────┐    │
    ...                              │   BATCH 3        │    │
Host 768: 172.31.1.768   ────────▶  │   Hosts 513-768  │ ───┘
                                     └──────────────────┘
Host 769: 172.31.1.769               ┌──────────────────┐
    ...                              │   BATCH 4        │
Host 1000: 172.31.2.232  ────────▶  │   Hosts 769-1000 │
                                     │   (232 hosts)    │
                                     └──────────────────┘

WITHIN EACH BATCH:
┌────────────────────────────────────────┐
│  All hosts deploy in PARALLEL          │
│                                        │
│  Host 1 ──┐                           │
│  Host 2 ──┤                           │
│  Host 3 ──┼─▶ Background processes (&)│
│    ...    │                           │
│  Host 256─┘   └─▶ wait command        │
└────────────────────────────────────────┘
```

### なぜバッチを逐次実行するのか

**リソース管理:**

- セルフホストランナーへの過剰な負荷を防止
- 各バッチで 256 個の SSH 接続を並列に開く
- 逐次処理により安定したパフォーマンスを確保

**設定可能:**

- デフォルトのバッチサイズ: 256 (GitHub Actions のマトリクス上限)
- ワークフロー入力により、より小さなバッチに調整可能
- 速度とリソース使用量のバランス調整

### スケーリング特性

**デプロイメント速度 (デフォルト BATCH_SIZE=256):**

- 10 ホスト → 1 バッチ → 約 2 分
- 100 ホスト → 1 バッチ → 約 3 分
- 500 ホスト → 2 バッチ → 約 6 分
- 1,000 ホスト → 4 バッチ → 約 12 分
- 5,000 ホスト → 20 バッチ → 約 60 分

**速度に影響する要因:**

- ネットワーク帯域幅 (ホストあたり 19MB のパッケージ)
- SSH 接続のオーバーヘッド (ホストあたり約 1 秒)
- ターゲットホストの CPU/ディスク速度
- ランナーのリソース (CPU/メモリ)

## 次のステップ

アーキテクチャを理解できたところで、次は GitHub のセットアップとセルフホストランナーの構成に進みます。
