---
title: Patching the Deployment
linkTitle: 1. Patching the Deployment
weight: 1
---

**自動検出と設定（automatic discovery and configuration）**を構成するには、計装用のアノテーションを追加するために Deployment にパッチを適用する必要があります。パッチが適用されると、OpenTelemetry Collector が自動検出と設定のライブラリを注入し、Pod が再起動されてトレースとプロファイリングデータの送信が開始されます。まず、以下を実行して `api-gateway` に `splunk-otel-java` イメージが含まれていないことを確認します。

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

次に、Deployment にアノテーションを追加して、すべてのサービスに対して Java の自動検出と設定を有効にします。次のコマンドはすべての Deployment にパッチを適用します。これにより、OpenTelemetry Operator がトリガーされ、`splunk-otel-java` イメージが Pod に注入されます。

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

`api-gateway` Pod のコンテナイメージを再度確認するには、次のコマンドを実行します。

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

`api-gateway` に新しいイメージが追加され、`ghcr.io` から `splunk-otel-java` がプルされます（注：`api-gateway` コンテナが2つ表示される場合、元のコンテナがまだ終了処理中である可能性が高いので、数秒待ってください）。

**Splunk Observability Cloud** の Kubernetes Navigator に戻ります。数分後、Operator によって Pod が再起動され、自動検出と設定のコンテナが追加されることが確認できます。これは以下のスクリーンショットのように表示されます。

![restart](../../images/k8s-navigator-restarted-pods.png)

Kubernetes Navigator で Pod が緑色になるまで待ってから、次のセクションに進んでください。
