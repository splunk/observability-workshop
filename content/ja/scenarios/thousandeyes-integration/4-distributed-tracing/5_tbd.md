---
title: Kubernetes サービステストと相関
linkTitle: 4.5. Kubernetes テスト
weight: 4.5
time: 20 minutes
description: シンセティックモニタリングとトレース相関の両方に役立つ、内部 Kubernetes および外部依存関係のテストを作成します。
draft: true
---

このセクションはレビューが必要です

## AppDynamics テスト推奨機能の再現

AppDynamics には「Test Recommendations」と呼ばれる機能があり、アプリケーションエンドポイントに対するシンセティックテストを自動的に提案します。ThousandEyes を Kubernetes クラスター内にデプロイすることで、Kubernetes サービスディスカバリーと Splunk Observability Cloud の統合ビューを活用して、この機能を再現できます。

ThousandEyes Enterprise Agent はクラスターの**内部**で動作するため、サービス名をホスト名として使用して内部 Kubernetes サービスを直接テストできます。これにより、外部に公開されていないバックエンドサービスを監視する強力な方法が提供されます。

## 仕組み

1. **サービスディスカバリー**: `kubectl get svc` を使用してクラスター内のサービスを列挙します
2. **ホスト名の構築**: Kubernetes DNS 命名規則を使用してテスト URL を構築します: `<service-name>.<namespace>.svc.cluster.local`
3. **テストの作成**: 内部サービスに対して可用性テストとトレース対応のトランザクションテストの両方を作成します
4. **Splunk での相関**: シンセティックテスト結果を APM トレースやインフラストラクチャメトリクスと並べて表示します

## クラスター内テストの利点

- **内部サービスモニタリング**: インターネットに公開されていないバックエンドサービスをテストできます
- **サービスメッシュ対応**: Istio、Linkerd、その他のサービスメッシュの背後にあるサービスを監視できます
- **DNS 解決テスト**: Kubernetes DNS とサービスディスカバリーを検証できます
- **ネットワークポリシーの検証**: ネットワークポリシーが適切な通信を許可していることを確認できます
- **レイテンシーベースライン**: クラスター内部のネットワークパフォーマンスを測定できます
- **本番前テスト**: Ingress/LoadBalancer で公開する前にサービスをテストできます

## ワークショップターゲット: Spring PetClinic

このリポジトリには、ThousandEyes ガイドの既知の Kubernetes ターゲットとして使用できる Spring PetClinic マイクロサービスアプリケーションがすでに含まれています。デプロイメントマニフェストは `workshop/petclinic/deployment.yaml` にあり、ワークショップ VM では `~/workshop/petclinic/deployment.yaml` で利用できます。

このマニフェストは、PetClinic フロントエンド/API ゲートウェイ、バックエンドサービス、MySQL データベース、およびロードジェネレーターをデプロイします。また、以下も作成されます:

- ポート `82` の `ClusterIP` サービスとしての `api-gateway`
- ポート `81` の `LoadBalancer` サービスとしての `api-gateway-external`
- 内部バックエンドサービスとしての `customers-service`、`vets-service`、`visits-service`

{{% notice title="トレーシングのセットアップ" style="info" %}}
Splunk OpenTelemetry Operator をすでにインストールしており、PetClinic をトレース相関に使用する予定の場合は、このマニフェストを適用する前に Distributed Tracing セクションで PetClinic のインストルメンテーションセットアップを完了してください。PetClinic マニフェストには一部のサービスに Java インジェクションアノテーションが含まれており、オペレーター Webhook がアクティブな場合、それらのアノテーションには対応する `Instrumentation` リソースが必要です。
{{% /notice %}}

選択した namespace に PetClinic をデプロイします:

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

以下の例では、PetClinic が `default` namespace にデプロイされていることを前提としています。別の namespace にデプロイする場合は、サービス DNS 名の `default` をご自身の namespace に置き換えてください。

アプリケーションリソースを確認します:

```bash
kubectl get pods -n $PETCLINIC_NAMESPACE
kubectl get svc -n $PETCLINIC_NAMESPACE api-gateway api-gateway-external customers-service vets-service visits-service
```

ThousandEyes エージェントが実行されている namespace からクラスター内部の到達性を検証します:

```bash
kubectl run te-petclinic-curl \
  -n te-demo \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.$PETCLINIC_NAMESPACE.svc.cluster.local:82/api/customer/owners
```

ThousandEyes テストに使用する PetClinic URL:

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
ThousandEyes Enterprise Agent は `te-demo` で実行し、PetClinic は `default` で実行できます。エージェントとターゲットアプリケーションが異なる namespace にある場合は、`api-gateway.default.svc.cluster.local` のような完全な Kubernetes DNS 名を使用してください。
{{% /notice %}}

## PetClinic 用の ThousandEyes テストの設定

少なくとも 2 つの PetClinic テストを作成します: フロントエンド用のシンプルな可用性テストと、APM 相関用のトレース対応 API テストです。両方のテストで同じ Kubernetes Enterprise Agent を使用して、クラスター内部から測定が行われるようにします。

エンドポイントを検証する際に、ターゲット URL のシェル変数を設定します:

```bash
kubectl run te-petclinic-curl \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS "http://api-gateway.default.svc.cluster.local:82/api/customer/owners"
```

### テスト 1: PetClinic フロントエンドの可用性

このテストを使用して、ThousandEyes Enterprise Agent からアプリケーションフロントエンドに到達可能であることを証明します。

1. ThousandEyes で、**Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** を選択します。
3. テストを設定します:
   - **Test Name**: `[PetClinic] Frontend Availability`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/`
   - **Interval**: `2 minutes`
   - **Agents**: このガイドで先にデプロイした Kubernetes Enterprise Agent を選択します
   - **HTTP Response Code**: `200`
   - **Verify Content**: オプション。返されたページコンテンツを検証したい場合は `PetClinic` を使用します
4. テストを保存します。

### テスト 2: 分散トレーシング付き PetClinic Owners API

このテストは、ThousandEyes と Splunk APM のドリルダウンワークフローに使用します。API ゲートウェイをターゲットとし、`customers-service` にルーティングされるため、浅いヘルスチェックよりも有用なトレースが得られます。

1. ThousandEyes で、**Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** または **API** を選択します。
3. テストを設定します:
   - **Test Name**: `[Trace] PetClinic Owners API`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`
   - **Method**: `GET`
   - **Interval**: `2 minutes`
   - **Agents**: 同じ Kubernetes Enterprise Agent を選択します
   - **HTTP Response Code**: `200`
   - **Advanced Settings > Distributed Tracing**: Enabled

**Basic Settings** のハイライトされたフィールドは、PetClinic API ターゲットとクラスター内の Enterprise Agent に一致する必要があります:

![PetClinic ThousandEyes HTTP Server basic settings](../images/te-petclinic-basic-settings.png)

**HTTP Communication and Performance** で、分散トレーシングを有効にし、API リクエストをデフォルトの `2xx` または `3xx` レスポンス検証で `GET` のままにします:

![PetClinic ThousandEyes HTTP Server tracing settings](../images/te-petclinic-http-settings.png)

4. テストを保存し、数回のインターバルで実行させます。

{{% notice title="トレーステストの要件" style="warning" %}}
分散トレーシング演習には **HTTP Server** または **API** テストを使用してください。ブラウザスタイルのページロードおよびトランザクションテストはエンドユーザーモニタリングに役立ちますが、ThousandEyes と Splunk APM のワークフローに必要なトレースヘッダーを注入するための適切なテストタイプではありません。
{{% /notice %}}

### オプションの PetClinic API テスト

最初の 2 つのテストが動作したら、他の PetClinic サービスをカバーする API テストを追加します:

```text
[Trace] PetClinic Vets API
http://api-gateway.default.svc.cluster.local:82/api/vet/vets

[Trace] PetClinic Owner Visits API
http://api-gateway.default.svc.cluster.local:82/api/visit/owners/1/pets/1/visits
```

同じベースライン設定を使用します:

- **Test Type**: HTTP Server or API
- **Method**: `GET`
- **Interval**: `2 minutes`
- **Agent**: Kubernetes Enterprise Agent
- **Expected Response Code**: `200`
- **Distributed Tracing**: Splunk APM 相関が必要な場合は Enabled

PetClinic を `default` namespace 以外にデプロイした場合は、各 URL の `default` をご自身の PetClinic namespace に置き換えてください。
