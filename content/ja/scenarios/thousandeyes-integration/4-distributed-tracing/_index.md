---
title: 分散トレーシングと双方向ドリルダウン
linkTitle: 4. Distributed Tracing
weight: 4
time: 25 minutes
description: ThousandEyes と Splunk APM の間でサポートされているトレース相関を有効にし、調査時にチームが2つの製品間を行き来できるようにします。
---

このセクションでは、ThousandEyes と Splunk の統合を真の調査ワークフローに変えていきます。前のセクションでは、ThousandEyes が合成メトリクスを Splunk Observability Cloud にストリームしました。このセクションでは、サポートされている **ThousandEyes <-> Splunk APM の分散トレーシング統合**を有効にして、ネットワーク、プラットフォーム、アプリケーションの各チームが同じリクエストを見ながら両方のツール間をピボットできるようにします。

{{% notice title="なぜ重要か" style="primary" icon="lightbulb" %}}
これが2つの環境間で**双方向アクセス**を可能にする要素です。ThousandEyes は関連するトレースを Splunk APM で開けるようになり、Splunk APM は元の ThousandEyes テストに戻れるようになります。
{{% /notice %}}

## 学べる内容

このセクションを終えると、次のことができるようになります。

- 内部サービスを計装して、Splunk APM にトレースを送信できる
- ThousandEyes の **HTTP Server** または **API** テストで分散トレーシングを有効にできる
- ThousandEyes の **Generic Connector** を Splunk APM 用に設定できる
- ThousandEyes の **Service Map** を開き、対応する Splunk のトレースに直接ジャンプできる
- Splunk APM の ThousandEyes メタデータを使用して、元の ThousandEyes テストに戻れる

## サポートされているワークフロー

この学習シナリオは、ThousandEyes と Splunk によってドキュメント化されているサポート対象のワークフローに従います。

- 分散トレーシングが有効な場合、ThousandEyes は **HTTP Server** および **API** テストに `b3`、`traceparent`、`tracestate` ヘッダーを自動的に挿入します。
- 監視対象のエンドポイントは、ヘッダーを受け入れ、OpenTelemetry で計装され、トレースコンテキストを伝播し、オブザーバビリティバックエンドにトレースを送信する必要があります。
- Splunk APM の場合、ThousandEyes は `https://api.<REALM>.signalfx.com` を指す **Generic Connector** を使用し、**API スコープ**の Splunk トークンで認証します。
- Splunk APM は、`thousandeyes.test.id` や `thousandeyes.permalink` などの ThousandEyes 属性で一致するトレースをエンリッチし、ThousandEyes に戻る逆方向のジャンプを可能にします。

## これらのヘッダーが実際に意味するもの

この部分は読み流しがちですが、重要です。トレースの相関は、サービスが ThousandEyes が挿入するヘッダーを理解し、トレースを正しく継続する場合にのみ機能します。

- `traceparent` と `tracestate` は W3C Trace Context ヘッダーです。
- `b3` は Zipkin B3 シングルヘッダー形式です。
- ThousandEyes が両方を挿入するのは、実際の環境にはプロキシ、メッシュ、ゲートウェイ、アプリランタイムが混在しており、それらすべてが同じ伝播形式を好むわけではないためです。

OpenTelemetry の用語では、重要な設定は propagator のリストです。

```text
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

これにより、次の2つが実現されます。

1. サービスが、受信した ThousandEyes リクエストから **B3** または **W3C** のコンテキストを抽出できるようになります。
2. `tracecontext` を有効にしておくことで、W3C `tracestate` が保持されます。

{{% notice title="重要な詳細" style="warning" %}}
`tracestate` を別の OpenTelemetry propagator として追加する必要は**ありません**。`tracecontext` propagator が `traceparent` と `tracestate` の両方を処理します。
{{% /notice %}}

## 「適切に行われた」状態とは

Collector はこのセットアップの一部に過ぎません。Kubernetes における正しい ThousandEyes トレーシングのデプロイには、**3つのレイヤー**があります。

1. **デプロイメントのアノテーション** OpenTelemetry Operator がランタイム固有のインストルメンテーションを注入できるようにします。
2. **Instrumentation リソース** 注入された SDK が、トレースの送信先と使用する propagator を認識できるようにします。
3. **Collector のトレースパイプライン** OTLP トレースが実際に受信され、Splunk APM にエクスポートされるようにします。

最も多い間違いは、collector のみに焦点を当ててしまうことです。Collector は、生の `b3`、`traceparent`、`tracestate` リクエストヘッダーを直接見ることはありません。アプリケーションまたは自動計装ライブラリが最初にそれらのヘッダーを抽出し、span コンテキストを継続し、その後 OTLP 経由で collector に span を送信する必要があります。

## 現在のクラスターからの実環境設定

以下の例は、このワークショップを現在実行しているライブクラスターから抜粋したものです。Kubernetes で実際に動作しているパターンを示しています。

### 1. デプロイメントのアノテーション

ライブクラスターでは、`teastore` アプリケーションが `teastore/default` Instrumentation リソースを指しています。

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

ThousandEyes のリクエストがトレースに変換されない場合、まずここを確認します。

### 2. Instrumentation リソース

これは `teastore` のライブの `Instrumentation` オブジェクトで、ThousandEyes に関係するフィールドのみに絞り込んだものです。

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

これが ThousandEyes シナリオにおいて重要な部分です。

- `endpoint` は、クラスター内ローカルの OTel エージェントサービスに span を送信します。
- `b3` により、ThousandEyes の B3 ヘッダーを抽出できます。
- `tracecontext` により、`traceparent` と `tracestate` が保持されます。
- `parentbased_always_on` により、ThousandEyes がリクエストを開始した時点でトレースが継続されます。

### 3. 注入されたPodが実際に取得するもの

実行中の `teastore-webui-v1` Pod では、Operator が次の環境変数を注入しています。

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

これは、抽象的な設定オブジェクトで宣言されているだけでなく、propagator が実際にワークロードに適用されていることを証明する有用な検証ポイントです。

### 4. エージェント Collector のトレースパイプライン

`otel-splunk` のライブのエージェント collector は、OTLP、Jaeger、Zipkin のトラフィックを受信し、トレースを上流に転送しています。これは実行中の ConfigMap からの抜粋です。

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

ThousandEyes にとって重要なのは、collector の特殊な B3 オプションではありません。重要なのは、collector が `4317` と `4318` で OTLP を公開しており、サービスがそこに span をエクスポートしているという点です。

### 5. ゲートウェイ Collector の Splunk APM へのエクスポート

その後、ライブのゲートウェイ collector がトレースを Splunk Observability Cloud に転送します。これは、実行中のゲートウェイ ConfigMap の関連部分です。

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

これは、span を Splunk APM に届ける部分です。このパイプラインが壊れていると、ThousandEyes はリクエストにヘッダーを挿入することはできても、相関したトレースは Splunk に表示されません。

{{% notice title="現在のクラスターからの教訓" style="info" %}}
ライブクラスターでは、`teastore/default` Instrumentation リソースが、`b3` と `tracecontext` を明示的に組み合わせているため、ThousandEyes に従うべきパターンとなっています。これは、このシナリオで複製したい設定です。
{{% /notice %}}

{{% notice title="重要" style="warning" %}}
このセクションでは、ブラウザのページ URL は使用**しないでください**。ThousandEyes は、ブラウザがこのワークフローに必要なカスタムトレースヘッダーを受け入れないことをドキュメント化しています。代わりに、**HTTP Server** または **API** テストの背後にある計装済みのバックエンドエンドポイントを使用してください。
{{% /notice %}}

## ステップ 1: ワークロードが Splunk APM にトレースを送信していることを確認する

アプリケーションが既に計装され、Splunk APM でトレースが表示されている場合は、ステップ 2 にスキップできます。そうでない場合、Kubernetes における最速の学習パスは、Operator を有効にした Splunk OpenTelemetry Collector を使用してゼロコード計装を行うことです。

### Operator を有効にした Splunk OpenTelemetry Collector のインストール

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
  --set operatorcrds.install=true
```

### 自動計装のためのデプロイメントのアノテーション

Java ワークロードの一般的な例は次のとおりです。

```bash
kubectl patch deployment api-gateway -n production -p '{"spec":{"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"otel-splunk/splunk-otel-collector"}}}}}'
```

他のランタイムの場合は、言語に対応するアノテーションを使用します。

- `instrumentation.opentelemetry.io/inject-nodejs`
- `instrumentation.opentelemetry.io/inject-python`
- `instrumentation.opentelemetry.io/inject-dotnet`

Collector がアプリケーションと同じ namespace にインストールされている場合は、Splunk の公式ドキュメントでも `"true"` をアノテーション値として使用することがサポートされています。

このワークショップ環境の**ライブクラスターのパターン**に従いたい場合、アノテーション値は namespace 修飾され、`teastore/default` Instrumentation オブジェクトを指します。

```bash
kubectl patch deployment teastore-webui-v1 -n teastore -p '{"spec":{"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/container-names":"teastore-webui-v1","instrumentation.opentelemetry.io/inject-java":"teastore/default"}}}}}'
```

### トレースが存在することを検証する

1. デプロイメントのロールアウトが完了するのを待ちます。

   ```bash
   kubectl rollout status deployment/api-gateway -n production
   ```

2. 複数のサービスにまたがるバックエンドエンドポイントに対して、いくつかのリクエストを生成します。たとえば次のように。

   ```text
   http://api-gateway.production.svc.cluster.local:8080/api/v1/orders
   ```

   現在のワークショップクラスターでは、`http://teastore-webui.teastore.svc.cluster.local:8080/` のようなサービスが適切なターゲットです。これは複数の下流アプリケーションサービスに繋がっており、シンプルなヘルスチェックよりも有用なエンドツーエンドのトレースを生成するためです。

3. 続行する前に、トレースが **Splunk APM** に届いていることを確認します。

{{% notice title="学習のヒント" style="info" %}}
トレーシング演習では、純粋な `/health` エンドポイントではなく、ビジネストランザクションを使用してください。マルチサービスのリクエストの方が、ThousandEyes でははるかに優れた Service Map が得られ、Splunk APM ではより有用なトレースが得られます。
{{% /notice %}}

## ステップ 2: ThousandEyes テストで分散トレーシングを有効にする

ステップ 1 の計装済みバックエンドエンドポイントを対象とする **HTTP Server** または **API** テストを作成または編集します。

1. ThousandEyes で **HTTP Server** または **API** テストを作成します。
2. **Advanced Settings** を開きます。
3. **Distributed Tracing** を有効にします。
4. テストを保存し、すでに Splunk APM にトレースを送信している同じエンドポイントに対して実行します。

![Enable Distributed Tracing in ThousandEyes](../images/distributed-tracing-enable.png)

テスト実行後、ThousandEyes はトレースヘッダーを挿入し、そのリクエストのトレースコンテキストをキャプチャします。

## ステップ 3: ThousandEyes で Splunk APM Connector を作成する

前のセクションのメトリクスストリーミング統合では、**Ingest** トークンを使用しました。このステップは異なります。ThousandEyes は Splunk APM をクエリしてトレースリンクを構築する必要があるため、Splunk の **API** トークンを使用します。

1. Splunk Observability Cloud で、**API** スコープを持つアクセストークンを作成します。
2. ThousandEyes で **Manage > Integrations > Integrations 2.0** に移動します。
3. **Generic Connector** を作成し、次のように設定します。
   - **Target URL** `https://api.<REALM>.signalfx.com`
   - **Header** `X-SF-Token: <your-api-scope-token>`
4. 新しい **Operation** を作成し、**Splunk Observability APM** を選択します。
5. オペレーションを有効にし、統合を保存します。

![Splunk APM Generic Connector in ThousandEyes](../images/splunk-apm-generic-connector.png)

![Splunk APM Operation in ThousandEyes](../images/splunk-apm-operation.png)

## ステップ 4: 双方向の調査ループを検証する

テストが実行され、コネクタが有効になったら、両方向のワークフローを検証します。

### ThousandEyes から開始する

1. ThousandEyes でテストを開きます。
2. **Service Map** タブに移動します。
3. トレースパス、サービスのレイテンシー、下流のエラーを確認できることを確認します。
4. ThousandEyes のリンクから **Splunk APM** に入り、完全なトレースを調査します。

![ThousandEyes Service Map with Splunk APM correlation](../images/thousandeyes-service-map.png)

### Splunk APM で続行する

Splunk APM 内で、トレースに次のような ThousandEyes メタデータが含まれていることを確認します。

- `thousandeyes.account.id`
- `thousandeyes.test.id`
- `thousandeyes.permalink`
- `thousandeyes.source.agent.id`

`thousandeyes.permalink` フィールド、または trace waterfall ビュー内の **Go to ThousandEyes test** ボタンを使用して、元の ThousandEyes テストに戻ります。

![Splunk APM trace linked back to ThousandEyes](../images/splunk-apm-trace.png)

## 推奨される学習シナリオ

ワークショップ中は次のフローを使用します。

1. 複数のサービスを呼び出す内部 API ルートに対して ThousandEyes テストを作成します。
2. ThousandEyes に問題を最初に表面化させ、ネットワークおよび合成監視の観点からクラスを開始します。
3. ThousandEyes で **Service Map** を開き、レイテンシーやエラーが発生し始める場所を特定します。
4. **Splunk APM** にジャンプして span レベルの分析を行います。
5. **ThousandEyes** に戻って、テスト、エージェント、ネットワークパスを再確認します。

これは、各チームが実際にどのように作業するかを反映しているため、強力な指導ループとなります。

- ネットワークおよびエッジチームは ThousandEyes から開始することが多い
- SRE およびプラットフォームチームは Splunk のダッシュボードまたはアラートから開始することが多い
- アプリケーションチームは通常、Splunk APM のトレースを必要とする

この統合があれば、誰もがコンテキストを失うことなく移動できます。

## よくある落とし穴

- テストが Splunk のダッシュボードに表示されているのに、トレース相関がない場合があります。これは通常、**メトリクス**ストリームのみが設定されており、**Splunk APM Generic Connector** が設定されていないことを意味します。
- トレースが Splunk APM に存在していても、監視対象のエンドポイントが下流にトレースヘッダーを伝播していない場合、ThousandEyes には表示されません。
- `/health` のような浅いエンドポイントでは、設定が正しくてもトレースの価値が限定的なことがよくあります。

## 参考資料

- [ThousandEyes Distributed Tracing](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing)
- [ThousandEyes Distributed Tracing with Splunk Observability APM](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm)
- [Splunk APM: View traces with Cisco ThousandEyes integration](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace)
- [Splunk OTel Collector zero-code instrumentation for Kubernetes language runtimes](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/automatic-discovery-of-apps-and-services/kubernetes/language-runtimes)
