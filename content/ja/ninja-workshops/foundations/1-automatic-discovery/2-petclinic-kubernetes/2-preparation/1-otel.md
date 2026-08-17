---

title: Splunk OpenTelemetry Collector のデプロイ
linkTitle: 1. OpenTelemetry Collector のデプロイ
weight: 1
---

オブザーバビリティシグナル（**メトリクス、トレース**、**ログ**）を **Splunk Observability Cloud** に送信するには、KubernetesクラスターにSplunk OpenTelemetry Collectorをデプロイする必要があります。

このワークショップでは、Splunk OpenTelemetry Collector Helm Chartを使用します。まず、Helm chartリポジトリをHelmに追加し、`helm repo update` を実行して最新バージョンを確認します

{{< tabs >}}
{{% tab title="Install Helm Chart" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
```

{{% /tab %}}
{{< /tabs >}}

**Splunk Observability Cloud** では、Kubernetes上でのOpenTelemetry Collectorのセットアップを案内するUIウィザードが提供されていますが、時間の都合上、以下のHelm installコマンドを使用します。自動ディスカバリーおよび設定とコードプロファイリング用のオペレーターを有効にするための追加パラメータが設定されています。

* `--set="operator.enabled=true"` - 自動ディスカバリーおよび設定を処理するためのOpenTelemetryオペレーターをインストールします。
* `--set="splunkObservability.profilingEnabled=true"` - オペレーター経由でコードプロファイリングを有効にします。

Collectorをインストールするには、以下のコマンドを実行してください。これを編集**しないでください**

{{< tabs >}}
{{% tab title="Helm Install" %}}

```bash
helm install splunk-otel-collector --version {{< otel-version >}} \
--set="operatorcrds.install=true", \
--set="operator.enabled=true", \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkObservability.profilingEnabled=true" \
--set="agent.service.enabled=true"  \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml

{{% /tab %}}
{{% tab title="Output" %}}

``` plaintext
LAST DEPLOYED: Fri Apr 19 09:39:54 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Platform endpoint "https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event".

Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm eu0.

[INFO] You've enabled the operator's auto-instrumentation feature (operator.enabled=true)! The operator can automatically instrument Kubernetes hosted applications.
  - Status: Instrumentation language maturity varies. See `operator.instrumentation.spec` and documentation for utilized instrumentation details.
  - Splunk Support: We offer full support for Splunk distributions and best-effort support for native OpenTelemetry distributions of auto-instrumentation libraries.
```

{{% /tab %}}
{{< /tabs >}}

続行する前に、Podが **Running** として報告されていることを確認してください（通常約30秒かかります）。

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods | grep splunk-otel
```

{{% /tab %}}
{{% tab title="Output" %}}

``` text
splunk-otel-collector-k8s-cluster-receiver-6bd5567d95-5f8cj     1/1     Running   0          10m
splunk-otel-collector-agent-tspd2                               1/1     Running   0          10m
splunk-otel-collector-operator-69d476cb7-j7zwd                  2/2     Running   0          10m
```

{{% /tab %}}
{{< /tabs >}}

Splunk OpenTelemetry Collectorからエラーが報告されていないことを確認してください（`ctrl + c` で終了）。または、インストール済みの**素晴らしい** `k9s` ターミナルUIを使用するとボーナスポイントです！

{{< tabs >}}
{{% tab title="kubectl logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
2021-03-21T16:11:10.900Z        INFO    service/service.go:364  Starting receivers...
2021-03-21T16:11:10.900Z        INFO    builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:75 Receiver started.       {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.009Z        INFO    k8sclusterreceiver@v0.21.0/watcher.go:195       Configured Kubernetes MetadataExporter  {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster", "exporter_name": "signalfx"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:75 Receiver started.       {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.009Z        INFO    healthcheck/handler.go:128      Health Check state change       {"component_kind": "extension", "component_type": "health_check", "component_name": "health_check", "status": "ready"}
2021-03-21T16:11:11.009Z        INFO    service/service.go:267  Everything is ready. Begin running and processing data.
2021-03-21T16:11:11.009Z        INFO    k8sclusterreceiver@v0.21.0/receiver.go:59       Starting shared informers and wait for initial cache sync.      {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.281Z        INFO    k8sclusterreceiver@v0.21.0/receiver.go:75       Completed syncing shared informer caches.       {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
```

{{% /tab %}}
{{< /tabs >}}

>[!INFO] 失敗したインストールの削除
>OpenTelemetry Collector のインストールでエラーが発生した場合は、
>以下のコマンドでインストールを削除してやり直すことができます
>
>``` bash
>helm delete splunk-otel-collector
>```
