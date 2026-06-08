---
title: Deployment のパッチ適用
linkTitle: 1. Deployment のパッチ適用
weight: 1
---

**automatic discovery and configuration** を設定するには、計装アノテーションを追加するために Deployment にパッチを適用する必要があります。パッチが適用されると、OpenTelemetry Collector が automatic discovery and configuration ライブラリを注入し、トレースとプロファイリングデータの送信を開始するために Pod が再起動されます。まず、`api-gateway` に `splunk-otel-java` イメージがまだ含まれていないことを確認するために、以下を実行します:

{{< tabs >}}
{P}{{% tab title="Describe api-gateway" %}}

``` bash
kubectl describe pods api-gateway | grep Image:
```

{{% /tab %}}
{{% tab title="Describe Output" %}}

``` text
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

{{% /tab %}}
{{< /tabs >}}

次に、Deployment にアノテーションを追加して、すべてのサービスに対して Java の automatic discovery and configuration を有効にします。以下のコマンドはすべての Deployment にパッチを適用します。これにより、OpenTelemetry Operator が Pod に `splunk-otel-java` イメージを注入するようトリガーされます:

{{< tabs >}}
{{% tab title="Patch all PetClinic services" %}}

``` bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"
```

{{% /tab %}}
{{% tab title="Patch Output" %}}

``` text
deployment.apps/config-server patched (no change)
deployment.apps/admin-server patched (no change)
deployment.apps/customers-service patched
deployment.apps/visits-service patched
deployment.apps/discovery-server patched (no change)
deployment.apps/vets-service patched
deployment.apps/api-gateway patched
```

{{% /tab %}}
{{< /tabs >}}

**config-server**、**discovery-server**、**admin-server** はすでにパッチが適用されているため、変更はありません。

`api-gateway` Pod のコンテナイメージを再度確認するには、以下のコマンドを実行します:

{{< tabs >}}
{{% tab title="Describe api-gateway" %}}

``` bash
kubectl describe pods api-gateway | grep Image:
```

{{% /tab %}}
{{% tab title="Describe Output" %}}

```text
Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v1.30.0
Image:         quay.io/phagen/spring-petclinic-api-gateway:0.0.2
```

{{% /tab %}}
{{< /tabs >}}

`api-gateway` に新しいイメージが追加され、`ghcr.io` から `splunk-otel-java` がプルされます（注: `api-gateway` コンテナが2つ表示される場合、元のコンテナがまだ終了処理中の可能性がありますので、数秒お待ちください）。

**Splunk Observability Cloud** の Kubernetes Navigator に戻ります。数分後、Operator によって Pod が再起動され、automatic discovery and configuration コンテナが追加されるのが確認できます。以下のスクリーンショットのように表示されます:

![restart](../../images/k8s-navigator-restarted-pods.png)

Kubernetes Navigator で Pod が緑色になるのを待ってから、次のセクションに進んでください。
