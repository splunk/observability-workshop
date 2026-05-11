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

## ワークショップ対象: Spring PetClinic

このリポジトリには、この ThousandEyes ガイドの既知の Kubernetes ターゲットとして使える Spring PetClinic マイクロサービスアプリケーションが含まれています。デプロイメントマニフェストは `workshop/petclinic/deployment.yaml` にあり、ワークショップ VM では `~/workshop/petclinic/deployment.yaml` として利用できます。

このマニフェストは、PetClinic のフロントエンド/API gateway、バックエンドサービス、MySQL データベース、ロードジェネレーターをデプロイします。主なサービスは次のとおりです。

- `api-gateway`: port `82` の `ClusterIP` サービス
- `api-gateway-external`: port `81` の `LoadBalancer` サービス
- `customers-service`、`vets-service`、`visits-service`: 内部バックエンドサービス

{{% notice title="トレーシング設定" style="info" %}}
Splunk OpenTelemetry Operator をすでにインストールしており、PetClinic をトレース相関に使う場合は、このマニフェストを適用する前に Distributed Tracing セクションの PetClinic 計装セットアップを完了してください。PetClinic マニフェストには一部サービスの Java injection アノテーションが含まれており、Operator webhook が有効な場合は対応する `Instrumentation` リソースが必要です。
{{% /notice %}}

PetClinic を選択した namespace にデプロイします。

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

アプリケーションリソースを確認します。

```bash
kubectl get pods -n $PETCLINIC_NAMESPACE
kubectl get svc -n $PETCLINIC_NAMESPACE api-gateway api-gateway-external customers-service vets-service visits-service
```

ThousandEyes agent が動作している namespace から、クラスター内部の到達性を確認します。

```bash
kubectl run te-petclinic-curl \
  -n te-demo \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.$PETCLINIC_NAMESPACE.svc.cluster.local:82/api/customer/owners
```

ThousandEyes テストでは、次の PetClinic URL を使用します。

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
ThousandEyes Enterprise Agent は `te-demo` で実行し、PetClinic は `default` で実行できます。agent とターゲットアプリケーションが別 namespace にある場合は、`api-gateway.default.svc.cluster.local` のような完全な Kubernetes DNS 名を使用してください。
{{% /notice %}}

## PetClinic 用 ThousandEyes テストを設定する

PetClinic テストを少なくとも 2 つ作成します。1 つはフロントエンドのシンプルな可用性テスト、もう 1 つは APM 相関用のトレース対応 API テストです。どちらも同じ Kubernetes Enterprise Agent を使用します。

### Test 1: PetClinic Frontend Availability

1. ThousandEyes で **Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** を選択します。
3. 次のように設定します。
   - **Test Name**: `[PetClinic] Frontend Availability`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/`
   - **Interval**: `2 minutes`
   - **Agents**: このガイドでデプロイした Kubernetes Enterprise Agent
   - **HTTP Response Code**: `200`
   - **Verify Content**: 任意。返却ページの内容を検証したい場合は `PetClinic`
4. テストを保存します。

### Test 2: PetClinic Owners API With Distributed Tracing

このテストは ThousandEyes と Splunk APM のドリルダウンワークフローに使用します。API gateway をターゲットにして `customers-service` にルーティングされるため、単純なヘルスチェックより有用なトレースを生成します。

1. ThousandEyes で **Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** または **API** を選択します。
3. 次のように設定します。
   - **Test Name**: `[Trace] PetClinic Owners API`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`
   - **Method**: `GET`
   - **Interval**: `2 minutes`
   - **Agents**: 同じ Kubernetes Enterprise Agent
   - **HTTP Response Code**: `200`
   - **Advanced Settings > Distributed Tracing**: Enabled

**Basic Settings** のハイライトされたフィールドが PetClinic API ターゲットとクラスター内 Enterprise Agent に一致していることを確認します。

![PetClinic ThousandEyes HTTP Server basic settings](../images/te-petclinic-basic-settings.png)

**HTTP Communication and Performance** で distributed tracing を有効にし、API リクエストを `GET` のままにします。

![PetClinic ThousandEyes HTTP Server tracing settings](../images/te-petclinic-http-settings.png)

4. テストを保存し、数回の実行間隔を待ちます。

{{% notice title="トレーステストの要件" style="warning" %}}
分散トレーシング演習では **HTTP Server** または **API** テストを使用してください。ブラウザ形式の page load や transaction テストはエンドユーザー監視には有用ですが、ThousandEyes と Splunk APM ワークフローに必要なトレースヘッダーを注入する用途には適していません。
{{% /notice %}}

### 任意の PetClinic API テスト

最初の 2 つのテストが動作したら、他の PetClinic サービスもカバーできます。

```text
[Trace] PetClinic Vets API
http://api-gateway.default.svc.cluster.local:82/api/vet/vets

[Trace] PetClinic Owner Visits API
http://api-gateway.default.svc.cluster.local:82/api/visit/owners/1/pets/1/visits
```

PetClinic を `default` 以外の namespace にデプロイした場合は、各 URL の `default` を PetClinic の namespace に置き換えてください。
