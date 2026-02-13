---
title: アーキテクチャと設計
weight: 1
time: 5 minutes
---

## システムアーキテクチャ

Jenkins ベースの Smart Agent デプロイシステムは、ハブ・アンド・スポーク型のアーキテクチャを採用しています。AWS VPC 内の Jenkins エージェントが SSH 経由で複数のターゲットホストへのデプロイを調整します。

### 全体アーキテクチャ

```mermaid
graph TB
    subgraph "Jenkins Infrastructure"
        JM[Jenkins Master<br/>Web UI + Orchestration]
        JA[Jenkins Agent<br/>EC2 in VPC<br/>Label: linux]
    end

    subgraph "AWS VPC - Private Network"
        subgraph "Target EC2 Instances"
            H1[Host 1<br/>172.31.1.243]
            H2[Host 2<br/>172.31.1.48]
            H3[Host 3<br/>172.31.1.5]
            HN[Host N<br/>172.31.x.x]
        end
    end

    DEV[Developer/Operator]
    APPD[AppDynamics<br/>Controller]

    DEV -->|1. Triggers Pipeline| JM
    JM -->|2. Assigns Job| JA
    JA -->|3. SSH Deploy<br/>Private IPs| H1
    JA -->|3. SSH Deploy<br/>Private IPs| H2
    JA -->|3. SSH Deploy<br/>Private IPs| H3
    JA -->|3. SSH Deploy<br/>Private IPs| HN

    H1 -.->|Metrics| APPD
    H2 -.->|Metrics| APPD
    H3 -.->|Metrics| APPD
    HN -.->|Metrics| APPD

    style JM fill:#d4e6f1
    style JA fill:#a9cce3
    style H1 fill:#aed6f1
    style H2 fill:#aed6f1
    style H3 fill:#aed6f1
    style HN fill:#aed6f1
```

## ネットワークアーキテクチャ

すべてのインフラストラクチャは、共有セキュリティグループを持つ単一の AWS VPC 内で稼働します。Jenkins エージェントはプライベート IP 経由でターゲットホストと通信するため、ターゲットホストにパブリック IP アドレスは不要です。

### VPC レイアウト

```text
┌─────────────────────────────────────────────────────────────────┐
│                        AWS VPC (10.0.0.0/16)                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Security Group: app-agents-sg                │  │
│  │  Rules:                                                   │  │
│  │  - Inbound: SSH (22) from Jenkins Agent only             │  │
│  │  - Outbound: HTTPS (443) to AppDynamics Controller       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Jenkins Agent│    │  Target EC2  │    │  Target EC2  │      │
│  │              │    │              │    │              │      │
│  │ Private IP:  │───▶│ Private IP:  │    │ Private IP:  │      │
│  │ 172.31.50.10 │SSH │ 172.31.1.243 │    │ 172.31.1.48  │      │
│  │              │───▶│              │    │              │      │
│  │ Label: linux │    │ Ubuntu 20.04 │    │ Ubuntu 20.04 │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
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

## デプロイフロー

### 完全なデプロイシーケンス

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant JM as Jenkins Master
    participant JA as Jenkins Agent<br/>(VPC)
    participant TH as Target Hosts<br/>(VPC)
    participant AppD as AppDynamics<br/>Controller

    Dev->>JM: 1. Trigger Pipeline
    JM->>JM: 2. Load Credentials
    JM->>JA: 3. Schedule Job
    JA->>JA: 4. Prepare Batches

    loop For Each Batch
        JA->>TH: 5. SSH Copy Files (SCP)
        JA->>TH: 6. SSH Execute Commands
        TH->>TH: 7. Install/Config Agent
        TH-->>JA: 8. Return Status
    end

    JA->>JM: 9. Report Results
    JM->>Dev: 10. Show Build Status

    TH->>AppD: 11. Send Metrics (Post-Install)
    AppD-->>Dev: 12. View Monitoring Data
```

## コンポーネントの詳細

### Jenkins Master

**役割:**

- ユーザー向け Web UI
- パイプラインのオーケストレーション
- 認証情報の管理
- ビルド履歴とログ
- ジョブのスケジューリング

**要件:**

- Jenkins 2.300以降
- プラグイン: Pipeline、SSH Agent、Credentials、Git
- エージェントへのネットワークアクセス

### Jenkins Agent

**配置場所:**

- AWS VPC（ターゲットと同一）
- プライベートネットワークアクセス

**役割:**

- パイプラインステージの実行
- ターゲットホストへの SSH 接続
- ファイル転送（SCP）
- バッチ処理ロジック
- エラー収集

**要件:**

- ラベル: `linux`
- Java 11以降
- SSH クライアント
- ネットワーク: すべてのターゲットへの SSH 接続
- ディスク: アーティファクト用に約20GB

### ターゲットホスト

**前提条件:**

- Ubuntu 20.04以降
- SSH サーバーが稼働していること
- sudo アクセス権を持つユーザー
- SSH 鍵が認証済みであること

**デプロイ後:**

```text
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

1. **AWS VPC 分離**
   - エージェント用のプライベートサブネット
   - 直接のインターネットアクセスは不要
   - VPC フローログの有効化

2. **セキュリティグループ**
   - Jenkins Agent の IP をホワイトリスト登録
   - ポート 22（SSH）のみ
   - ステートフルファイアウォールルール

3. **SSH 鍵認証**
   - パスワード認証なし
   - Jenkins 認証情報に鍵を保存
   - 一時鍵ファイル（600パーミッション）
   - 各ビルド後に鍵を削除

4. **Jenkins RBAC**
   - ロールベースのアクセス制御
   - パイプラインレベルの権限
   - 認証情報のアクセス制限
   - 監査ログの有効化

5. **シークレット管理**
   - コードやログにシークレットを含めない
   - 認証情報のバインディングのみ
   - 環境変数のマスキング
   - 自動シークレットローテーション（オプション）

### 認証情報のフロー

```mermaid
flowchart LR
    subgraph "Jenkins Master"
        CS[Credentials Store<br/>Encrypted at Rest]
        JM[Jenkins Master]
    end

    subgraph "Jenkins Agent"
        WS[Workspace<br/>Temp Files]
        KEY[SSH Key File<br/>600 permissions]
    end

    subgraph "Target Hosts"
        TH[EC2 Instances<br/>Authorized Keys]
    end

    CS -->|Binding| JM
    JM -->|Secure Copy| KEY
    KEY -->|SSH Auth| TH
    WS -.->|Cleanup| X[Deleted]
    KEY -.->|Cleanup| X

    style CS fill:#fdeaa8
    style KEY fill:#fadbd8
    style X fill:#e8e8e8
```

## バッチ処理

システムは自動バッチ処理を使用して、あらゆるスケールのデプロイに対応します。デフォルトでは、ホストは256台ずつのバッチで処理され、バッチ内のすべてのホストは並列でデプロイされます。

### バッチ処理の仕組み

```text
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

### スケーリング特性

**デプロイ速度（デフォルト BATCH_SIZE=256）:**

- 10台 → 1バッチ → 約2分
- 100台 → 1バッチ → 約3分
- 500台 → 2バッチ → 約6分
- 1,000台 → 4バッチ → 約12分
- 5,000台 → 20バッチ → 約60分

**速度に影響する要因:**

- ネットワーク帯域幅（ホストあたり19MBのパッケージ）
- SSH 接続のオーバーヘッド（ホストあたり約1秒）
- ターゲットホストの CPU/ディスク速度
- Jenkins エージェントのリソース

## 次のステップ

アーキテクチャを理解したところで、Jenkins のセットアップと認証情報の設定に進みます。
