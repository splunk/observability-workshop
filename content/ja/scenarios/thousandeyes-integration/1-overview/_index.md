---
title: 概要
linkTitle: 1. 概要
weight: 1
time: 10 minutes
description: ThousandEyes エージェントモデルと、Kubernetes、ThousandEyes、Splunk Observability Cloud にまたがるワークショップアーキテクチャを理解します。
---

## ThousandEyes エージェントタイプ

### Enterprise Agent

Enterprise Agent は、自社のインフラストラクチャ内にデプロイするソフトウェアベースの監視エージェントです。以下の機能を提供します

- **内部からの可視性**: 内部ネットワークから外部サービスへの監視とテスト
- **カスタマイズ可能な配置**: ユーザーとアプリケーションが存在する場所にデプロイ
- **フルテスト機能**: HTTP、ネットワーク、DNS、音声、その他のテストタイプ
- **永続的な監視**: スケジュールされたテストを実行し続けるエージェント

このワークショップでは、Enterprise Agent を Kubernetes クラスター内のコンテナ化されたワークロードとしてデプロイします。

### Endpoint Agent

Endpoint Agent は、エンドユーザーのデバイス（ラップトップ、デスクトップ）にインストールされる軽量なエージェントで、以下の機能を提供します

- **実際のユーザー視点**: 実際のユーザーエンドポイントからの監視
- **ブラウザベースの監視**: リアルユーザーエクスペリエンスメトリクスのキャプチャ
- **セッションデータ**: ユーザーの視点からのアプリケーションパフォーマンスに関する詳細なインサイト

このワークショップでは、**Enterprise Agent** のデプロイのみに焦点を当てます。

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
  - ネットワークモード: IPv4 のみ（環境変数 `TEAGENT_INET: "4"` で設定）
  - イメージプルポリシー: `Always`（最新のイメージが確実にプルされます）
  - Init コマンド: `/sbin/my_init`（エージェントの適切な初期化に必要）
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

- **ThousandEyes Cloud**: 以下の機能を提供する中央プラットフォーム
  - エージェントの登録と管理
  - テストの設定とスケジューリング
  - メトリクスの収集と集約
  - 組み込みアラートエンジン
- **ThousandEyes API**: プログラマティックアクセスのための RESTful API（v7/stream エンドポイント）

### 4. テストタイプとメトリクス

Enterprise Agent は以下を実行します

- **HTTP/HTTPS テスト**: Web ページの可用性、レスポンスタイム、ステータスコード
- **DNS テスト**: 名前解決時間、レコード検証
- **ネットワークレイヤーテスト**: レイテンシー、パケットロス、パス可視化
- **Voice/RTP テスト**: 音声トラフィックの品質メトリクス

収集されるメトリクスは以下の通りです

- HTTP サーバー可用性（%）
- スループット（bytes/s）
- リクエスト時間（秒）
- ページロード完了率（%）
- エラーコードと失敗理由

### 5. Splunk Observability Cloud との統合

- **OpenTelemetry Metrics Stream**:
  - エンドポイント: `https://ingest.{realm}.signalfx.com/v2/datapoint/otlp`
  - プロトコル: HTTP または gRPC
  - フォーマット: Protobuf
  - 認証: `X-SF-Token` ヘッダー
  - シグナルタイプ: Metrics（OpenTelemetry v2）
- **分散トレーシング統合**:
  - ThousandEyes テストタイプ: 分散トレーシングが有効な **HTTP Server** または **API**
  - ThousandEyes コネクターターゲット: `https://api.{realm}.signalfx.com`
  - 認証: `X-SF-Token` ヘッダーの Splunk **API** トークン
  - 結果: ThousandEyes から関連する Splunk APM トレースを開くことができ、Splunk APM トレースから元の ThousandEyes テストにリンクバックできます
- **オブザーバビリティ機能**:
  - **Metrics**: ThousandEyes データのリアルタイム可視化
  - **Dashboards**: 統合ビューを備えた構築済み ThousandEyes ダッシュボード
  - **APM/RUM 統合**: シンセティックテストとアプリケーショントレースおよびリアルユーザーモニタリングの相関
  - **Alerting**: 相関ルールを備えた一元的なアラート管理

### 6. データフロー

1. エージェントが Kubernetes Secret のトークンを使用して認証します
2. エージェントが内部および外部のターゲットに対してスケジュールされたテストを実行します
3. テスト結果が ThousandEyes Cloud に送信されます
4. ThousandEyes が OpenTelemetry プロトコル経由で Splunk にメトリクスをストリーミングします
5. 分散トレーシングが有効な HTTP Server および API テストでは、ThousandEyes がリクエストに `b3`、`traceparent`、`tracestate` ヘッダーを挿入します
6. インストルメント済みアプリケーションが結果のトレースを Splunk APM に送信します
7. ThousandEyes から関連する Splunk トレースを開くことができ、Splunk APM から元の ThousandEyes テストにリンクバックできます
8. DevOps、ネットワーク、アプリケーションチームが調査中に両方のビューを使用して連携します

## テスト機能

このデプロイにより、以下のことが可能になります

- ✅ **内部サービスのテスト**: クラスター内から Kubernetes サービス、API、マイクロサービスを監視します
- ✅ **外部依存関係のテスト**: 決済ゲートウェイ、サードパーティ API、SaaS プラットフォームへの接続性を検証します
- ✅ **パフォーマンスの測定**: クラスターの視点からレイテンシー、可用性、パフォーマンスメトリクスをキャプチャします
- ✅ **問題のトラブルシューティング**: 問題がインフラストラクチャ、ネットワークパス、またはインストルメント済みアプリケーションサービスのいずれに起因するかを特定します

{{% notice title="注意" style="info" %}}
これは ThousandEyes エージェントの**公式にサポートされたデプロイ構成ではありません**。ただし、本番環境に近い環境でテスト済みであり、非常にうまく動作します。
{{% /notice %}}
