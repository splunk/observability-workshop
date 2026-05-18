---
title: 概要
linkTitle: 1. Overview
weight: 1
time: 10 minutes
description: ThousandEyes エージェントモデルと、Kubernetes、ThousandEyes、Splunk Observability Cloud にまたがるワークショップアーキテクチャを理解します。
---

## ThousandEyes エージェントタイプ

### Enterprise Agents

Enterprise Agents は、自社のインフラストラクチャ内にデプロイするソフトウェアベースの監視エージェントです。以下の機能を提供します

- **内部からの可視性**: 内部ネットワークから外部サービスへの監視とテスト
- **カスタマイズ可能な配置**: ユーザーとアプリケーションがある場所にデプロイ可能
- **フルテスト機能**: HTTP、ネットワーク、DNS、音声、その他のテストタイプ
- **永続的な監視**: スケジュールされたテストを実行する常時稼働エージェント

このワークショップでは、Enterprise Agent を Kubernetes クラスター内のコンテナ化されたワークロードとしてデプロイします。

### Endpoint Agents

Endpoint Agents は、エンドユーザーデバイス（ノートPC、デスクトップ）にインストールされる軽量エージェントで、以下を提供します

- **実際のユーザー視点**: 実際のユーザーエンドポイントからの監視
- **ブラウザベースの監視**: 実際のユーザーエクスペリエンスメトリクスのキャプチャ
- **セッションデータ**: ユーザーの視点からのアプリケーションパフォーマンスに関する詳細な洞察

このワークショップでは **Enterprise Agent** のデプロイのみを扱います。

## アーキテクチャ

```mermaid
---
config:
  theme: 'base'
---
graph LR
    subgraph k8s["Kubernetes Cluster"]
        secret["Secret<br/>te-creds"]
        agent["ThousandEyes<br/>Enterprise Agent<br/>Pod"]
        
        subgraph apps["Application Pods"]
            api["API Gateway<br/>Pod"]
            customers["Customers Service<br/>Pod"]
            vets["Vets Service<br/>Pod"]
            visits["Visits Service<br/>Pod"]
        end
        
        subgraph svcs["Services"]
            api_svc["api-gateway<br/>Service"]
            customers_svc["customers-service<br/>Service"]
            vets_svc["vets-service<br/>Service"]
            visits_svc["visits-service<br/>Service"]
        end
        
        api_svc --> api
        customers_svc --> customers
        vets_svc --> vets
        visits_svc --> visits
        
        secret -.-> agent
        agent -->|"HTTP Tests"| api_svc
        agent -->|"HTTP Tests"| customers_svc
        agent -->|"HTTP Tests"| vets_svc
        agent -->|"HTTP Tests"| visits_svc
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
    style customers fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style vets fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style visits fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style api_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style customers_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style vets_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style visits_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
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

- **Secret (te-creds)**: 認証用の base64 エンコードされた `TEAGENT_ACCOUNT_TOKEN` を保存します
- **ThousandEyes Enterprise Agent Pod**:
  - コンテナイメージ: `thousandeyes/enterprise-agent:latest`
  - ホスト名: `te-agent-aleccham`（カスタマイズ可能）
  - セキュリティケーパビリティ: `NET_ADMIN`、`SYS_ADMIN`（ネットワークテストに必要）
  - メモリ割り当て: 2GB リクエスト、3.5GB リミット
  - ネットワークモード: IPv4 のみ（`TEAGENT_INET: "4"` 環境変数で設定）
  - イメージプルポリシー: `Always`（最新イメージが確実にプルされます）
  - Init コマンド: `/sbin/my_init`（適切なエージェント初期化に必要）
- **内部サービス**: REST API、マイクロサービス、データベース、gRPC サービスを含む Kubernetes ワークロード

### 2. テスト対象

- **内部サービス**: Kubernetes クラスター内のサービスを監視します
- **外部サービス**: 以下のような外部依存関係をテストします
  - 決済ゲートウェイ（Stripe、PayPal）
  - サードパーティ API
  - SaaS アプリケーション
  - CDN エンドポイント
  - パブリック Web サイト

### 3. ThousandEyes Platform

- **ThousandEyes Cloud**: 以下の中央プラットフォーム
  - エージェントの登録と管理
  - テストの設定とスケジューリング
  - メトリクスの収集と集約
  - 組み込みアラートエンジン
- **ThousandEyes API**: プログラムによるアクセスのための RESTful API（v7/stream エンドポイント）

### 4. テストタイプとメトリクス

Enterprise Agent は以下を実行します

- **HTTP/HTTPS テスト**: Web ページの可用性、応答時間、ステータスコード
- **DNS テスト**: 名前解決時間、レコード検証
- **ネットワークレイヤーテスト**: レイテンシ、パケットロス、パス可視化
- **Voice/RTP テスト**: 音声トラフィックの品質メトリクス

収集されるメトリクスには以下が含まれます

- HTTP サーバー可用性（%）
- スループット（bytes/s）
- リクエスト時間（秒）
- ページロード完了率（%）
- エラーコードと障害理由

### 5. Splunk Observability Cloud との統合

- **OpenTelemetry Metrics Stream**:
  - エンドポイント: `https://ingest.{realm}.signalfx.com/v2/datapoint/otlp`
  - プロトコル: HTTP または gRPC
  - フォーマット: Protobuf
  - 認証: `X-SF-Token` ヘッダー
  - シグナルタイプ: Metrics（OpenTelemetry v2）
- **分散トレーシング統合**:
  - ThousandEyes テストタイプ: 分散トレーシングが有効な **HTTP Server** または **API**
  - ThousandEyes コネクタターゲット: `https://api.{realm}.signalfx.com`
  - 認証: `X-SF-Token` ヘッダーの Splunk **API** トークン
  - 結果: ThousandEyes は関連する Splunk APM トレースを開くことができ、Splunk APM トレースは元の ThousandEyes テストにリンクバックできます
- **オブザーバビリティ機能**:
  - **Metrics**: ThousandEyes データのリアルタイム可視化
  - **Dashboards**: 統合ビューを備えた構築済み ThousandEyes ダッシュボード
  - **APM/RUM 統合**: シンセティックテストとアプリケーショントレースおよびリアルユーザーモニタリングの相関
  - **Alerting**: 相関ルールを備えた一元的なアラート管理

### 6. データフロー

1. エージェントが Kubernetes Secret のトークンを使用して認証します
2. エージェントが内部および外部ターゲットに対してスケジュールされたテストを実行します
3. テスト結果が ThousandEyes Cloud に送信されます
4. ThousandEyes が OpenTelemetry プロトコル経由で Splunk にメトリクスをストリーミングします
5. 分散トレーシングが有効な HTTP Server および API テストの場合、ThousandEyes はリクエストに `b3`、`traceparent`、`tracestate` ヘッダーを注入します
6. 計装されたアプリケーションが結果のトレースを Splunk APM に送信します
7. ThousandEyes は関連する Splunk トレースを開くことができ、Splunk APM は元の ThousandEyes テストにリンクバックできます
8. DevOps、ネットワーク、アプリケーションチームが調査中に両方のビューで連携します

## テスト機能

このデプロイにより、以下が可能になります

- ✅ **内部サービスのテスト**: クラスター内から Kubernetes サービス、API、マイクロサービスを監視します
- ✅ **外部依存関係のテスト**: 決済ゲートウェイ、サードパーティ API、SaaS プラットフォームへの接続性を検証します
- ✅ **パフォーマンスの測定**: クラスターの視点からレイテンシ、可用性、パフォーマンスメトリクスをキャプチャします
- ✅ **問題のトラブルシューティング**: 問題がインフラストラクチャ、ネットワークパス、または計装されたアプリケーションサービスのいずれに起因するかを特定します

{{% notice title="Note" style="info" %}}
これは ThousandEyes エージェントデプロイの**公式にサポートされた構成ではありません**。ただし、テスト済みであり、本番環境に近い環境で非常にうまく動作します。
{{% /notice %}}
