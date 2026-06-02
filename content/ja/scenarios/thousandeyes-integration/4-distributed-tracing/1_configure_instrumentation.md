---
title: Distributed Tracing and Bi-Directional Drilldowns
linkTitle: 4.1 Configure Instrumentation
weight: 1
time: 10 minutes
description: インストルメンテーションを設定する
---

## 必要な変更の概要

[ThousandEyes ドキュメント](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing)、特に [Splunk Observability APM 用のページ](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm)では、分散トレーシングに必要な設定が示されています。

Propagators について:

- `baggage`
- `b3` は ThousandEyes の B3 ヘッダーを抽出できるようにします。
- `tracecontext` は `traceparent` と `tracestate` を保持します。

加えて、サンプラーを `parentbased_always_on` に設定することで、ThousandEyes がリクエストを開始した後もトレースが継続されることを保証します。

{{% notice title="重要なポイント" style="warning" %}}
私たちのテスト（少なくとも本記事執筆時点）では、propagators の順序が結果に影響することと、デフォルト設定では動作しないことを確認しました。そのため、ここで正しい順序にパッチを当てる必要があります。
{{% /notice %}}

以下の変更を行います。

- ステップ 1: OTel Collector を変更
  - propagators の正しい順序（`baggage`、`b3`、`tracecontext`）でインストルメンテーションにパッチを当てる
- ステップ 2: アプリケーションにパッチを当てる
  - 各サービスに java インストルメンテーションをインジェクションするためのパッチを当てる

### ステップ 1: OTel Collector を変更する

インストルメンテーションの設定を確認しましょう。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe instrumentation splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Abbreviated Output" %}}

```text
Name:         splunk-otel-collector
Namespace:    default
Labels:       app=splunk-otel-collector
...
Spec:
...
  Propagators:
    tracecontext
    baggage
    b3
...
```

{{% /tab %}}
{{< /tabs >}}

`Propagators` の下を見ると、必要なものは設定されていますが、正しい順序にするためにパッチを当てます。

### ステップ 2: インストルメンテーションにパッチを当てる（デフォルトを修正するため）

ここではパッチを当てますが、今後アップグレードするとこの変更は失われます。そのため、本来は `values.yaml` ファイルを更新して、常に適用されるようにするのが正しい方法です。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl patch instrumentation splunk-otel-collector \
  --type=merge \
  -p '{
    "spec": {
      "propagators": ["baggage", "b3", "tracecontext"],
      "sampler": {
        "type": "parentbased_always_on"
      }
    }
  }'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
instrumentation.opentelemetry.io/splunk-otel-collector patched
```

{{% /tab %}}
{{< /tabs >}}

その後、Propagators が正しい順序で設定されていること、そしてサンプラーが追加されていることを確認できます。
{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe instrumentation splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Abbreviated Output" %}}

```text
Name:         splunk-otel-collector
Namespace:    default
Labels:       app=splunk-otel-collector
...
Spec:
...
  Propagators:
    baggage
    b3
    tracecontext
  ...
  Sampler:
    Type:  parentbased_always_on
...
```

{{% /tab %}}
{{< /tabs >}}

### ステップ 3: アプリケーションにパッチを当てる

まず、デプロイされているコンテナイメージを確認しましょう。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe pods api-gateway | grep Image:
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
    Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.7
```

{{% /tab %}}
{{< /tabs >}}

`api-gateway` のコンテナは 1 つだけであることがわかります。アプリケーションにパッチを当てると、複数のコンテナイメージ（api-gateway 用と、インストルメンテーション用）が表示されるようになります。

それでは java インストルメンテーションをインジェクションしましょう。（注: `config-server`、`discovery-server`、`admin-server` についてはすでにパッチ済みのため、変更はありません。）

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
deployment.apps/admin-server patched (no change)
deployment.apps/api-gateway patched
deployment.apps/config-server patched (no change)
deployment.apps/customers-service patched
deployment.apps/discovery-server patched (no change)
deployment.apps/vets-service patched
deployment.apps/visits-service patched

```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="他のランタイムの場合" style="info" %}}
他のランタイムを使用する場合は、その言語に合致するアノテーションを使用してください。例:

- `instrumentation.opentelemetry.io/inject-nodejs`
- `instrumentation.opentelemetry.io/inject-python`
- `instrumentation.opentelemetry.io/inject-dotnet`
{{% /notice %}}

インストルメンテーションがデプロイされたかは、以下で確認できます。
{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe pods api-gateway | grep Image:
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
    Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v2.27.0
    Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.7
```

{{% /tab %}}
{{< /tabs >}}

また、この Pod で Java インストルメンテーションが有効になっていること、そして propagators に `baggage`、`b3`、`tracecontext` が正しい順序で含まれていることも確認できます。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe pods api-gateway | grep OTEL_PROPAGATORS
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
      OTEL_PROPAGATORS:                      baggage,b3,tracecontext
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="すべての Pod を再起動する" style="warning" %}}
一部の Pod はすでにインジェクション済みのため、正しいインストルメンテーションを反映させるには、すべての Pod を再起動することが重要です。

そのためには:
{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl rollout restart deployment -l app.kubernetes.io/part-of=spring-petclinic
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
deployment.apps/admin-server restarted
deployment.apps/api-gateway restarted
deployment.apps/config-server restarted
deployment.apps/customers-service restarted
deployment.apps/discovery-server restarted
deployment.apps/petclinic-db restarted
deployment.apps/petclinic-loadgen-deployment restarted
deployment.apps/splunk-otel-collector-k8s-cluster-receiver restarted
deployment.apps/splunk-otel-collector-operator restarted
deployment.apps/thousandeyes restarted
deployment.apps/vets-service restarted
deployment.apps/visits-service restarted
```

{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}

これで、ThousandEyes Enterprise Agent が動作する namespace から、クラスター内 API パスを検証できます。

以下を実行してみてください。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl run te-petclinic-curl \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
[{"id":1,"firstName":"George","lastName":"Franklin","address":"110 W. Liberty St.","city":"Madison","telephone":"6085551023","pets":[{"id":1,"name":"Leo","birthDate":"2000-09-07","type":{"id":1,"name":"cat"}}]},{"id":2,"firstName":"Betty","lastName":"Davis","address":"638 Cardinal Ave.","city":"Sun Prairie","telephone":"6085551749","pets":[{"id":2,"name":"Basil","birthDate":"2002-08-06","type":{"id":6,"name":"hamster"}}]},{"id":3,"firstName":"Eduardo","lastName":"Rodriquez","address":"2693 Commerce St.","city":"McFarland","telephone":"6085558763","pets":[{"id":4,"name":"Jewel","birthDate":"2000-03-07","type":{"id":2,"name":"dog"}},{"id":3,"name":"Rosy","birthDate":"2001-04-17","type":{"id":2,"name":"dog"}}]},{"id":4,"firstName":"Harold","lastName":"Davis","address":"563 Friendly St.","city":"Windsor","telephone":"6085553198","pets":[{"id":5,"name":"Iggy","birthDate":"2000-11-30","type":{"id":3,"name":"lizard"}}]},{"id":5,"firstName":"Peter","lastName":"McTavish","address":"2387 S. Fair Way","city":"Madison","telephone":"6085552765","pets":[{"id":6,"name":"George","birthDate":"2000-01-20","type":{"id":4,"name":"snake"}}]},{"id":6,"firstName":"Jean","lastName":"Coleman","address":"105 N. Lake St.","city":"Monona","telephone":"6085552654","pets":[{"id":8,"name":"Max","birthDate":"1995-09-04","type":{"id":1,"name":"cat"}},{"id":7,"name":"Samantha","birthDate":"1995-09-04","type":{"id":1,"name":"cat"}}]},{"id":7,"firstName":"Jeff","lastName":"Black","address":"1450 Oak Blvd.","city":"Monona","telephone":"6085555387","pets":[{"id":9,"name":"Lucky","birthDate":"1999-08-06","type":{"id":5,"name":"bird"}}]},{"id":8,"firstName":"Maria","lastName":"Escobito","address":"345 Maple St.","city":"Madison","telephone":"6085557683","pets":[{"id":10,"name":"Mulligan","birthDate":"1997-02-24","type":{"id":2,"name":"dog"}}]},{"id":9,"firstName":"David","lastName":"Schroeder","address":"2749 Blackhawk Trail","city":"Madison","telephone":"6085559435","pets":[{"id":11,"name":"Freddy","birthDate":"2000-03-09","type":{"id":5,"name":"bird"}}]},{"id":10,"firstName":"Carlos","lastName":"Estaban","address":"2335 Independence La.","city":"Waunakee","telephone":"6085555487","pets":[{"id":12,"name":"Lucky","birthDate":"2000-06-24","type":{"id":2,"name":"dog"}},{"id":13,"name":"Sly","birthDate":"2002-06-08","type":{"id":1,"name":"cat"}}]}]pod "te-petclinic-curl" deleted from default namespace
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="少々お待ちください" style="warning" %}}
期待される出力が得られるまでに、しばらく時間がかかる場合があります。
{{% /notice %}}

あなたのデプロイ環境は以下のとおりです。
{{< tabs >}}
{{% tab title="Script" %}}

```bash
echo "thousandeyes-$INSTANCE"
```

{{% /tab %}}
{{% tab title="Example Output" %}}
thousandeyes-shw-xxxx
{{% /tab %}}
{{< /tabs >}}

Splunk Observability Cloud で、環境全体が表示されているはずです（あなたの環境 `thousandeyes-shw-xxxx` でフィルタしてください）。

![ThousandEyes Service Map](../../images/splunk-apm-service-map.png?width=45vw)
