---
title: 概要
linkTitle: 1. 概要
weight: 1
time: 10 minutes
description: Kubernetes、ThousandEyes、Splunk Observability Cloud にまたがるワークショップアーキテクチャと ThousandEyes エージェントモデルについて理解します。
---

## ThousandEyes エージェントの種類

### Enterprise Agents

Enterprise Agentsは、お客様のインフラストラクチャ内にデプロイするソフトウェアベースの監視エージェントです。以下の機能を提供します：

- **内部から外部への可視性**: 内部ネットワークから外部サービスへの監視とテスト
- **カスタマイズ可能な配置**: ユーザーやアプリケーションが存在する場所にデプロイ
- **完全なテスト機能**: HTTP、ネットワーク、DNS、音声、その他のテストタイプ
- **継続的な監視**: スケジュールされたテストを実行する常時稼働エージェント

このワークショップでは、Enterprise AgentをKubernetesクラスター内のコンテナ化されたワークロードとしてデプロイします。

### Endpoint Agents

Endpoint Agentsは、エンドユーザーデバイス（ラップトップ、デスクトップ）にインストールされる軽量エージェントで、以下の機能を提供します：

- **実際のユーザー視点**: 実際のユーザーエンドポイントからの監視
- **ブラウザベースの監視**: リアルユーザーエクスペリエンスメトリクスの取得
- **セッションデータ**: ユーザーの視点からのアプリケーションパフォーマンスに関する詳細なインサイト

このワークショップでは、**Enterprise Agent** のデプロイのみを対象としています。

## アーキテクチャ

```mermaid
graph LR
    subgraph k8s["Kubernetes Cluster"]
        secret["Secret<br/>te-creds"]
        agent["ThousandEyes<br/>Enterprise Agent<br/>Pod"]

        subgraph apps["Application Pods"]
            api["API Gateway<br/>Pod"]
            payment["Payment Service<br/>Pod"]
            auth["Auth Service<br/>Pod"]
        end

        subgraph svcs["Services"]
            api_svc["api-gateway<br/>Service"]
            payment_svc["payment-svc<br/>Service"]
            auth_svc["auth-service<br/>Service"]
        end

        api_svc --> api
        payment_svc --> payment
        auth_svc --> auth

        secret -.-> agent
        agent -->|"HTTP Tests"| api_svc
        agent -->|"HTTP Tests"| payment_svc
        agent -->|"HTTP Tests"| auth_svc
    end

    external["External<br/>Services"]

    agent --> external

    subgraph te["ThousandEyes Platform"]
        te_cloud["ThousandEyes<br/>Cloud"]
        te_api["API<br/>v7/stream"]
        te_cloud <--> te_api
    end

    agent -->|"Test Results"| te_cloud

    subgraph splunk["Splunk Observability Cloud"]
        otel["OpenTelemetry<br/>Collector"]
        metrics["Metrics"]
        dashboards["Dashboards"]
        apm["APM/RUM"]
        alerts["Alerts"]

        otel --> metrics
        otel --> dashboards
        metrics --> apm
        dashboards --> alerts
    end

    te_cloud -->|"OTel/HTTP metrics"| otel
    te_cloud -->|"Trace lookup"| apm
    apm -->|"Deep links to test"| te_cloud

    user["DevOps/SRE<br/>Team"]
    user -.-> te_cloud
    user -.-> dashboards
    user -.-> agent

    style k8s fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style apps fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style svcs fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style agent fill:#ffeb3b,stroke:#f57c00,stroke-width:2px
    style secret fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style api fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style payment fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style auth fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style api_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style payment_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style auth_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style external fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    style te fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style te_cloud fill:#ffecb3,stroke:#f57f17,stroke-width:2px
    style te_api fill:#ffe082,stroke:#f57f17,stroke-width:2px
    style splunk fill:#ff6e40,stroke:#d84315,stroke-width:2px
    style otel fill:#ff8a65,stroke:#d84315,stroke-width:2px
    style metrics fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style dashboards fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style apm fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style alerts fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style user fill:#b2dfdb,stroke:#00695c,stroke-width:2px
```

## アーキテクチャコンポーネント

### 1. Kubernetes クラスター

- **Secret (te-creds)**: 認証用のbase64エンコードされた `TEAGENT_ACCOUNT_TOKEN` を保存
- **ThousandEyes Enterprise Agent Pod**:
  - コンテナイメージ: `thousandeyes/enterprise-agent:latest`
  - ホスト名: `te-agent-aleccham`（カスタマイズ可能）
  - セキュリティ権限: `NET_ADMIN`、`SYS_ADMIN`（ネットワークテストに必要）
  - メモリ割り当て: 2GBリクエスト、3.5GB上限
  - ネットワークモード: IPv4のみ（環境変数 `TEAGENT_INET: "4"` で設定）
  - イメージプルポリシー: `Always`（最新イメージのプルを保証）
  - Initコマンド: `/sbin/my_init`（エージェントの適切な初期化に必要）
- **内部サービス**: REST API、マイクロサービス、データベース、gRPCサービスを含むKubernetesワークロード

### 2. テスト対象

- **内部サービス**: Kubernetesクラスター内のサービスを監視
- **外部サービス**: 以下のような外部依存関係をテスト：
  - 決済ゲートウェイ（Stripe、PayPal）
  - サードパーティAPI
  - SaaSアプリケーション
  - CDNエンドポイント
  - 公開ウェブサイト

### 3. ThousandEyes Platform

- **ThousandEyes Cloud**: 以下のための中央プラットフォーム：
  - エージェントの登録と管理
  - テストの設定とスケジューリング
  - メトリクスの収集と集約
  - 組み込みアラートエンジン
- **ThousandEyes API**: プログラムによるアクセスのためのRESTful API（v7/streamエンドポイント）

### 4. テストタイプとメトリクス

Enterprise Agentは以下を実行します：

- **HTTP/HTTPS テスト**: ウェブページの可用性、応答時間、ステータスコード
- **DNS テスト**: 名前解決時間、レコード検証
- **ネットワーク層テスト**: レイテンシ、パケットロス、パス可視化
- **Voice/RTP テスト**: 音声トラフィックの品質メトリクス

収集されるメトリクスには以下が含まれます：

- HTTPサーバー可用性（%）
- スループット（bytes/s）
- リクエスト時間（秒）
- ページロード完了率（%）
- エラーコードと失敗理由

### 5. Splunk Observability Cloud との統合

- **OpenTelemetry Metrics Stream**:
  - エンドポイント: `https://ingest.{realm}.signalfx.com/v2/datapoint/otlp`
  - プロトコル: HTTPまたはgRPC
  - フォーマット: Protobuf
  - 認証: `X-SF-Token` ヘッダー
  - シグナルタイプ: Metrics（OpenTelemetry v2）
- **分散トレーシング統合**:
  - ThousandEyesテストタイプ: 分散トレーシングが有効な **HTTP Server** または **API**
  - ThousandEyesコネクタターゲット: `https://api.{realm}.signalfx.com`
  - 認証: `X-SF-Token` ヘッダーにSplunk **API** トークン
  - 結果: ThousandEyesは関連するSplunk APMトレースを開くことができ、Splunk APMトレースは元のThousandEyesテストにリンクバックできます
- **オブザーバビリティ機能**:
  - **Metrics**: ThousandEyesデータのリアルタイム可視化
  - **Dashboards**: 統合ビューを備えた事前構築済みThousandEyesダッシュボード
  - **APM/RUM 統合**: シンセティックテストとアプリケーショントレースおよびリアルユーザーモニタリングの相関
  - **Alerting**: 相関ルールを備えた一元化されたアラート管理

### 6. データフロー

1. エージェントがKubernetes Secretからのトークンを使用して認証
2. エージェントが内部および外部ターゲットに対してスケジュールされたテストを実行
3. テスト結果がThousandEyes Cloudに送信
4. ThousandEyesがOpenTelemetryプロトコルを介してSplunkにメトリクスをストリーミング
5. 分散トレーシングが有効なHTTP ServerおよびAPIテストの場合、ThousandEyesはリクエストに `b3`、`traceparent`、`tracestate` ヘッダーを挿入
6. 計装されたアプリケーションが結果のトレースをSplunk APMに送信
7. ThousandEyesは関連するSplunkトレースを開くことができ、Splunk APMは元のThousandEyesテストにリンクバック可能
8. DevOps、ネットワーク、アプリケーションチームが調査中に両方のビューで協力

## テスト機能

このデプロイにより、以下が可能になります：

- ✅ **内部サービスのテスト**: クラスター内からKubernetesサービス、API、マイクロサービスを監視
- ✅ **外部依存関係のテスト**: 決済ゲートウェイ、サードパーティAPI、SaaSプラットフォームへの接続性を検証
- ✅ **パフォーマンスの測定**: クラスターの視点からレイテンシ、可用性、パフォーマンスメトリクスを取得
- ✅ **問題のトラブルシューティング**: 問題がインフラストラクチャ、ネットワークパス、または計装されたアプリケーションサービスのいずれに起因するかを特定

{{% notice title="注意" style="info" %}}
これはThousandEyesエージェントの**公式にサポートされた**デプロイ設定**ではありません**。ただし、本番環境に近い環境でテストされており、非常にうまく動作します。
{{% /notice %}}
