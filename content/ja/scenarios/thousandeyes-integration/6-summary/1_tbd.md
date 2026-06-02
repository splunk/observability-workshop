---
title: TBD
linkTitle: 6.1 TBD
weight: 1
time: 10 minutes
description: TBD
draft: true
---

## サポートされているワークフロー

このラーニングシナリオは、ThousandEyes と Splunk によってドキュメント化されているサポート対象のワークフローに従っています。

- ThousandEyes は分散トレーシングが有効化されている場合、**HTTP Server** および **API** テストに対して `b3`、`traceparent`、`tracestate` ヘッダーを自動的に注入します。
- 監視対象のエンドポイントはヘッダーを受け入れ、OpenTelemetry でインストルメンテーションされ、トレースコンテキストを伝播し、observability バックエンドにトレースを送信する必要があります。
- Splunk APM では、ThousandEyes は `https://api.<REALM>.signalfx.com` を指す **Generic Connector** を使用し、**API スコープ** の Splunk トークンで認証します。
- Splunk APM は一致するトレースに `thousandeyes.test.id` や `thousandeyes.permalink` などの ThousandEyes 属性を付加し、これにより ThousandEyes への逆方向のジャンプが可能になります。

## これらのヘッダーが実際に意味するもの

この部分は読み流されがちですが、流すべきではありません。トレースの相関は、サービスが ThousandEyes が注入するヘッダーを理解し、トレースを正しく継続できる場合にのみ機能します。

- `traceparent` と `tracestate` は W3C Trace Context ヘッダーです。
- `b3` は Zipkin B3 single-header フォーマットです。
- 実環境にはプロキシ、メッシュ、ゲートウェイ、アプリケーションランタイムが混在しており、これらすべてが同じ伝播フォーマットを優先するわけではないため、ThousandEyes は両方を注入します。

OpenTelemetry の用語では、重要な設定は propagator のリストです。

```text
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

これは 2 つのことを実現します。

1. サービスが ThousandEyes からの受信リクエストから **B3** または **W3C** コンテキストのいずれかを抽出できるようにします。
2. `tracecontext` を有効にすることで W3C `tracestate` を保持します。

{{% notice title="重要な詳細" style="warning" %}}
`tracestate` を別の OpenTelemetry propagator として追加する必要は **ありません**。`tracecontext` propagator が `traceparent` と `tracestate` の両方を処理します。
{{% /notice %}}

## 「正しく実装された状態」とはどういう状態か

Collector はこのセットアップの 1 つの構成要素にすぎません。Kubernetes における正しい ThousandEyes トレーシングのデプロイには **3 つのレイヤー** があります。

1. **Deployment アノテーション**: OpenTelemetry Operator がランタイム固有のインストルメンテーションを注入できるようにします。
2. **Instrumentation リソース**: 注入された SDK がトレースの送信先と使用する propagator を認識できるようにします。
3. **Collector トレースパイプライン**: OTLP トレースが実際に受信され、Splunk APM にエクスポートされるようにします。

最もよくある間違いは、Collector のみに焦点を当ててしまうことです。Collector は生の `b3`、`traceparent`、`tracestate` リクエストヘッダーを直接見ることはありません。アプリケーションまたは自動インストルメンテーションライブラリが最初にこれらのヘッダーを抽出し、span コンテキストを継続し、その後 OTLP 経由で Collector にスパンを送信する必要があります。

## PetClinic の設定パターン

以下の例では、このワークショップに含まれる Spring PetClinic アプリケーションを使用します。これらは ThousandEyes がトレース相関のために必要とする Kubernetes アノテーション、`Instrumentation` リソース、Pod レベルの設定を示しています。

### 1. Deployment アノテーション

このガイドでは、PetClinic Java の Deployment は `default/splunk-otel-collector` Instrumentation リソースを指しています。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-java: default/splunk-otel-collector
```

ThousandEyes のリクエストがトレースに変換されない場合、これが最初に確認すべき箇所です。

### 2. Instrumentation リソース

これは PetClinic の `Instrumentation` オブジェクトを、ThousandEyes に関連するフィールドのみに絞ったものです。

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: splunk-otel-collector
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
      value: deployment.environment=thousandeyes-petclinic
```

これが ThousandEyes シナリオにとって重要な部分です。

- `endpoint` はクラスター内の OTel agent サービスにスパンを送信します。
- `b3` により ThousandEyes の B3 ヘッダーを抽出できます。
- `tracecontext` は `traceparent` と `tracestate` を保持します。
- `parentbased_always_on` は ThousandEyes がリクエストを開始した後にトレースが確実に継続されるようにします。

### 3. 注入された Pod が実際に取得する内容

実行中の PetClinic `api-gateway` Pod で、Operator が期待される OpenTelemetry の設定を注入したことを検証します。

```bash
kubectl exec deploy/api-gateway -- printenv | \
  grep -E 'OTEL_EXPORTER_OTLP_ENDPOINT|OTEL_PROPAGATORS|OTEL_TRACES_SAMPLER|OTEL_RESOURCE_ATTRIBUTES'
```

以下のような値が表示されるはずです。

```yaml
- name: OTEL_EXPORTER_OTLP_ENDPOINT
  value: http://splunk-otel-collector-agent.otel-splunk.svc:4317
- name: OTEL_PROPAGATORS
  value: baggage,b3,tracecontext
- name: OTEL_TRACES_SAMPLER
  value: parentbased_always_on
- name: OTEL_RESOURCE_ATTRIBUTES
  value: deployment.environment=thousandeyes-petclinic
```

これは有用な検証チェックポイントです。なぜなら、propagator が抽象的な設定オブジェクト内で宣言されているだけでなく、実際にワークロードに適用されていることを証明できるためです。

### 4. Agent Collector のトレースパイプライン

`otel-splunk` で稼働する agent collector は OTLP、Jaeger、Zipkin のトラフィックを受信し、トレースを上流に転送しています。以下は実行中の ConfigMap から抜粋したものです。

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

ThousandEyes にとって重要なのは、Collector における特別な B3 オプションではありません。重要なのは、Collector が `4317` と `4318` で OTLP を公開し、サービスがそこにスパンをエクスポートしていることです。

{{% notice title="PetClinic から得られる要点" style="info" %}}
PetClinic の `Instrumentation` リソースは、`b3` を `tracecontext` と一緒に明示的に含んでいるため、ThousandEyes で踏襲すべきパターンです。これがこのシナリオで必要となる設定です。
{{% /notice %}}

{{% notice title="重要" style="warning" %}}
このセクションではブラウザのページ URL を **使用しないでください**。ThousandEyes は、ブラウザがこのワークフローに必要なカスタムトレースヘッダーを受け入れないことをドキュメント化しています。代わりに、**HTTP Server** または **API** テストの背後にあるインストルメンテーション済みのバックエンドエンドポイントを使用してください。
{{% /notice %}}
