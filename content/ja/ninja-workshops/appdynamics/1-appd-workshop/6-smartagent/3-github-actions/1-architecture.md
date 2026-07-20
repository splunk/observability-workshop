---
title: アーキテクチャと設計
weight: 1
time: 5 minutes
---

## システムアーキテクチャ

GitHub Actionsベースの Smart Agent デプロイメントシステムは、AWS VPC内のセルフホステッドランナーを使用して、SSHを介して複数のターゲットホストへのデプロイメントをオーケストレーションします。

### ハイレベルアーキテクチャ

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

すべてのインフラストラクチャは、共有セキュリティグループを持つ単一のAWS VPCで動作します。セルフホステッドランナーはプライベートIPを介してターゲットホストと通信します。

### VPCレイアウト

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

### GitHubリポジトリ

**格納内容**

- 11個のワークフローYAMLファイル
- Smart Agentインストールパッケージ
- 設定ファイル（config.ini）

**Secrets**

- SSH秘密鍵

**Variables**

- ホストリスト（DEPLOYMENT_HOSTS）
- ユーザー/グループ設定（オプション）

### セルフホステッドランナー

**配置場所**

- AWS VPC（ターゲットと同一）
- プライベートネットワークアクセス

**責務**

- GitHubのワークフロージョブをポーリング
- ワークフローステップの実行
- ターゲットホストへのSSH接続
- ファイル転送（SCP）
- 並列実行
- エラー収集

**要件**

- Ubuntu/Amazon Linux 2
- GitHubへのアウトバウンドHTTPS（443）
- ターゲットホストへのアウトバウンドSSH（22）
- SSH鍵認証

**アクセス**

- GitHubへのアウトバウンドHTTPS（443）
- ターゲットホストへのアウトバウンドSSH（22）
- SSH鍵認証を使用

### ターゲットホスト

**前提条件**

- Ubuntu 20.04以上
- SSHサーバーが稼働中
- sudo権限を持つユーザー
- 認証済みSSH鍵

**デプロイ後**

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

1. **AWS VPC分離**
   - ホスト用プライベートサブネット
   - 直接のインターネットアクセスは不要
   - VPCフローログを有効化

2. **セキュリティグループ**
   - SSH（22）は同一セキュリティグループ内のみ
   - GitHubアクセス用のアウトバウンドHTTPS（443）
   - ステートフルファイアウォールルール

3. **SSH鍵認証**
   - パスワード認証なし
   - 鍵はGitHub Secretsに保存
   - ランナー上の一時的な鍵ファイル
   - ワークフロー終了後に鍵を削除

4. **GitHubセキュリティ**
   - リポジトリアクセス制御
   - ブランチ保護ルール
   - Secretsはログに公開されない
   - 環境変数のマスキング

5. **ネットワークセキュリティ**
   - プライベートIP通信のみ
   - パブリックIPは不要
   - ランナーはターゲットと同一VPC内

## ワークフローカテゴリー

システムには4つのカテゴリーに分類された11個のワークフローが含まれます。

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

すべてのワークフローは、あらゆる規模のデプロイメントをサポートするために自動バッチ処理を使用します。

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

### なぜシーケンシャルバッチなのか

**リソース管理**

- セルフホステッドランナーの過負荷を防止
- 各バッチは256個の並列SSH接続を開く
- シーケンシャル処理により安定したパフォーマンスを確保

**設定可能**

- デフォルトバッチサイズ: 256（GitHub Actionsマトリクスの上限）
- ワークフロー入力で小さいバッチに調整可能
- 速度とリソース使用量のバランス

### スケーリング特性

**デプロイ速度（デフォルトBATCH_SIZE=256）**

- 10ホスト → 1バッチ → 約2分
- 100ホスト → 1バッチ → 約3分
- 500ホスト → 2バッチ → 約6分
- 1,000ホスト → 4バッチ → 約12分
- 5,000ホスト → 20バッチ → 約60分

**速度に影響する要因**

- ネットワーク帯域幅（ホストあたり19MBパッケージ）
- SSH接続オーバーヘッド（ホストあたり約1秒）
- ターゲットホストのCPU/ディスク速度
- ランナーリソース（CPU/メモリ）

## 次のステップ

アーキテクチャを理解したところで、GitHubのセットアップとセルフホステッドランナーの設定に進みます。
