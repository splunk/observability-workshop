---
title: デプロイメントのパッチ適用
linkTitle: 1. デプロイメントのパッチ適用
weight: 1
---

**自動検出と設定**を構成するには、デプロイメントに計装アノテーションを追加するためのパッチを適用する必要があります。パッチが適用されると、OpenTelemetry Collectorが自動検出と設定ライブラリを注入し、Podが再起動されてトレースとプロファイリングデータの送信が開始されます。まず、以下を実行して`api-gateway`に`splunk-otel-java`イメージがないことを確認します：

{{< tabs >}}
{{% tab title="Describe api-gateway" %}}

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

次に、デプロイメントにアノテーションを追加して、すべてのサービスのJava自動検出と設定を有効にします。以下のコマンドは、すべてのデプロイメントにパッチを適用します。これにより、OpenTelemetry Operatorが`splunk-otel-java`イメージをPodに注入します：

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

**config-server**、**discovery-server**、**admin-server**については、すでにパッチが適用されているため変更はありません。

`api-gateway` Podのコンテナイメージを再度確認するには、以下のコマンドを実行します：

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

`api-gateway`に新しいイメージが追加され、`ghcr.io`から`splunk-otel-java`がプルされます（注：2つの`api-gateway`コンテナが表示される場合、元のコンテナがまだ終了処理中の可能性があるため、数秒待ってください）。

**Splunk Observability Cloud**のKubernetes Navigatorに戻ります。数分後、Podがオペレーターによって再起動され、自動検出と設定コンテナが追加されることが確認できます。以下のスクリーンショットのような表示になります：

![restart](../../images/k8s-navigator-restarted-pods.png)

Kubernetes NavigatorでPodが緑色になるまで待ってから、次のセクションに進んでください。
