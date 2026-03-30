---
title: Kubernetes サービステストと相関
linkTitle: 5. Kubernetes テスト
weight: 5
time: 20 minutes
description: シンセティック監視とトレース相関の両方に役立つ、内部 Kubernetes テストと外部依存関係テストを作成します。
---

## AppDynamics テスト推奨機能の再現

AppDynamicsには、アプリケーションのエンドポイントに対するシンセティックテストを自動的に提案する「Test Recommendations」という機能があります。ThousandEyesをKubernetesクラスター内にデプロイすることで、KubernetesのサービスディスカバリとSplunk Observability Cloudの統合ビューを組み合わせて、この機能を再現できます。

ThousandEyes Enterprise Agentは**クラスター内部**で実行されるため、サービス名をホスト名として使用して内部Kubernetesサービスを直接テストできます。これにより、外部に公開されていないバックエンドサービスを監視する強力な方法が得られます。

## 仕組み

1. **サービスディスカバリ**: `kubectl get svc` を使用してクラスター内のサービスを列挙します
2. **ホスト名の構築**: Kubernetes DNS命名規則を使用してテストURLを構築します: `<service-name>.<namespace>.svc.cluster.local`
3. **テストの作成**: 内部サービスに対して可用性テストとトレース対応トランザクションテストの両方を作成します
4. **Splunk での相関**: シンセティックテストの結果をAPMトレースおよびインフラストラクチャメトリクスと並べて表示します

## クラスター内テストのメリット

- **内部サービス監視**: インターネットに公開されていないバックエンドサービスをテストできます
- **サービスメッシュ対応**: Istio、Linkerd、その他のサービスメッシュの背後にあるサービスを監視できます
- **DNS 解決テスト**: Kubernetes DNSとサービスディスカバリを検証できます
- **ネットワークポリシー検証**: ネットワークポリシーが適切な通信を許可していることを確認できます
- **レイテンシベースライン**: クラスター内部のネットワークパフォーマンスを測定できます
- **本番前テスト**: Ingress/LoadBalancer経由で公開する前にサービスをテストできます

## ステップバイステップガイド

### 1. Kubernetes サービスの検出

クラスター内または特定のnamespace内のすべてのサービスを一覧表示します:

```bash
# Get all services in all namespaces
kubectl get svc --all-namespaces

# Get services in a specific namespace
kubectl get svc -n production

# Get services with detailed output including ports
kubectl get svc -n production -o wide
```

出力例:

```
NAMESPACE    NAME           TYPE        CLUSTER-IP      PORT(S)    AGE
production   api-gateway    ClusterIP   10.96.100.50    8080/TCP   5d
production   payment-svc    ClusterIP   10.96.100.51    8080/TCP   5d
production   auth-service   ClusterIP   10.96.100.52    9000/TCP   5d
production   postgres       ClusterIP   10.96.100.53    5432/TCP   5d
```

### 2. テストホスト名の構築

Kubernetesサービスは、以下の命名パターンを使用してDNS経由でアクセスできます:

```
<service-name>.<namespace>.svc.cluster.local
```

上記のサービスの場合:

- `api-gateway.production.svc.cluster.local:8080`
- `payment-svc.production.svc.cluster.local:8080`
- `auth-service.production.svc.cluster.local:9000`

**同じ namespace 内での省略形:**
ThousandEyesエージェントと同じnamespace内のサービスをテストする場合は、サービス名のみを使用できます:

- `api-gateway:8080`
- `payment-svc:8080`

### 3. 内部サービス用の ThousandEyes テストの作成

最良の学習成果を得るために、**2 種類のテスト**を作成します:

- `/health` または `/readiness` エンドポイントに対する**可用性テスト**で、到達可能性と応答時間を検証します
- 複数のサービスを横断するビジネスエンドポイントに対する**トレース対応トランザクションテスト**

最初のテストはシンセティック監視を学ぶためのものです。2番目のテストはSplunk APMを使用したクロスツールトラブルシューティングを学ぶためのものです。

#### ThousandEyes UI 経由

1. **Cloud & Enterprise Agents > Test Settings** に移動します
2. **Add New Test** → **HTTP Server** をクリックします
3. 可用性テストを設定します:
   - **Test Name**: `[K8s] API Gateway Health`
   - **URL**: `http://api-gateway.production.svc.cluster.local:8080/health`
   - **Interval**: 2 minutes
   - **Agents**: KubernetesにデプロイされたEnterprise Agentを選択します
   - **HTTP Response Code**: `200`
4. トレース対応トランザクションテストを設定します:
   - **Test Name**: `[Trace] API Gateway Orders`
   - **URL**: `http://api-gateway.production.svc.cluster.local:8080/api/v1/orders`
   - **Interval**: 2 minutes
   - **Agents**: KubernetesにデプロイされたEnterprise Agentを選択します
   - **Advanced Settings > Distributed Tracing**: Enabled
5. **Create Test** をクリックします

#### ThousandEyes API 経由

```bash
curl -X POST https://api.thousandeyes.com/v6/tests/http-server/new \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "testName": "[K8s] API Gateway Health",
    "url": "http://api-gateway.production.svc.cluster.local:8080/health",
    "interval": 120,
    "agents": [
      {"agentId": "<your-k8s-agent-id>"}
    ],
    "httpTimeLimit": 5000,
    "targetResponseTime": 1000,
    "alertsEnabled": 1
  }'
```

トレース対応バージョンの場合は、`url` をビジネストランザクションエンドポイントに切り替え、ThousandEyesテスト設定でdistributed tracingを有効にします。

{{% notice title="ベストプラクティス" style="success" icon="check" %}}
distributed tracingを教えることが目的の場合、`/health` だけを例として使用することは避けてください。ヘルスチェックは稼働時間の監視には便利ですが、ThousandEyesとSplunk APMの統合を魅力的にするマルチサービストレースを生成することはほとんどありません。
{{% /notice %}}

### 4. アラートルールの設定

一般的な障害シナリオに対するアラートを設定します:

- **可用性アラート**: HTTPレスポンスが200でない場合にトリガーします
- **パフォーマンスアラート**: レスポンスタイムがベースラインを超えた場合にトリガーします
- **DNS 解決アラート**: サービスDNSが解決できない場合にトリガーします

### 5. Splunk Observability Cloud での結果表示

テストが実行され、Splunkと統合されたら:

1. Splunk Observability Cloudで **ThousandEyes Dashboard** に移動します
2. **テスト名でフィルター**します（例: `[K8s]` プレフィックス）、すべてのKubernetes内部テストを表示します
3. **トレース対応テストの場合は、まず ThousandEyes から開始します**:
   - **Service Map** を開きます
   - サービスレベルのレイテンシとダウンストリームエラーを調べます
   - **Splunk APM** へのリンクをたどります
4. **APM データとの相関**:
   - シンセティックテストの失敗をAPMエラー率と並べて表示します
   - 問題がネットワーク関連（ThousandEyes）かアプリケーション関連（APM）かを特定します
   - Splunkトレースメタデータを使用して、元のThousandEyesテストに戻ります
5. 以下を組み合わせた**カスタムダッシュボードを作成**します:
   - ThousandEyes HTTP可用性メトリクス
   - APMサービスレイテンシとエラー率
   - Kubernetesインフラストラクチャメトリクス（CPU、メモリ、Pod再起動）

## ユースケース例

### ユースケース 1: マイクロサービスヘルスチェック

複数のマイクロサービスヘルスエンドポイントをテストします:

```bash
http://user-service.production.svc.cluster.local:8080/actuator/health
http://order-service.production.svc.cluster.local:8080/actuator/health
http://inventory-service.production.svc.cluster.local:8080/actuator/health
```

### ユースケース 2: API Gateway エンドポイントテスト

有用なトレースを生成する可能性が高いAPI Gatewayルートをテストします:

```bash
http://api-gateway.production.svc.cluster.local:8080/api/v1/users
http://api-gateway.production.svc.cluster.local:8080/api/v1/orders
http://api-gateway.production.svc.cluster.local:8080/api/v1/products
```

### ユースケース 3: データベース接続テスト

ThousandEyesは主にHTTPテスト用ですが、データベースプロキシをテストできます:

```bash
# Test PgBouncer or database HTTP management interfaces
http://pgbouncer.production.svc.cluster.local:8080/stats
http://redis-exporter.production.svc.cluster.local:9121/metrics
```

### ユースケース 4: 外部サービス依存関係

クラスター内ThousandEyesエージェントの最も価値のある機能の1つは、サービスと同じネットワークの視点からアプリケーションの外部依存関係を監視することです。これにより、問題がインフラストラクチャ、ネットワークパス、または外部サービス自体のいずれに起因するかを特定できます。

#### 決済ゲートウェイのテスト

重要な決済ゲートウェイエンドポイントの可用性とパフォーマンスを確保するためのテストを作成します:

**Stripe API:**

```bash
# Via ThousandEyes UI
Test Name: [External] Stripe API Health
URL: https://api.stripe.com/healthcheck
Interval: 2 minutes
Agents: Your Kubernetes Enterprise Agent
Expected Response: 200
```

**PayPal API:**

```bash
Test Name: [External] PayPal API Health
URL: https://api.paypal.com/v1/notifications/webhooks
Interval: 2 minutes
Agents: Your Kubernetes Enterprise Agent
Expected Response: 401 (authentication required, but endpoint is reachable)
```

**ThousandEyes API 経由:**

```bash
curl -X POST https://api.thousandeyes.com/v6/tests/http-server/new \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "testName": "[External] Stripe API Availability",
    "url": "https://api.stripe.com/healthcheck",
    "interval": 120,
    "agents": [
      {"agentId": "<your-k8s-agent-id>"}
    ],
    "httpTimeLimit": 5000,
    "targetResponseTime": 2000,
    "alertsEnabled": 1
  }'
```

#### なぜ外部依存関係を監視するのか？

- **プロアクティブな問題検出**: 顧客から報告される前に決済ゲートウェイの障害を把握できます
- **ネットワークパス検証**: Kubernetesエグレスネットワークが外部サービスに到達できることを確認します
- **パフォーマンスベースライン**: クラスターから外部APIへのレイテンシを追跡します
- **コンプライアンスと SLA 監視**: サードパーティサービスがSLAコミットメントを満たしていることを確認します
- **根本原因分析**: 問題がネットワーク関連か、インフラストラクチャか、外部プロバイダーかを迅速に判断します

#### 監視を推奨する外部サービス

- **決済プロセッサ**: Stripe、PayPal、Square、Braintree
- **認証プロバイダー**: Auth0、Okta、Azure AD
- **メールサービス**: SendGrid、Mailgun、AWS SES
- **SMS/コミュニケーション**: Twilio、MessageBird
- **CDN エンドポイント**: Cloudflare、Fastly、Akamai
- **クラウドストレージ**: AWS S3、Google Cloud Storage、Azure Blob Storage
- **サードパーティ API**: 重要なビジネスパートナー API

{{% notice title="ベストプラクティス" style="success" icon="check" %}}
テスト名に `[External]` プレフィックスを使用して、ダッシュボードで内部Kubernetesサービスと外部依存関係を簡単に区別できるようにします。
{{% /notice %}}

## ベストプラクティス

1. **一貫した命名を使用する**: フィルタリングを容易にするため、テスト名に `[K8s]` または `[Internal]` プレフィックスを付けます
2. **まずヘルスエンドポイントをテストする**: ビジネスロジックをテストする前に `/health` または `/readiness` エンドポイントから始めます
3. **適切な間隔を設定する**: 重要なサービスには短い間隔（1〜2分）を使用します
4. **テストにタグを付ける**: ThousandEyesのラベル/タグを使用してテストをグループ化します:
   - 環境（dev、staging、production）
   - サービスタイプ（API、database、cache）
   - チームオーナーシップ
5. **テストエージェントの健全性を監視する**: ThousandEyesエージェントPodが健全で、十分なリソースがあることを確認します
6. **両方のテストタイプを使用する**: 各重要なサービスパスに対して、シンプルな可用性テストとトレース対応ビジネストランザクションテストをペアにします
7. **APM との相関**: シンセティックデータとAPMデータを並べて表示するSplunkダッシュボードを作成します
8. **トレースラボには計装されたバックエンドを使用する**: distributed tracingは、ThousandEyesのターゲットがOpenTelemetryで計装されたサービスによってバックアップされたHTTP ServerまたはAPIエンドポイントである場合に最も効果的です

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
内部サービスを外部に公開する前にテストすることで、問題を早期に発見し、ユーザートラフィックが到達する前にインフラストラクチャが健全であることを確認できます。
{{% /notice %}}
