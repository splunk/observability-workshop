---
title: Kubernetes Service Testing and Correlation
linkTitle: 4.5. Kubernetes Testing
weight: 4.5
time: 20 minutes
description: シンセティックモニタリングとトレース相関の両方に役立つ、Kubernetes 内部および外部依存のテストを作成します。
draft: true
---

THIS ALSO NEEDS TO BE REVIEWED

## AppDynamics の Test Recommendations を再現する

AppDynamics には「Test Recommendations」という機能があり、アプリケーションのエンドポイントに対するシンセティックテストを自動で提案します。Kubernetes クラスター内に ThousandEyes をデプロイすれば、Kubernetes のサービスディスカバリと Splunk Observability Cloud の統合ビューを組み合わせて、同等の機能を再現できます。

ThousandEyes Enterprise Agent は **クラスター内部** で動作するため、Kubernetes 内部サービスをそのサービス名のホスト名で直接テストできます。これにより、外部に公開されていないバックエンドサービスを監視する強力な手段が得られます。

## 仕組み

1. **Service Discovery**: `kubectl get svc` を使ってクラスター内のサービスを列挙します
2. **Hostname Construction**: Kubernetes DNS の命名規則に従ってテスト URL を構築します: `<service-name>.<namespace>.svc.cluster.local`
3. **Test Creation**: 内部サービスに対して、可用性テストとトレース対応のトランザクションテストの両方を作成します
4. **Correlation in Splunk**: シンセティックテストの結果を APM トレースおよびインフラメトリクスと並べて参照します

## クラスター内テストのメリット

- **Internal Service Monitoring**: インターネットに公開されていないバックエンドサービスをテストできます
- **Service Mesh Awareness**: Istio、Linkerd などのサービスメッシュ配下のサービスを監視できます
- **DNS Resolution Testing**: Kubernetes DNS とサービスディスカバリを検証できます
- **Network Policy Validation**: ネットワークポリシーが適切な通信を許可しているか確認できます
- **Latency Baseline**: クラスター内部のネットワーク性能を測定できます
- **Pre-Production Testing**: Ingress や LoadBalancer で公開する前にサービスをテストできます

## ワークショップの対象: Spring PetClinic

このリポジトリには、本 ThousandEyes ガイドの既知の Kubernetes ターゲットとして利用できる Spring PetClinic マイクロサービスアプリケーションが含まれています。デプロイメントマニフェストは `workshop/petclinic/deployment.yaml` にあり、ワークショップ VM では `~/workshop/petclinic/deployment.yaml` で参照できます。

このマニフェストは、PetClinic のフロントエンド/API ゲートウェイ、バックエンドサービス、MySQL データベース、ロードジェネレーターをデプロイします。さらに次のサービスも作成します。

- ポート `82` の `ClusterIP` サービスとしての `api-gateway`
- ポート `81` の `LoadBalancer` サービスとしての `api-gateway-external`
- 内部バックエンドサービスとしての `customers-service`、`vets-service`、`visits-service`

{{% notice title="Tracing Setup" style="info" %}}
Splunk OpenTelemetry Operator を既にインストールしており、PetClinic をトレース相関に使用する予定であれば、このマニフェストを適用する前に Distributed Tracing セクションの PetClinic インストルメンテーション設定を完了してください。PetClinic のマニフェストには一部のサービスに Java インジェクションのアノテーションが含まれており、Operator の Webhook が有効な場合、これらのアノテーションには対応する `Instrumentation` リソースが必要です。
{{% /notice %}}

選択した Namespace に PetClinic をデプロイします。

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

以下の例では、PetClinic が `default` Namespace にデプロイされていることを前提としています。別の Namespace にデプロイする場合は、サービスの DNS 名にある `default` を該当の Namespace に置き換えてください。

アプリケーションのリソースを確認します。

```bash
kubectl get pods -n $PETCLINIC_NAMESPACE
kubectl get svc -n $PETCLINIC_NAMESPACE api-gateway api-gateway-external customers-service vets-service visits-service
```

ThousandEyes Agent が動作する Namespace と同じ Namespace から、クラスター内部の到達性を検証します。

```bash
kubectl run te-petclinic-curl \
  -n te-demo \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.$PETCLINIC_NAMESPACE.svc.cluster.local:82/api/customer/owners
```

ThousandEyes のテストには、次の PetClinic URL を使用します。

```text
Availability test:
http://api-gateway.default.svc.cluster.local:82/

Trace-enabled API test:
http://api-gateway.default.svc.cluster.local:82/api/customer/owners

Additional API test targets:
http://api-gateway.default.svc.cluster.local:82/api/vet/vets
http://api-gateway.default.svc.cluster.local:82/api/visit/owners/1/pets/1/visits
```

{{% notice title="Namespace Reminder" style="info" %}}
ThousandEyes Enterprise Agent は `te-demo` で動作させ、PetClinic は `default` で動作させることもできます。Agent と対象アプリケーションが異なる Namespace に存在する場合は、`api-gateway.default.svc.cluster.local` のように Kubernetes の完全な DNS 名を使用してください。
{{% /notice %}}

## PetClinic 向けの ThousandEyes テストを構成する

PetClinic 用に少なくとも 2 つのテストを作成します。1 つはフロントエンドに対する単純な可用性テスト、もう 1 つは APM 相関のためのトレース対応 API テストです。両方のテストで同じ Kubernetes Enterprise Agent を使用し、測定がクラスター内部から行われるようにします。

エンドポイントを検証する間、対象 URL をシェル変数に設定しておきます。

```bash
kubectl run te-petclinic-curl \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS "http://api-gateway.default.svc.cluster.local:82/api/customer/owners"
```

### Test 1: PetClinic フロントエンドの可用性

このテストは、ThousandEyes Enterprise Agent からアプリケーションのフロントエンドに到達できることを確認するために使用します。

1. ThousandEyes で **Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** を選択します。
3. テストを構成します。
   - **Test Name**: `[PetClinic] Frontend Availability`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/`
   - **Interval**: `2 minutes`
   - **Agents**: 本ガイドの前のステップでデプロイした Kubernetes Enterprise Agent を選択します
   - **HTTP Response Code**: `200`
   - **Verify Content**: 任意。返されたページ内容を検証したい場合は `PetClinic` を使用します
4. テストを保存します。

### Test 2: 分散トレーシング対応の PetClinic Owners API

このテストは、ThousandEyes と Splunk APM のドリルダウンワークフローで使用します。API ゲートウェイを対象とし、`customers-service` にルーティングするため、表面的なヘルスチェックよりも有用なトレースが得られます。

1. ThousandEyes で **Cloud & Enterprise Agents > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** または **API** を選択します。
3. テストを構成します。
   - **Test Name**: `[Trace] PetClinic Owners API`
   - **URL**: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`
   - **Method**: `GET`
   - **Interval**: `2 minutes`
   - **Agents**: 同じ Kubernetes Enterprise Agent を選択します
   - **HTTP Response Code**: `200`
   - **Advanced Settings > Distributed Tracing**: 有効化します

**Basic Settings** のハイライトされたフィールドは、PetClinic API のターゲットおよびクラスター内の Enterprise Agent と一致している必要があります。

![PetClinic ThousandEyes HTTP Server basic settings](../images/te-petclinic-basic-settings.png)

**HTTP Communication and Performance** で分散トレーシングを有効化し、API リクエストは `GET` のままにして、デフォルトの `2xx` または `3xx` のレスポンス検証を維持します。

![PetClinic ThousandEyes HTTP Server tracing settings](../images/te-petclinic-http-settings.png)

1. テストを保存し、数インターバルの間実行させます。

{{% notice title="Trace Test Requirement" style="warning" %}}
分散トレーシングの演習では **HTTP Server** または **API** テストを使用してください。ブラウザ形式のページロードテストやトランザクションテストはエンドユーザーモニタリングには有用ですが、ThousandEyes と Splunk APM のワークフローに必要なトレースヘッダーを注入する用途には適したテスト種別ではありません。
{{% /notice %}}

### オプション: PetClinic API テスト

最初の 2 つのテストが動作したら、他の PetClinic サービスをカバーする API テストを追加します。

```text
[Trace] PetClinic Vets API
http://api-gateway.default.svc.cluster.local:82/api/vet/vets

[Trace] PetClinic Owner Visits API
http://api-gateway.default.svc.cluster.local:82/api/visit/owners/1/pets/1/visits
```

同じベースライン設定を使用します。

- **Test Type**: HTTP Server または API
- **Method**: `GET`
- **Interval**: `2 minutes`
- **Agent**: Kubernetes Enterprise Agent
- **Expected Response Code**: `200`
- **Distributed Tracing**: Splunk APM 相関を行いたい場合は有効化します

PetClinic を `default` 以外の Namespace にデプロイした場合は、各 URL の `default` を実際の PetClinic の Namespace に置き換えてください。
