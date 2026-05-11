---
title: 分散トレーシングと双方向ドリルダウン
linkTitle: 4. Distributed Tracing
weight: 4
time: 25 minutes
description: ThousandEyes と Splunk APM 間のトレース相関を有効にし、調査中にチームが両製品間をシームレスに移動できるようにします。
---

このセクションでは、ThousandEyes と Splunk の統合を本格的な調査ワークフローに変えます。前のセクションでは、ThousandEyes がシンセティックメトリクスを Splunk Observability Cloud にストリーミングしました。このセクションでは、サポートされている **ThousandEyes <-> Splunk APM 分散トレーシング統合** を有効にし、ネットワーク、プラットフォーム、アプリケーションの各チームが同じリクエストを見ながら両ツール間を行き来できるようにします。

{{% notice title="Why This Matters" style="primary" icon="lightbulb" %}}
これは、2つの環境間の **双方向アクセス** を実現するための重要な要素です。ThousandEyes から Splunk APM の関連トレースを開くことができ、Splunk APM から元の ThousandEyes テストに戻ることもできます。
{{% /notice %}}

## 学習内容

このセクションを完了すると、以下のことができるようになります

- 付属の Spring PetClinic Kubernetes アプリケーションをトレースターゲットとしてデプロイおよび使用する
- 内部サービスを計装して Splunk APM にトレースを送信する
- ThousandEyes の **HTTP Server** または **API** テストで分散トレーシングを有効にする
- ThousandEyes の **Generic Connector** を Splunk APM 用に設定する
- ThousandEyes の **Service Map** を開き、対応する Splunk トレースに直接ジャンプする
- Splunk APM 内の ThousandEyes メタデータを使用して元の ThousandEyes テストに戻る

## サポートされるワークフロー

この学習シナリオは、ThousandEyes と Splunk がドキュメント化しているサポート対象のワークフローに従います

- ThousandEyes は、分散トレーシングが有効になっている場合、**HTTP Server** および **API** テストに `b3`、`traceparent`、`tracestate` ヘッダーを自動的にインジェクトします。
- 監視対象のエンドポイントは、ヘッダーを受け入れ、OpenTelemetry で計装され、トレースコンテキストを伝播し、オブザーバビリティバックエンドにトレースを送信する必要があります。
- Splunk APM の場合、ThousandEyes は `https://api.<REALM>.signalfx.com` を指す **Generic Connector** を使用し、**API スコープ** の Splunk トークンで認証します。
- Splunk APM は、一致するトレースに `thousandeyes.test.id` や `thousandeyes.permalink` などの ThousandEyes 属性を付与し、ThousandEyes への逆方向ジャンプを可能にします。

## ヘッダーの意味

この部分は読み飛ばしがちですが、そうすべきではありません。トレース相関は、サービスが ThousandEyes がインジェクトするヘッダーを理解し、トレースを正しく継続する場合にのみ機能します。

- `traceparent` と `tracestate` は W3C Trace Context ヘッダーです。
- `b3` は Zipkin B3 シングルヘッダー形式です。
- ThousandEyes が両方をインジェクトするのは、実際の環境にはプロキシ、メッシュ、ゲートウェイ、アプリケーションランタイムが混在しており、すべてが同じ伝播形式を優先するわけではないためです。

OpenTelemetry の用語では、重要な設定はプロパゲーターリストです

```text
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

これにより2つのことが実現されます

1. サービスが受信した ThousandEyes リクエストから **B3** または **W3C** コンテキストのいずれかを抽出できるようになります。
2. `tracecontext` を有効にしたままにすることで、W3C `tracestate` が保持されます。

{{% notice title="Important Detail" style="warning" %}}
`tracestate` を個別の OpenTelemetry プロパゲーターとして追加する必要は **ありません**。`tracecontext` プロパゲーターが `traceparent` と `tracestate` の両方を処理します。
{{% /notice %}}

## 「正しい構成」とは

コレクターはこのセットアップの一部に過ぎません。Kubernetes における正しい ThousandEyes トレーシングデプロイメントには **3つのレイヤー** があります

1. **Deployment アノテーション** - OpenTelemetry Operator がランタイム固有の計装をインジェクトするため。
2. **Instrumentation リソース** - インジェクトされた SDK がトレースの送信先と使用するプロパゲーターを把握するため。
3. **Collector トレースパイプライン** - OTLP トレースが実際に受信され、Splunk APM にエクスポートされるため。

最もよくある間違いは、コレクターだけに注目することです。コレクターは生の `b3`、`traceparent`、`tracestate` リクエストヘッダーを直接見ることはありません。アプリケーションまたは自動計装ライブラリがまずそれらのヘッダーを抽出し、スパンコンテキストを継続してから、OTLP 経由でコレクターにスパンを送信する必要があります。

## 現在のクラスターの実際の構成

以下の例は、このワークショップを実行しているライブクラスターからの抜粋です。現在 Kubernetes で実際に動作しているパターンを示しています。

### 1. Deployment アノテーション

ライブクラスターでは、`teastore` アプリケーションが `teastore/default` Instrumentation リソースを指しています

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: teastore-webui-v1
  namespace: teastore
spec:
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/container-names: teastore-webui-v1
        instrumentation.opentelemetry.io/inject-java: teastore/default
```

ThousandEyes のリクエストがトレースに変換されない場合、最初に確認すべき箇所です。

### 2. Instrumentation リソース

これは `teastore` のライブ `Instrumentation` オブジェクトで、ThousandEyes に関連するフィールドのみを抜粋しています

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: default
  namespace: teastore
spec:
  exporter:
    endpoint: http://splunk-otel-collector-agent.otel-splunk.svc:4317
  propagators:
    - baggage
    - b3
    - tracecontext
  sampler:
    type: parentbased_always_on
  env:
    - name: OTEL_RESOURCE_ATTRIBUTES
      value: deployment.environment=teastore
```

ThousandEyes シナリオにおける重要なポイントは以下のとおりです

- `endpoint` はクラスターローカルの OTel エージェントサービスにスパンを送信します。
- `b3` は ThousandEyes の B3 ヘッダーの抽出を可能にします。
- `tracecontext` は `traceparent` と `tracestate` を保持します。
- `parentbased_always_on` は ThousandEyes がリクエストを開始した後もトレースが継続されることを保証します。

### 3. インジェクトされた Pod が実際に受け取る内容

実行中の `teastore-webui-v1` Pod では、Operator が以下の環境変数をインジェクトしました

```yaml
- name: JAVA_TOOL_OPTIONS
  value: " -javaagent:/otel-auto-instrumentation-java-teastore-webui-v1/javaagent.jar"
- name: OTEL_SERVICE_NAME
  value: teastore-webui-v1
- name: OTEL_EXPORTER_OTLP_ENDPOINT
  value: http://splunk-otel-collector-agent.otel-splunk.svc:4317
- name: OTEL_PROPAGATORS
  value: baggage,b3,tracecontext
- name: OTEL_TRACES_SAMPLER
  value: parentbased_always_on
```

これは、プロパゲーターが抽象的な設定オブジェクトで宣言されているだけでなく、実際にワークロードに適用されていることを証明する有用な検証チェックポイントです。

### 4. Agent Collector トレースパイプライン

`otel-splunk` のライブ Agent Collector は OTLP、Jaeger、Zipkin トラフィックを受信し、上流にトレースを転送しています。以下は実行中の ConfigMap からの抜粋です

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_http:
        endpoint: 0.0.0.0:14268
  zipkin:
    endpoint: 0.0.0.0:9411

service:
  pipelines:
    traces:
      receivers: [otlp, jaeger, zipkin]
      processors:
        [memory_limiter, k8sattributes, batch, resourcedetection, resource, resource/add_environment]
      exporters: [otlp, signalfx]
```

ThousandEyes にとって重要なのは、コレクターに特別な B3 オプションを設定することではありません。重要なのは、コレクターが `4317` と `4318` で OTLP を公開しており、サービスがそこにスパンをエクスポートしていることです。

### 5. Gateway Collector から Splunk APM へのエクスポート

ライブの Gateway Collector はトレースを Splunk Observability Cloud に転送します。以下は実行中の Gateway ConfigMap の関連部分です

```yaml
exporters:
  otlphttp:
    auth:
      authenticator: headers_setter
    traces_endpoint: https://ingest.us1.signalfx.com/v2/trace/otlp

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        include_metadata: true
      http:
        endpoint: 0.0.0.0:4318
        include_metadata: true

service:
  pipelines:
    traces:
      receivers: [otlp, jaeger, zipkin]
      processors:
        [memory_limiter, k8sattributes, batch, resource/add_cluster_name, resource/add_environment]
      exporters: [otlphttp, signalfx]
```

これは、スパンを Splunk APM に到達させるための部分です。このパイプラインが壊れている場合、ThousandEyes はリクエストにヘッダーをインジェクトできますが、相関するトレースが Splunk に表示されることはありません。

{{% notice title="Current Cluster Takeaway" style="info" %}}
ライブクラスターでは、`teastore/default` Instrumentation リソースが ThousandEyes 用のパターンとして適しています。`b3` と `tracecontext` を明示的に含んでいるためです。これがこのシナリオで再現したい構成です。
{{% /notice %}}

{{% notice title="Important" style="warning" %}}
このセクションではブラウザのページ URL を使用 **しないでください**。ThousandEyes のドキュメントによると、ブラウザはこのワークフローに必要なカスタムトレースヘッダーを受け入れません。代わりに、**HTTP Server** または **API** テストの背後にある計装済みバックエンドエンドポイントを使用してください。
{{% /notice %}}

## ステップ 1: ワークロードが Splunk APM にトレースを送信していることを確認する

アプリケーションがすでに計装されており、Splunk APM でトレースが表示されている場合は、ステップ 2 に進んでください。そうでない場合、Kubernetes で最も速い学習パスは、ゼロコード計装用の Operator を有効にした Splunk OpenTelemetry Collector を使用することです。

### Operator 付き Splunk OpenTelemetry Collector のインストール

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update

helm install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --namespace otel-splunk \
  --create-namespace \
  --set splunkObservability.realm=$REALM \
  --set splunkObservability.accessToken=$ACCESS_TOKEN \
  --set clusterName=$CLUSTER_NAME \
  --set environment="thousandeyes-$INSTANCE" \
  --set operator.enabled=true \
  --set operatorcrds.install=true \
  --set agent.service.enabled=true
```

### ワークショップのトレースターゲットとして Spring PetClinic をデプロイする

このプロジェクトには、`workshop/petclinic/deployment.yaml` に Spring PetClinic マイクロサービスアプリケーションの Kubernetes デプロイメントが含まれています。ワークショップ VM では、`~/workshop/petclinic/deployment.yaml` のコピーを使用してください。

PetClinic マニフェストは、RUM およびロードジェネレーション設定用の `workshop-secret` を必要とします。また、いくつかのサービスに Java 自動計装アノテーションが含まれているため、アプリケーションマニフェストを適用する前に PetClinic の namespace と Instrumentation リソースを作成してください。

```bash
PETCLINIC_NAMESPACE=default
OTEL_COLLECTOR_NAMESPACE=otel-splunk
OTEL_INSTRUMENTATION=splunk-otel-collector

kubectl create namespace $PETCLINIC_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
```

PetClinic namespace に `Instrumentation` リソースを作成または更新します。インジェクトされた Java エージェントはこのリソースを使用して、Splunk OTel Collector にスパンを送信し、ThousandEyes が送信するトレースヘッダーを受け入れます

```bash
cat <<EOF | kubectl apply -f -
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: $OTEL_INSTRUMENTATION
  namespace: $PETCLINIC_NAMESPACE
spec:
  exporter:
    endpoint: http://splunk-otel-collector-agent.$OTEL_COLLECTOR_NAMESPACE.svc:4317
  propagators:
    - baggage
    - b3
    - tracecontext
  sampler:
    type: parentbased_always_on
  env:
    - name: OTEL_RESOURCE_ATTRIBUTES
      value: deployment.environment=${INSTANCE:-thousandeyes}-petclinic
EOF
```

`workshop-secret` を作成または更新してから、PetClinic をデプロイします

```bash
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

すべての PetClinic Java デプロイメントにパッチを適用して、PetClinic namespace の Instrumentation リソースを使用するようにします

```bash
kubectl get deployments \
  -n $PETCLINIC_NAMESPACE \
  -l app.kubernetes.io/part-of=spring-petclinic \
  -o name | \
  xargs -I % kubectl patch -n $PETCLINIC_NAMESPACE % \
    -p "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"$PETCLINIC_NAMESPACE/$OTEL_INSTRUMENTATION\"}}}}}"
```

主要なサービスのロールアウトが完了するのを待ちます

```bash
kubectl rollout status -n $PETCLINIC_NAMESPACE deployment/api-gateway
kubectl rollout status -n $PETCLINIC_NAMESPACE deployment/customers-service
kubectl rollout status -n $PETCLINIC_NAMESPACE deployment/vets-service
kubectl rollout status -n $PETCLINIC_NAMESPACE deployment/visits-service
```

ThousandEyes Enterprise Agent が実行されている namespace からクラスター内 API パスを検証します

```bash
kubectl run te-petclinic-curl \
  -n te-demo \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.$PETCLINIC_NAMESPACE.svc.cluster.local:82/api/customer/owners
```

トレース対応の ThousandEyes **HTTP Server** または **API** テストには、この URL を使用します

```text
http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

`PETCLINIC_NAMESPACE` を変更した場合は、ThousandEyes テスト URL の `default` をその namespace に置き換えてください。

### 自動計装用の Deployment アノテーション

Java ワークロードの場合、一般的な例は以下のようになります

```bash
kubectl patch deployment api-gateway -n production -p '{"spec":{"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"otel-splunk/splunk-otel-collector"}}}}}'
```

他のランタイムの場合は、言語に対応するアノテーションを使用します

- `instrumentation.opentelemetry.io/inject-nodejs`
- `instrumentation.opentelemetry.io/inject-python`
- `instrumentation.opentelemetry.io/inject-dotnet`

コレクターがアプリケーションと同じ namespace にインストールされている場合、Splunk の公式ドキュメントではアノテーション値として `"true"` を使用することもサポートされています。

このリポジトリの PetClinic デプロイメントを使用している場合は、この単一デプロイメントの例ではなく、上記の PetClinic パッチコマンドを使用してください。

このワークショップ環境の **ライブクラスターパターン** に従う場合、アノテーション値は namespace 修飾されており、`teastore/default` Instrumentation オブジェクトを指しています

```bash
kubectl patch deployment teastore-webui-v1 -n teastore -p '{"spec":{"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/container-names":"teastore-webui-v1","instrumentation.opentelemetry.io/inject-java":"teastore/default"}}}}}'
```

### トレースの存在を確認する

1. デプロイメントのロールアウトが完了するのを待ちます

   ```bash
   kubectl rollout status deployment/api-gateway -n default
   ```

2. PetClinic API Gateway に対していくつかのリクエストを生成します

   ```text
   http://api-gateway.default.svc.cluster.local:82/api/customer/owners
   ```

   このリクエストは PetClinic API Gateway を通じて入り、`customers-service` にルーティングされ、PetClinic データベースにクエリを実行します。単純なヘルスチェックよりも有用なトレースが生成されます。

3. 続行する前に、**Splunk APM** にトレースが到着していることを確認してください。

{{% notice title="Learning Tip" style="info" %}}
トレーシング演習には、純粋な `/health` エンドポイントではなく、ビジネストランザクションを使用してください。複数サービスにまたがるリクエストは、ThousandEyes でより充実した Service Map を、Splunk APM でより有用なトレースを提供します。
{{% /notice %}}

## ステップ 2: ThousandEyes テストで分散トレーシングを有効にする

ステップ 1 の計装済みバックエンドエンドポイントをターゲットにした **HTTP Server** または **API** テストを作成または編集します。

1. ThousandEyes で **HTTP Server** または **API** テストを作成します。
2. **Advanced Settings** を開きます。
3. **Distributed Tracing** を有効にします。
4. テストを保存し、すでに Splunk APM にトレースを送信しているのと同じエンドポイントに対して実行します。

![ThousandEyes での Distributed Tracing の有効化](../images/distributed-tracing-enable.png)

テストが実行されると、ThousandEyes はトレースヘッダーをインジェクトし、そのリクエストのトレースコンテキストをキャプチャします。

## ステップ 3: ThousandEyes で Splunk APM Connector を作成する

前のセクションのメトリクスストリーミング統合は **Ingest** トークンを使用しました。このステップは異なります。ThousandEyes は Splunk APM にクエリを実行してトレースリンクを構築する必要があるため、代わりに Splunk **API** トークンを使用します。

1. Splunk Observability Cloud で、**API** スコープのアクセストークンを作成します。
2. ThousandEyes で、**Manage > Integrations > Integrations 2.0** に移動します。
3. 以下の設定で **Generic Connector** を作成します
   - **Target URL**: `https://api.<REALM>.signalfx.com`
   - **Header**: `X-SF-Token: <your-api-scope-token>`
4. 新しい **Operation** を作成し、**Splunk Observability APM** を選択します。
5. Operation を有効にして統合を保存します。

![ThousandEyes での Splunk APM Generic Connector](../images/splunk-apm-generic-connector.png)

![ThousandEyes での Splunk APM Operation](../images/splunk-apm-operation.png)

## ステップ 4: 双方向調査ループを検証する

テストが実行中でコネクターが有効になったら、両方向のワークフローを検証します。

### ThousandEyes から開始する

1. ThousandEyes でテストを開きます。
2. **Service Map** タブに移動します。
3. トレースパス、サービスレイテンシー、ダウンストリームエラーが表示されることを確認します。
4. ThousandEyes から **Splunk APM** へのリンクを使用して、完全なトレースを検査します。

![Splunk APM 相関が表示された ThousandEyes Service Map](../images/thousandeyes-service-map.png)

### Splunk APM で続行する

Splunk APM 内で、トレースに以下のような ThousandEyes メタデータが含まれていることを確認します

- `thousandeyes.account.id`
- `thousandeyes.test.id`
- `thousandeyes.permalink`
- `thousandeyes.source.agent.id`

`thousandeyes.permalink` フィールドまたはトレースウォーターフォールビューの **Go to ThousandEyes test** ボタンを使用して、元の ThousandEyes テストに戻ります。

![ThousandEyes にリンクされた Splunk APM トレース](../images/splunk-apm-trace.png)

## 推奨される学習シナリオ

ワークショップでは以下のフローを使用してください

1. 複数のサービスを呼び出す内部 API ルートに対して ThousandEyes テストを作成します。
2. まず ThousandEyes で問題を表面化させ、クラスがネットワークとシンセティックモニタリングの観点から開始できるようにします。
3. ThousandEyes で **Service Map** を開き、レイテンシーやエラーの発生箇所を特定します。
4. **Splunk APM** にジャンプしてスパンレベルの分析を行います。
5. **ThousandEyes** に戻り、テスト、エージェント、ネットワークパスを再度検査します。

これは、異なるチームが実際にどのように作業するかを反映しているため、優れた学習ループとなります

- ネットワークおよびエッジチームは多くの場合 ThousandEyes から開始します。
- SRE およびプラットフォームチームは多くの場合 Splunk のダッシュボードやアラートから開始します。
- アプリケーションチームは通常 Splunk APM のトレースを求めます。

この統合により、全員がコンテキストを失うことなく切り替えることができます。

## よくある落とし穴

- テストが Splunk ダッシュボードに表示されているにもかかわらず、トレース相関がない場合があります。これは通常、**メトリクス** ストリームのみが設定されており、**Splunk APM Generic Connector** が設定されていないことを意味します。
- 監視対象のエンドポイントがトレースヘッダーをダウンストリームに伝播しない場合、Splunk APM にトレースが存在していても ThousandEyes に表示されないことがあります。
- `/health` のような浅いエンドポイントは、構成が正しくても限られたトレース価値しか生成しないことが多いです。

## リファレンス

- [ThousandEyes Distributed Tracing](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing)
- [ThousandEyes Distributed Tracing with Splunk Observability APM](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm)
- [Splunk APM: View traces with Cisco ThousandEyes integration](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace)
- [Splunk OTel Collector zero-code instrumentation for Kubernetes language runtimes](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/automatic-discovery-of-apps-and-services/kubernetes/language-runtimes)
