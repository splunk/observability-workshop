---
title: TBD
linkTitle: 6.1 TBD
weight: 1
time: 10 minutes
description: TBD
draft: true
---

## サポートされるワークフロー

この学習シナリオは、ThousandEyes と Splunk が文書化しているサポート対象のワークフローに従います

- ThousandEyes は、分散トレーシングが有効な場合、**HTTP Server** テストおよび **API** テストに `b3`、`traceparent`、`tracestate` ヘッダーを自動的に挿入します。
- 監視対象のエンドポイントは、ヘッダーを受け入れ、OpenTelemetry で計装され、トレースコンテキストを伝播し、オブザーバビリティバックエンドにトレースを送信する必要があります。
- Splunk APM の場合、ThousandEyes は `https://api.<REALM>.signalfx.com` を指す **Generic Connector** を使用し、**API-scope** の Splunk トークンで認証します。
- Splunk APM は、一致するトレースに `thousandeyes.test.id` や `thousandeyes.permalink` などの ThousandEyes 属性を付加し、ThousandEyes への逆方向のジャンプを可能にします。

## これらのヘッダーが実際に意味すること

この部分は見過ごされがちですが、見過ごすべきではありません。トレースの相関は、サービスが ThousandEyes の挿入するヘッダーを理解し、トレースを正しく継続する場合にのみ機能します。

- `traceparent` と `tracestate` は W3C Trace Context ヘッダーです。
- `b3` は Zipkin B3 シングルヘッダー形式です。
- ThousandEyes が両方を挿入するのは、実際の環境にはプロキシ、メッシュ、ゲートウェイ、アプリランタイムが混在しており、すべてが同じ伝播形式を優先するとは限らないためです。

OpenTelemetry の用語では、重要な設定はプロパゲーターリストです

```text
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

これにより2つのことが実現されます

1. サービスが、受信した ThousandEyes リクエストから **B3** または **W3C** コンテキストのいずれかを抽出できるようになります。
2. `tracecontext` を有効にしておくことで、W3C の `tracestate` が保持されます。

{{% notice title="重要な詳細" style="warning" %}}
`tracestate` を別の OpenTelemetry プロパゲーターとして追加する必要は**ありません**。`tracecontext` プロパゲーターが `traceparent` と `tracestate` の両方を処理します。
{{% /notice %}}

## 「正しく構成された」状態とは

コレクターはこのセットアップの一部に過ぎません。Kubernetes における正しい ThousandEyes トレーシングデプロイメントには **3つのレイヤー** があります

1. **Deployment アノテーション** — OpenTelemetry Operator がランタイム固有の計装を挿入できるようにします。
2. **Instrumentation リソース** — 挿入された SDK がトレースの送信先と使用するプロパゲーターを認識できるようにします。
3. **Collector トレースパイプライン** — OTLP トレースが実際に受信され、Splunk APM にエクスポートされるようにします。

最もよくある間違いは、コレクターだけに焦点を当てることです。コレクターは生の `b3`、`traceparent`、`tracestate` リクエストヘッダーを直接見ることはありません。アプリケーションまたは自動計装ライブラリがまずこれらのヘッダーを抽出し、スパンコンテキストを継続してから、OTLP 経由でコレクターにスパンを送信する必要があります。

## PetClinic 構成パターン

以下の例では、このワークショップに含まれる Spring PetClinic アプリケーションを使用します。ThousandEyes がトレース相関に必要とする Kubernetes アノテーション、`Instrumentation` リソース、および Pod レベルの設定を示します。

### 1. Deployment アノテーション

このガイドでは、PetClinic の Java デプロイメントは `default/splunk-otel-collector` Instrumentation リソースを参照しています

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

ThousandEyes のリクエストがトレースに変換されない場合、最初に確認すべき場所です。

### 2. Instrumentation リソース

これは PetClinic の `Instrumentation` オブジェクトで、ThousandEyes に関連するフィールドのみを抜粋したものです

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

ThousandEyes シナリオにおける重要なポイントは以下の通りです

- `endpoint` はクラスターローカルの OTel エージェントサービスにスパンを送信します。
- `b3` は ThousandEyes B3 ヘッダーの抽出を可能にします。
- `tracecontext` は `traceparent` と `tracestate` を保持します。
- `parentbased_always_on` は、ThousandEyes がリクエストを開始した後もトレースが継続されることを保証します。

### 3. 挿入された Pod が実際に受け取る設定

実行中の PetClinic `api-gateway` Pod で、オペレーターが期待される OpenTelemetry 設定を挿入したことを検証します

```bash
kubectl exec deploy/api-gateway -- printenv | \
  grep -E 'OTEL_EXPORTER_OTLP_ENDPOINT|OTEL_PROPAGATORS|OTEL_TRACES_SAMPLER|OTEL_RESOURCE_ATTRIBUTES'
```

以下のような値が表示されるはずです

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

これは有用な検証チェックポイントです。プロパゲーターが抽象的な設定オブジェクトで宣言されているだけでなく、実際にワークロードに適用されていることを証明するためです。

### 4. Agent Collector トレースパイプライン

`otel-splunk` 内のライブエージェントコレクターは、OTLP、Jaeger、Zipkin トラフィックを受信し、トレースを上流に転送しています。以下は、実行中の ConfigMap から抜粋したものです

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

ThousandEyes にとって重要なのは、コレクターの特別な B3 オプションではありません。重要なのは、コレクターが `4317` と `4318` で OTLP を公開しており、サービスがそこにスパンをエクスポートしていることです。

{{% notice title="PetClinic のポイント" style="info" %}}
PetClinic の `Instrumentation` リソースは、`b3` と `tracecontext` を明示的に含んでいるため、ThousandEyes で従うべきパターンです。これがこのシナリオで必要な構成です。
{{% /notice %}}

{{% notice title="重要" style="warning" %}}
このセクションではブラウザページの URL を使用**しないでください**。ThousandEyes のドキュメントによると、ブラウザはこのワークフローに必要なカスタムトレースヘッダーを受け入れません。代わりに、**HTTP Server** テストまたは **API** テストの背後にある計装済みのバックエンドエンドポイントを使用してください。
{{% /notice %}}
