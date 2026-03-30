---
title: 分散トレーシングと双方向ドリルダウン
linkTitle: 4. 分散トレーシング
weight: 4
time: 25 minutes
description: ThousandEyes と Splunk APM 間でサポートされているトレース相関を有効にし、調査中にチームが両製品間を移動できるようにします。
---

このセクションでは、ThousandEyesとSplunkの統合を真の調査ワークフローに変えます。前のセクションでは、ThousandEyesが合成メトリクスをSplunk Observability Cloudにストリーミングしました。このセクションでは、サポートされている **ThousandEyes <-> Splunk APM 分散トレーシング統合** を有効にし、ネットワーク、プラットフォーム、アプリケーションチームが同じリクエストを見ながら両方のツール間を行き来できるようにします。

{{% notice title="これが重要な理由" style="primary" icon="lightbulb" %}}
これは、2つの環境間で **双方向アクセス** を可能にする部分です。ThousandEyesからSplunk APMの関連トレースを開くことができ、Splunk APMから元のThousandEyesテストに戻ることができます。
{{% /notice %}}

## 学習内容

このセクションを終了すると、以下のことができるようになります：

- 内部サービスを計装してSplunk APMにトレースを送信する
- ThousandEyesの **HTTP Server** または **API** テストで分散トレーシングを有効にする
- Splunk APM用のThousandEyes **Generic Connector** を設定する
- ThousandEyesの **Service Map** を開き、対応するSplunkトレースに直接ジャンプする
- Splunk APMのThousandEyesメタデータを使用して、元のThousandEyesテストに戻る

## サポートされているワークフロー

この学習シナリオは、ThousandEyesとSplunkがドキュメント化しているサポートされたワークフローに従います：

- ThousandEyesは、分散トレーシングが有効になっている場合、**HTTP Server** および **API** テストに `b3`、`traceparent`、`tracestate` ヘッダーを自動的に挿入します。
- 監視対象のエンドポイントは、ヘッダーを受け入れ、OpenTelemetryで計装され、トレースコンテキストを伝播し、オブザーバビリティバックエンドにトレースを送信する必要があります。
- Splunk APMの場合、ThousandEyesは `https://api.<REALM>.signalfx.com` を指し、**API スコープ** のSplunkトークンで認証する **Generic Connector** を使用します。
- Splunk APMは、`thousandeyes.test.id` や `thousandeyes.permalink` などのThousandEyes属性で一致するトレースを強化し、ThousandEyesへの逆ジャンプを可能にします。

## これらのヘッダーの実際の意味

この部分は見落としがちですが、そうすべきではありません。トレース相関は、サービスがThousandEyesが挿入するヘッダーを理解し、トレースを正しく継続する場合にのみ機能します。

- `traceparent` と `tracestate` はW3C Trace Contextヘッダーです。
- `b3` はZipkin B3シングルヘッダー形式です。
- ThousandEyesは両方を挿入します。これは、実際の環境には、同じ伝播形式を好まないプロキシ、メッシュ、ゲートウェイ、アプリランタイムが混在していることが多いためです。

OpenTelemetryの用語では、重要な設定はプロパゲーターリストです：

```text
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

これは2つのことを行います：

1. サービスが受信ThousandEyesリクエストから **B3** または **W3C** コンテキストのいずれかを抽出できるようにします。
2. `tracecontext` を有効にしておくことで、W3C `tracestate` を保持します。

{{% notice title="重要な詳細" style="warning" %}}
`tracestate` を別のOpenTelemetryプロパゲーターとして追加する必要は **ありません**。`tracecontext` プロパゲーターが `traceparent` と `tracestate` の両方を処理します。
{{% /notice %}}

## 「正しく行う」とはどういうことか

コレクターはこのセットアップの一部に過ぎません。Kubernetesでの正しいThousandEyesトレーシングデプロイメントには **3 つのレイヤー** があります：

1. **Deployment アノテーション** - OpenTelemetry Operatorがランタイム固有の計装を挿入するため。
2. **Instrumentation リソース** - 挿入されたSDKがトレースの送信先と使用するプロパゲーターを知るため。
3. **Collector トレースパイプライン** - OTLPトレースが実際に受信され、Splunk APMにエクスポートされるため。

最も一般的な間違いは、コレクターだけに焦点を当てることです。コレクターは生の `b3`、`traceparent`、または `tracestate` リクエストヘッダーを直接見ることはありません。アプリケーションまたは自動計装ライブラリがまずそれらのヘッダーを抽出し、スパンコンテキストを継続し、次にOTLP経由でコレクターにスパンを送信する必要があります。

## 現在のクラスターからの実際の設定

以下の例は、このワークショップを現在実行しているライブクラスターからトリミングされたものです。これらは、今日Kubernetesで実際に機能しているパターンを示しています。

### 1. Deployment アノテーション

ライブクラスターでは、`teastore` アプリケーションは `teastore/default` Instrumentationリソースを指しています：

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

これは、ThousandEyesリクエストがトレースに変換されない場合に最初に確認する場所です。

### 2. Instrumentation リソース

これは `teastore` からのライブ `Instrumentation` オブジェクトで、ThousandEyesに関係するフィールドにトリミングされています：

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

これがThousandEyesシナリオの重要な部分です：

- `endpoint` はクラスターローカルのOTelエージェントサービスにスパンを送信します。
- `b3` はThousandEyes B3ヘッダーの抽出を可能にします。
- `tracecontext` は `traceparent` と `tracestate` を保持します。
- `parentbased_always_on` は、ThousandEyesがリクエストを開始するとトレースが継続することを保証します。

### 3. 挿入された Pod が実際に取得するもの

実行中の `teastore-webui-v1` Podでは、オペレーターが以下の環境変数を挿入しました：

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

これは有用な検証チェックポイントです。プロパゲーターが抽象的な設定オブジェクトで宣言されているだけでなく、ワークロードに適用されていることを証明するためです。

### 4. Agent Collector トレースパイプライン

`otel-splunk` のライブエージェントコレクターは、OTLP、Jaeger、Zipkinトラフィックを受信し、上流にトレースを転送しています。これは実行中のConfigMapからのトリミングされた抜粋です：

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

ThousandEyesの場合、重要な部分はコレクターの特別なB3オプションではありません。重要な部分は、コレクターが `4317` と `4318` でOTLPを公開していること、およびサービスがそこにスパンをエクスポートしていることです。

### 5. Gateway Collector の Splunk APM へのエクスポート

ライブゲートウェイコレクターは、トレースをSplunk Observability Cloudに転送します。これは実行中のゲートウェイConfigMapの関連部分です：

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

これは、スパンをSplunk APMに送信する部分です。このパイプラインが壊れている場合、ThousandEyesはリクエストにヘッダーを挿入できますが、相関トレースがSplunkに表示されることはありません。

{{% notice title="現在のクラスターのポイント" style="info" %}}
ライブクラスターでは、`teastore/default` InstrumentationリソースがThousandEyesで従うべきパターンです。これは `b3` と `tracecontext` を明示的に含んでいるためです。これが、このシナリオで複製したい設定です。
{{% /notice %}}

{{% notice title="重要" style="warning" %}}
このセクションではブラウザページのURLを使用 **しないでください**。ThousandEyesのドキュメントによると、ブラウザはこのワークフローに必要なカスタムトレースヘッダーを受け入れません。代わりに、**HTTP Server** または **API** テストの背後にある計装されたバックエンドエンドポイントを使用してください。
{{% /notice %}}

## ステップ 1：ワークロードが Splunk APM にトレースを送信していることを確認する

アプリケーションがすでに計装されていて、トレースがSplunk APMに表示されている場合は、ステップ2にスキップできます。そうでない場合、Kubernetesでの最速の学習パスは、ゼロコード計装用のオペレーターを有効にしたSplunk OpenTelemetry Collectorを使用することです。

### Splunk OpenTelemetry Collector とオペレーターをインストールする

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update

helm install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --namespace otel-splunk \
  --create-namespace \
  --set splunkObservability.realm=$REALM \
  --set splunkObservability.accessToken=$ACCESS_TOKEN \
  --set clusterName=$CLUSTER_NAME \
  --set operator.enabled=true \
  --set operatorcrds.install=true
```

### 自動計装用に Deployment にアノテーションを付ける

Javaワークロードの場合、一般的な例は次のようになります：

```bash
kubectl patch deployment api-gateway -n production -p '{"spec":{"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"otel-splunk/splunk-otel-collector"}}}}}'
```

他のランタイムの場合は、言語に合ったアノテーションを使用してください：

- `instrumentation.opentelemetry.io/inject-nodejs`
- `instrumentation.opentelemetry.io/inject-python`
- `instrumentation.opentelemetry.io/inject-dotnet`

コレクターがアプリケーションと同じ名前空間にインストールされている場合、公式のSplunkドキュメントでは `"true"` をアノテーション値として使用することもサポートしています。

このワークショップ環境の **ライブクラスターパターン** に従いたい場合、アノテーション値は名前空間修飾され、`teastore/default` Instrumentationオブジェクトを指します：

```bash
kubectl patch deployment teastore-webui-v1 -n teastore -p '{"spec":{"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/container-names":"teastore-webui-v1","instrumentation.opentelemetry.io/inject-java":"teastore/default"}}}}}'
```

### トレースが存在することを検証する

1. デプロイメントのロールアウトが完了するまで待ちます：

   ```bash
   kubectl rollout status deployment/api-gateway -n production
   ```

2. 複数のサービスを横断するバックエンドエンドポイントに対していくつかのリクエストを生成します。例：

   ```text
   http://api-gateway.production.svc.cluster.local:8080/api/v1/orders
   ```

   現在のワークショップクラスターでは、`http://teastore-webui.teastore.svc.cluster.local:8080/` のようなサービスが適切なターゲットです。これは、いくつかの下流アプリケーションサービスをフロントエンドし、単純なヘルスチェックよりも有用なエンドツーエンドトレースを生成するためです。

3. 続行する前に、**Splunk APM** にトレースが到着していることを確認してください。

{{% notice title="学習のヒント" style="info" %}}
トレーシング演習には、純粋な `/health` エンドポイントではなく、ビジネストランザクションを使用してください。マルチサービスリクエストは、ThousandEyesでより良いService Mapを提供し、Splunk APMでより有用なトレースを提供します。
{{% /notice %}}

## ステップ 2：ThousandEyes テストで分散トレーシングを有効にする

ステップ1の計装されたバックエンドエンドポイントをターゲットとする **HTTP Server** または **API** テストを作成または編集します。

1. ThousandEyesで、**HTTP Server** または **API** テストを作成します。
2. **Advanced Settings** を開きます。
3. **Distributed Tracing** を有効にします。
4. テストを保存し、すでにSplunk APMにトレースを送信しているのと同じエンドポイントに対して実行します。

![ThousandEyes で分散トレーシングを有効にする](../images/distributed-tracing-enable.png)

テストが実行された後、ThousandEyesはトレースヘッダーを挿入し、そのリクエストのトレースコンテキストをキャプチャします。

## ステップ 3：ThousandEyes で Splunk APM コネクターを作成する

前のセクションのメトリックストリーミング統合は **Ingest** トークンを使用します。このステップは異なります：ThousandEyesはSplunk APMにクエリを実行してトレースリンクを構築する必要があるため、代わりにSplunk **API** トークンを使用します。

1. Splunk Observability Cloudで、**API** スコープを持つアクセストークンを作成します。
2. ThousandEyesで、**Manage > Integrations > Integrations 2.0** に移動します。
3. 以下の設定で **Generic Connector** を作成します：
   - **Target URL**: `https://api.<REALM>.signalfx.com`
   - **Header**: `X-SF-Token: <your-api-scope-token>`
4. 新しい **Operation** を作成し、**Splunk Observability APM** を選択します。
5. オペレーションを有効にして、統合を保存します。

![ThousandEyes の Splunk APM Generic Connector](../images/splunk-apm-generic-connector.png)

![ThousandEyes の Splunk APM オペレーション](../images/splunk-apm-operation.png)

## ステップ 4：双方向調査ループを検証する

テストが実行され、コネクターが有効になったら、両方向でワークフローを検証します。

### ThousandEyes から始める

1. ThousandEyesでテストを開きます。
2. **Service Map** タブに移動します。
3. トレースパス、サービスレイテンシー、下流のエラーが表示されることを確認します。
4. ThousandEyesから **Splunk APM** へのリンクを使用して、完全なトレースを検査します。

![Splunk APM 相関を持つ ThousandEyes Service Map](../images/thousandeyes-service-map.png)

### Splunk APM で続ける

Splunk APM内で、トレースに以下のようなThousandEyesメタデータが含まれていることを確認します：

- `thousandeyes.account.id`
- `thousandeyes.test.id`
- `thousandeyes.permalink`
- `thousandeyes.source.agent.id`

`thousandeyes.permalink` フィールドまたはトレースウォーターフォールビューの **Go to ThousandEyes test** ボタンを使用して、元のThousandEyesテストに戻ります。

![ThousandEyes にリンクされた Splunk APM トレース](../images/splunk-apm-trace.png)

## 推奨される学習シナリオ

ワークショップ中に以下のフローを使用してください：

1. 複数のサービスを呼び出す内部APIルートに対するThousandEyesテストを作成します。
2. ThousandEyesに最初に問題を表示させ、クラスがネットワークと合成モニタリングの観点から始められるようにします。
3. ThousandEyesで **Service Map** を開き、レイテンシーやエラーがどこから始まるかを特定します。
4. スパンレベルの分析のために **Splunk APM** にジャンプします。
5. テスト、エージェント、ネットワークパスを再度検査するために **ThousandEyes** に戻ります。

これは、異なるチームが実際に作業する方法を反映しているため、強力な教育ループです：

- ネットワークおよびエッジチームは、ThousandEyesから始めることが多いです。
- SREおよびプラットフォームチームは、Splunkダッシュボードまたはアラートから始めることが多いです。
- アプリケーションチームは、通常Splunk APMのトレースを求めます。

この統合が整っていれば、全員がコンテキストを失うことなく切り替えることができます。

## よくある落とし穴

- テストがSplunkダッシュボードに表示されていても、トレース相関がない場合があります。これは通常、**メトリクス** ストリームのみが設定されており、**Splunk APM Generic Connector** が設定されていないことを意味します。
- 監視対象のエンドポイントがトレースヘッダーを下流に伝播しない場合、トレースがSplunk APMに存在してもThousandEyesに表示されない場合があります。
- `/health` のような浅いエンドポイントは、設定が正しくても限られたトレース価値しか生成しないことがよくあります。

## 参考資料

- [ThousandEyes Distributed Tracing](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing)
- [ThousandEyes Distributed Tracing with Splunk Observability APM](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm)
- [Splunk APM: View traces with Cisco ThousandEyes integration](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace)
- [Splunk OTel Collector zero-code instrumentation for Kubernetes language runtimes](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/automatic-discovery-of-apps-and-services/kubernetes/language-runtimes)
