---
title: Kubernetes サービステストと相関分析
linkTitle: 5. Kubernetes テスト
weight: 5
time: 20 minutes
description: シンセティック監視とトレース相関分析の両方に役立つ、内部 Kubernetes テストおよび外部依存関係テストを作成します。
---

## AppDynamics テスト推奨の再現

AppDynamics には「Test Recommendations」と呼ばれる機能があり、アプリケーションのエンドポイントに対するシンセティックテストを自動的に提案します。Kubernetes クラスター内に ThousandEyes をデプロイすることで、Kubernetes のサービスディスカバリと Splunk Observability Cloud の統合ビューを組み合わせて、この機能を再現できます。

ThousandEyes Enterprise Agent は**クラスター内部**で動作するため、サービス名をホスト名として使用して内部 Kubernetes サービスを直接テストできます。これにより、外部に公開されていないバックエンドサービスを監視する強力な方法が提供されます。

## 仕組み

1. **サービスディスカバリ**: `kubectl get svc` を使用してクラスター内のサービスを列挙します
2. **ホスト名の構築**: Kubernetes DNS の命名規則 `<service-name>.<namespace>.svc.cluster.local` を使用してテスト URL を構築します
3. **テストの作成**: 内部サービスに対して可用性テストとトレース対応トランザクションテストの両方を作成します
4. **Splunk での相関分析**: シンセティックテストの結果を APM トレースやインフラストラクチャメトリクスと並べて表示します

## クラスター内テストの利点

- **内部サービスの監視**: インターネットに公開されていないバックエンドサービスをテストできます
- **サービスメッシュ対応**: Istio、Linkerd、その他のサービスメッシュの背後にあるサービスを監視できます
- **DNS 解決テスト**: Kubernetes DNS とサービスディスカバリを検証できます
- **ネットワークポリシーの検証**: ネットワークポリシーが適切な通信を許可していることを確認できます
- **レイテンシベースライン**: クラスター内部のネットワークパフォーマンスを測定できます
- **本番前テスト**: Ingress/LoadBalancer で公開する前にサービスをテストできます

## ワークショップターゲット: Spring PetClinic

このリポジトリには、ThousandEyes ガイドの Kubernetes ターゲットとして使用できる Spring PetClinic マイクロサービスアプリケーションが既に含まれています。デプロイメントマニフェストは `workshop/petclinic/deployment.yaml` にあり、ワークショップ VM では `~/workshop/petclinic/deployment.yaml` で利用可能です。

このマニフェストは、PetClinic のフロントエンド/API ゲートウェイ、バックエンドサービス、MySQL データベース、およびロードジェネレーターをデプロイします。また、以下も作成されます:

- ポート `82` の `ClusterIP` サービスとしての `api-gateway`
- ポート `81` の `LoadBalancer` サービスとしての `api-gateway-external`
- 内部バックエンドサービスとしての `customers-service`、`vets-service`、`visits-service`

{{% notice title="トレーシングのセットアップ" style="info" %}}
既に Splunk OpenTelemetry Operator をインストール済みで、PetClinic をトレース相関分析に使用する予定の場合は、このマニフェストを適用する前に Distributed Tracing セクションで PetClinic のインストルメンテーションセットアップを完了してください。PetClinic マニフェストには一部のサービスに Java インジェクションアノテーションが含まれており、Operator Webhook がアクティブな場合、これらのアノテーションには対応する `Instrumentation` リソースが必要です。
{{% /notice %}}

選択した Namespace に PetClinic をデプロイします:

```bash
PETCLINIC_NAMESPACE=default

kubectl create namespace $PETCLINIC_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic workshop-secret \
  -n $PETCLINIC_NAMESPACE \
  --from-literal=app=${INSTANCE:-thousandeyes}-petclinic-service \
  --from-literal=env=${INSTANCE:-thousandeyes}-petclinic \
  --from-literal=realm=${REALM:-us1} \
  --from-literal=rum_token=${RUM_TOKEN:-not-used} \
  --from-literal=url=http://api-gateway:82 \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -n $PETCLINIC_NAMESPACE -f ~/workshop/petclinic/deployment.yaml
```

以下の例では、PetClinic が `default` Namespace にデプロイされていることを前提としています。別の Namespace にデプロイした場合は、サービス DNS 名の `default` を使用した Namespace に置き換えてください。

アプリケーションリソースを確認します:

```bash
kubectl get pods -n $PETCLINIC_NAMESPACE
kubectl get svc -n $PETCLINIC_NAMESPACE api-gateway api-gateway-external customers-service vets-service visits-service
```

ThousandEyes エージェントが動作している Namespace からクラスター内部の到達性を検証します:

```bash
kubectl run te-petclinic-curl \
  -n te-demo \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.$PETCLINIC_NAMESPACE.svc.cluster.local:82/api/customer/owners
```

ThousandEyes テストに使用する PetClinic の URL です:

```text
Availability test:
http://api-gateway.default.svc.cluster.local:82/

Trace-enabled API test:
http://api-gateway.default.svc.cluster.local:82/api/customer/owners

Additional API test targets:
http://api-gateway.default.svc.cluster.local:82/api/vet/vets
http://api-gateway.default.svc.cluster.local:82/api/visit/owners/1/pets/1/visits
```

{{% notice title="Namespace に関する注意" style="info" %}}
ThousandEyes Enterprise Agent は `te-demo` で動作し、PetClinic は `default` で動作できます。エージェントとターゲットアプリケーションが異なる Namespace にある場合は、`api-gateway.default.svc.cluster.local` のような完全な Kubernetes DNS 名を使用してください。
{{% /notice %}}

## PetClinic 用の ThousandEyes テストの設定

少なくとも 2 つの PetClinic テストを作成します: フロントエンド用のシンプルな可用性テストと、APM 相関分析用のトレース対応 API テストです。両方のテストで同じ Kubernetes Enterprise Agent を使用し、クラスター内部から測定を行います。

エンドポイントを検証する際のターゲット URL のシェル変数を設定します:

```bash
PETCLINIC_NAMESPACE=default
PETCLINIC_BASE_URL="http://api-gateway.$PETCLINIC_NAMESPACE.svc.cluster.local:82"

kubectl run te-petclinic-curl \
  -n te-demo \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS "$PETCLINIC_BASE_URL/api/customer/owners"
```

### テスト 1: PetClinic フロントエンドの可用性

このテストは、ThousandEyes Enterprise Agent からアプリケーションフロントエンドに到達可能であることを確認するために使用します。

1. ThousandEyes で **Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** を選択します。
3. テストを設定します:
   - **Test Name**: `[PetClinic] Frontend Availability`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/`
   - **Interval**: `2 minutes`
   - **Agents**: このガイドの前の手順でデプロイした Kubernetes Enterprise Agent を選択します
   - **HTTP Response Code**: `200`
   - **Verify Content**: オプション。返されるページコンテンツを検証したい場合は `PetClinic` を使用します
4. テストを保存します。

### テスト 2: 分散トレーシング付き PetClinic Owners API

このテストは、ThousandEyes と Splunk APM のドリルダウンワークフローに使用します。API ゲートウェイをターゲットにし、`customers-service` にルーティングされるため、浅いヘルスチェックよりも有用なトレースが得られます。

1. ThousandEyes で **Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** または **API** を選択します。
3. テストを設定します:
   - **Test Name**: `[Trace] PetClinic Owners API`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`
   - **Method**: `GET`
   - **Interval**: `2 minutes`
   - **Agents**: 同じ Kubernetes Enterprise Agent を選択します
   - **HTTP Response Code**: `200`
   - **Advanced Settings > Distributed Tracing**: Enabled

**Basic Settings** でハイライトされたフィールドは、PetClinic API ターゲットとクラスター内の Enterprise Agent に一致する必要があります:

![PetClinic ThousandEyes HTTP Server の基本設定](../images/te-petclinic-basic-settings.png)

**HTTP Communication and Performance** で分散トレーシングを有効にし、API リクエストは `GET` のまま、デフォルトの `2xx` または `3xx` レスポンス検証を維持します:

![PetClinic ThousandEyes HTTP Server のトレーシング設定](../images/te-petclinic-http-settings.png)

4. テストを保存し、数回のインターバル分実行させます。

{{% notice title="トレーステストの要件" style="warning" %}}
分散トレーシングの演習には **HTTP Server** または **API** テストを使用してください。ブラウザスタイルのページロードおよびトランザクションテストはエンドユーザー監視に有用ですが、ThousandEyes と Splunk APM のワークフローに必要なトレースヘッダーを注入するための適切なテストタイプではありません。
{{% /notice %}}

### オプションの PetClinic API テスト

最初の 2 つのテストが動作した後、他の PetClinic サービスをカバーする API テストを追加します:

```text
[Trace] PetClinic Vets API
http://api-gateway.default.svc.cluster.local:82/api/vet/vets

[Trace] PetClinic Owner Visits API
http://api-gateway.default.svc.cluster.local:82/api/visit/owners/1/pets/1/visits
```

同じベースライン設定を使用します:

- **Test Type**: HTTP Server または API
- **Method**: `GET`
- **Interval**: `2 minutes`
- **Agent**: Kubernetes Enterprise Agent
- **Expected Response Code**: `200`
- **Distributed Tracing**: Splunk APM 相関分析が必要な場合は Enabled

PetClinic を `default` Namespace 以外にデプロイした場合は、各 URL の `default` を PetClinic の Namespace に置き換えてください。

## ステップバイステップガイド

### 1. Kubernetes サービスの検出

クラスター内のすべてのサービスまたは特定の Namespace のサービスを一覧表示します:

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

Kubernetes サービスは以下の命名パターンを使用して DNS 経由でアクセスできます:

```
<service-name>.<namespace>.svc.cluster.local
```

上記のサービスの場合:

- `api-gateway.production.svc.cluster.local:8080`
- `payment-svc.production.svc.cluster.local:8080`
- `auth-service.production.svc.cluster.local:9000`

**同一 Namespace 内の短縮形:**
ThousandEyes エージェントと同じ Namespace のサービスをテストする場合、サービス名のみで指定できます:

- `api-gateway:8080`
- `payment-svc:8080`

### 3. 内部サービス用の ThousandEyes テストの作成

最良の学習成果を得るには、**2 種類のテスト**を作成します:

- `/health` または `/readiness` エンドポイントに対する**可用性テスト**で、到達性とレスポンスタイムを検証します
- 複数のサービスを横断するビジネスエンドポイントに対する**トレース対応トランザクションテスト**

最初のテストではシンセティック監視を学びます。2 番目のテストでは Splunk APM を使用したクロスツールトラブルシューティングを学びます。

#### ThousandEyes UI 経由

1. **Cloud & Enterprise Agents > Test Settings** に移動します
2. **Add New Test** → **HTTP Server** をクリックします
3. 可用性テストを設定します:
   - **Test Name**: `[K8s] API Gateway Health`
   - **URL**: `http://api-gateway.production.svc.cluster.local:8080/health`
   - **Interval**: 2 minutes
   - **Agents**: Kubernetes にデプロイした Enterprise Agent を選択します
   - **HTTP Response Code**: `200`
4. トレース対応トランザクションテストを設定します:
   - **Test Name**: `[Trace] API Gateway Orders`
   - **URL**: `http://api-gateway.production.svc.cluster.local:8080/api/v1/orders`
   - **Interval**: 2 minutes
   - **Agents**: Kubernetes にデプロイした Enterprise Agent を選択します
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

トレース対応バージョンの場合は、`url` をビジネストランザクションエンドポイントに切り替え、ThousandEyes テスト設定で分散トレーシングを有効にします。

{{% notice title="ベストプラクティス" style="success" icon="check" %}}
分散トレーシングを教えることが目的の場合、`/health` のみを例として使用することは避けてください。ヘルスチェックは稼働時間の監視に有用ですが、ThousandEyes と Splunk APM の統合を説得力のあるものにするマルチサービストレースを生成することはほとんどありません。
{{% /notice %}}

### 4. アラートルールの設定

一般的な障害シナリオに対するアラートを設定します:

- **可用性アラート**: HTTP レスポンスが 200 でない場合にトリガーします
- **パフォーマンスアラート**: レスポンスタイムがベースラインを超えた場合にトリガーします
- **DNS 解決アラート**: サービス DNS が解決できない場合にトリガーします

### 5. Splunk Observability Cloud での結果の表示

テストが実行され、Splunk と統合された後:

1. Splunk Observability Cloud の **ThousandEyes ダッシュボード**に移動します
2. **テスト名でフィルター**します（例: `[K8s]` プレフィックス）。すべての Kubernetes 内部テストを表示できます
3. **トレース対応テストの場合、まず ThousandEyes から開始します**:
   - **Service Map** を開きます
   - サービスレベルのレイテンシとダウンストリームエラーを調査します
   - **Splunk APM** へのリンクをたどります
4. **APM データとの相関分析**:
   - シンセティックテストの失敗を APM のエラー率と並べて表示します
   - 問題がネットワーク関連（ThousandEyes）かアプリケーション関連（APM）かを特定します
   - Splunk のトレースメタデータを使用して、元の ThousandEyes テストに戻ります
5. **カスタムダッシュボードの作成**。以下を組み合わせます:
   - ThousandEyes HTTP 可用性メトリクス
   - APM サービスのレイテンシとエラー率
   - Kubernetes インフラストラクチャメトリクス（CPU、メモリ、Pod の再起動）

## ユースケースの例

### ユースケース 1: マイクロサービスのヘルスチェック

複数のマイクロサービスのヘルスエンドポイントをテストします:

```bash
http://user-service.production.svc.cluster.local:8080/actuator/health
http://order-service.production.svc.cluster.local:8080/actuator/health
http://inventory-service.production.svc.cluster.local:8080/actuator/health
```

### ユースケース 2: API Gateway エンドポイントテスト

有用なトレースを生成しやすい API Gateway ルートをテストします:

```bash
http://api-gateway.production.svc.cluster.local:8080/api/v1/users
http://api-gateway.production.svc.cluster.local:8080/api/v1/orders
http://api-gateway.production.svc.cluster.local:8080/api/v1/products
```

### ユースケース 3: データベース接続テスト

ThousandEyes は主に HTTP テスト用ですが、データベースプロキシもテストできます:

```bash
# Test PgBouncer or database HTTP management interfaces
http://pgbouncer.production.svc.cluster.local:8080/stats
http://redis-exporter.production.svc.cluster.local:9121/metrics
```

### ユースケース 4: 外部サービスの依存関係

クラスター内の ThousandEyes エージェントの最も価値のある機能の 1 つは、サービスと同じネットワーク視点からアプリケーションの外部依存関係を監視できることです。これにより、問題がインフラストラクチャ、ネットワークパス、または外部サービス自体のいずれに起因するかを特定できます。

#### 決済ゲートウェイのテスト

重要な決済ゲートウェイエンドポイントの可用性とパフォーマンスを確認するテストを作成します:

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

#### 外部依存関係を監視する理由

- **プロアクティブな問題検出**: 顧客から報告される前に決済ゲートウェイの障害を把握できます
- **ネットワークパスの検証**: Kubernetes のエグレスネットワークが外部サービスに到達できることを確認できます
- **パフォーマンスベースライン**: クラスターから外部 API へのレイテンシを追跡できます
- **コンプライアンスと SLA の監視**: サードパーティサービスが SLA コミットメントを満たしていることを検証できます
- **根本原因分析**: 問題がネットワーク関連、自社インフラストラクチャ、または外部プロバイダーのいずれに起因するかを迅速に判断できます

#### 監視を推奨する外部サービス

- **決済プロセッサ**: Stripe、PayPal、Square、Braintree
- **認証プロバイダー**: Auth0、Okta、Azure AD
- **メールサービス**: SendGrid、Mailgun、AWS SES
- **SMS/コミュニケーション**: Twilio、MessageBird
- **CDN エンドポイント**: Cloudflare、Fastly、Akamai
- **クラウドストレージ**: AWS S3、Google Cloud Storage、Azure Blob Storage
- **サードパーティ API**: 重要なビジネスパートナー API

{{% notice title="ベストプラクティス" style="success" icon="check" %}}
テスト名に `[External]` プレフィックスを使用すると、ダッシュボードで内部 Kubernetes サービスと外部依存関係を簡単に区別できます。
{{% /notice %}}

## ベストプラクティス

1. **一貫した命名規則を使用する**: テスト名に `[K8s]` や `[Internal]` などのプレフィックスを付けてフィルタリングを容易にします
2. **まずヘルスエンドポイントをテストする**: ビジネスロジックをテストする前に `/health` や `/readiness` エンドポイントから始めます
3. **適切なインターバルを設定する**: 重要なサービスにはより短いインターバル（1～2 分）を使用します
4. **テストにタグを付ける**: ThousandEyes のラベル/タグを使用して、以下の基準でテストをグループ化します:
   - 環境（dev、staging、production）
   - サービスタイプ（API、database、cache）
   - チームの所有者
5. **テストエージェントの健全性を監視する**: ThousandEyes エージェント Pod が正常で、十分なリソースを持っていることを確認します
6. **両方のテストタイプを使用する**: 重要な各サービスパスに対して、シンプルな可用性テストとトレース対応のビジネストランザクションテストを組み合わせます
7. **APM との相関分析**: シンセティックデータと APM データを並べて表示する Splunk ダッシュボードを作成します
8. **トレースラボにはインストルメント済みバックエンドを使用する**: 分散トレーシングは、ThousandEyes のターゲットが OpenTelemetry でインストルメントされたサービスに支えられた HTTP Server または API エンドポイントである場合に最も効果的です

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
内部サービスを外部に公開する前にテストすることで、問題を早期に発見し、ユーザートラフィックが到達する前にインフラストラクチャが正常であることを確認できます。
{{% /notice %}}
