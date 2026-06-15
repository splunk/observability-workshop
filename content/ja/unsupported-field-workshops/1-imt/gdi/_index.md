---
title: Kubernetes への OpenTelemetry Collector のデプロイ
linkTitle: 2. Get Data In
weight: 2
time: 15 minutes
---

* Splunk Helm chart を使用して K3s に OpenTelemetry Collector をインストールします
* Kubernetes Navigator でクラスターを確認します

---

## 1. Helm を使用したインストール

Splunk Helm chart を使用して OpenTelemetry Collector をインストールします。まず、Splunk Helm chart リポジトリを Helm に追加して更新します

{{< tabs >}}
{{% tab title="Helm Repo Add" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="Helm Repo Add Output" %}}
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
{{% /tab %}}
{{< /tabs >}}

以下のコマンドで OpenTelemetry Collector Helm chart をインストールします。このコマンドは編集**しないでください**

{{< tabs >}}
{{% tab title="Helm Install" %}}

```bash
helm install splunk-otel-collector --version {{< otel-version >}} \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml

```
<!--
``` bash
helm install splunk-otel-collector --version {{< otel-version >}} \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="environment=$INSTANCE-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```
-->
{{% /tab %}}
{{% tab title="Helm Install Output" %}}

``` text
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
NAME: splunk-otel-collector
LAST DEPLOYED: Fri May  7 11:19:01 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

{{% /tab %}}
{{< /tabs >}}

`kubectl get pods` を実行してデプロイの進行状況を監視できます。通常、約30秒後に新しい Pod が起動して実行中と表示されます。

続行する前に、ステータスが Running と表示されていることを確認してください。

{{< tabs >}}
{{% tab title="Kubectl Get Pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Kubectl Get Pods Output" %}}

``` text
NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-2sk6k                             0/1     Running   0          10s
splunk-otel-collector-k8s-cluster-receiver-6956d4446f-gwnd7   0/1     Running   0          10s
```

{{% /tab %}}
{{< /tabs >}}

OpenTelemetry Collector Pod のログを確認して、エラーがないことを確認します。出力は以下の Output タブに表示されているログ出力と同様になるはずです。

`helm` インストールで設定されたラベルを使用してログを確認します（終了するには `ctrl+c` を押す必要があります）。または、インストール済みの `k9s` ターミナル UI を使用してみましょう！

{{< tabs >}}
{{% tab title="Kubectl Logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector
```

{{% /tab %}}
{{% tab title="Kubectl Logs Output" %}}
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
{{% /tab %}}
{{< /tabs >}}

{{% notice title="インストールに失敗した場合の削除" style="info" %}}
OpenTelemetry Collector のインストールでエラーが発生した場合は、以下のコマンドでインストールを削除してやり直すことができます

``` sh
helm delete splunk-otel-collector
```

{{% /notice %}}

---

## 2. UI でメトリクスを検証する

Splunk UI で、左下の **>>** をクリックし、**Infrastructure** をクリックします。

![Selecting the Kubernetes Navigator Map](../images/clustermap-nav.png)

**Containers** の下にある **Kubernetes** をクリックして Kubernetes Navigator Cluster Map を開き、メトリクスが送信されていることを確認します。

クラスターが検出され、報告されていることを確認します（ワークショップでは他の多くのクラスターも表示されます）。クラスター名を確認するには、以下のコマンドを実行して出力をクリップボードにコピーしてください

{{% tab title="Echo Cluster Name" %}}

```bash
echo $INSTANCE-k3s-cluster
```

{{% /tab %}}

次に、UI で Splunk ロゴのすぐ下にある「Cluster: - 」メニューをクリックし、コピーしたクラスター名を検索ボックスに貼り付け、ボックスをクリックしてクラスターを選択し、最後にメニューの外の空白部分をクリックしてフィルターを適用します。

![K8S Clusters Filter](../images/search-k3s-cluster.png)

![Select K8S Cluster](../images/selecting-k3s-cluster.png)

![Filtered K8S Cluster](../images/filtered-k3s-cluster.png)

ノードの状態を確認するには、クラスターの薄い青色の背景にカーソルを合わせ、左上隅に表示される青い虫眼鏡 ![Magnifying Glass](../images/blue-cross.png?classes=inline&height=25px) をクリックします。

これによりノードレベルにドリルダウンします。次に、サイドバーボタンをクリックして Metrics サイドバーを開きます。

サイドバーが開いたら、スライダーを使用してクラスター/ノードに関連するさまざまなチャート（CPU、Memory、Network、Events など）を確認できます。

![Sidebar metrics](../images/explore-metrics.png)
