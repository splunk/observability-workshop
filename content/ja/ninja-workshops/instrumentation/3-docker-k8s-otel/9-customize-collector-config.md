---
title: OpenTelemetry Collector設定のカスタマイズ
linkTitle: 9. OpenTelemetry Collector設定のカスタマイズ
weight: 9
time: 20 minutes
---

K8sクラスターにSplunk Distribution of the OpenTelemetry Collectorをデフォルト設定でデプロイしました。このセクションでは、Collector設定をカスタマイズする方法をいくつかの例を通して説明します。

## Collector設定の確認

Collector設定をカスタマイズする前に、現在の設定がどのようになっているか確認する方法を見てみましょう。

Kubernetes環境では、Collector設定はConfig Mapを使用して保存されます。

クラスター内に存在するConfig Mapを以下のコマンドで確認できます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get cm -l app=splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                 DATA   AGE
splunk-otel-collector-otel-k8s-cluster-receiver   1      3h37m
splunk-otel-collector-otel-agent                  1      3h37m
```

{{% /tab %}}
{{< /tabs >}}

> なぜConfig Mapが2つあるのでしょうか？

次に、Collector AgentのConfig Mapを以下のように表示できます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Name:         splunk-otel-collector-otel-agent
Namespace:    default
Labels:       app=splunk-otel-collector
              app.kubernetes.io/instance=splunk-otel-collector
              app.kubernetes.io/managed-by=Helm
              app.kubernetes.io/name=splunk-otel-collector
              app.kubernetes.io/version=0.136.1
              chart=splunk-otel-collector-0.136.0
              helm.sh/chart=splunk-otel-collector-0.136.0
              release=splunk-otel-collector
Annotations:  meta.helm.sh/release-name: splunk-otel-collector
              meta.helm.sh/release-namespace: default

Data
====
relay:
----
exporters:
  otlphttp:
    auth:
      authenticator: headers_setter
    metrics_endpoint: https://ingest.us1.signalfx.com/v2/datapoint/otlp
    traces_endpoint: https://ingest.us1.signalfx.com/v2/trace/otlp
    (followed by the rest of the collector config in yaml format) 
```

{{% /tab %}}
{{< /tabs >}}

## K8sでのCollector設定の更新方法

以前のLinuxインスタンスでCollectorを実行した例では、Collector設定は `/etc/otel/collector/agent_config.yaml` ファイルに保存されていました。その場合、Collector設定を変更するには、このファイルを編集して保存し、Collectorを再起動するだけでした。

K8sでは少し異なる方法で行います。`agent_config.yaml` を直接変更する代わりに、Helmチャートのデプロイに使用する `values.yaml` ファイルを変更してCollector設定をカスタマイズします。

[GitHub](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/helm-charts/splunk-otel-collector/values.yaml)にあるvalues.yamlファイルに、利用可能なカスタマイズオプションが記載されています。

例を見てみましょう。

## インフラストラクチャイベントモニタリングの追加

最初の例として、K8sクラスターのインフラストラクチャイベントモニタリングを有効にしましょう。

> これにより、チャートのEvents Feedセクションの一部としてKubernetesイベントを確認できるようになります。
> クラスターReceiverは、kubernetes-eventsモニターを使用するSmart Agent Receiverで設定され、カスタムイベントを送信します。詳細は [Collect Kubernetes events](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-kubernetes/kubernetes-config-logs.html#collect-kubernetes-events) を参照してください。

`values.yaml` ファイルに以下の行を追加します。

> ヒント: viでの開き方と保存方法は前のステップを参照してください。

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
...
```

ファイルを保存したら、以下のコマンドで変更を適用します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm upgrade splunk-otel-collector \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=otel-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Release "splunk-otel-collector" has been upgraded. Happy Helming!
NAME: splunk-otel-collector
LAST DEPLOYED: Fri Dec 20 01:17:03 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

次に、Config Mapを表示して変更が適用されたことを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl describe cm splunk-otel-collector-otel-k8s-cluster-receiver
```

{{% /tab %}}
{{% tab title="Example Output" %}}

`smartagent/kubernetes-events` がAgent設定に含まれていることを確認します。

``` bash
  smartagent/kubernetes-events:
    alwaysClusterReporter: true
    type: kubernetes-events
    whitelistedEvents:
    - involvedObjectKind: Pod
      reason: Created
    - involvedObjectKind: Pod
      reason: Unhealthy
    - involvedObjectKind: Pod
      reason: Failed
    - involvedObjectKind: Job
      reason: FailedCreate
```

{{% /tab %}}
{{< /tabs >}}

> 注意: これらの変更はクラスターReceiverのConfig Mapに適用されるため、クラスターReceiverのConfig Mapを指定しています。

## Debug Exporterの追加

Collectorに送信されるトレースとログを確認し、Splunkに送信する前に内容を検査したい場合があります。この目的にはDebug Exporterを使用できます。これはOpenTelemetry関連の問題のトラブルシューティングに役立ちます。

values.yamlファイルの末尾にDebug Exporterを以下のように追加します。

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers:
     ...
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - debug
        logs:
          exporters:
            - debug
```

ファイルを保存したら、以下のコマンドで変更を適用します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm upgrade splunk-otel-collector \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=otel-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Release "splunk-otel-collector" has been upgraded. Happy Helming!
NAME: splunk-otel-collector
LAST DEPLOYED: Fri Dec 20 01:32:03 2024
NAMESPACE: default
STATUS: deployed
REVISION: 3
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

curlを使用してアプリケーションを数回実行し、以下のコマンドでAgent Collectorのログをtailします。

``` bash
kubectl logs -l component=otel-collector-agent -f
```

Agent Collectorのログに以下のようなトレースが出力されます。

````
2024-12-20T01:43:52.929Z info Traces {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 2}
2024-12-20T01:43:52.929Z info ResourceSpans #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> splunk.distro.version: Str(1.8.0)
     -> telemetry.distro.name: Str(splunk-otel-dotnet)
     -> telemetry.distro.version: Str(1.8.0)
     -> os.type: Str(linux)
     -> os.description: Str(Debian GNU/Linux 12 (bookworm))
     -> os.build_id: Str(6.8.0-1021-aws)
     -> os.name: Str(Debian GNU/Linux)
     -> os.version: Str(12)
     -> host.name: Str(derek-1)
     -> process.owner: Str(app)
     -> process.pid: Int(1)
     -> process.runtime.description: Str(.NET 8.0.11)
     -> process.runtime.name: Str(.NET)
     -> process.runtime.version: Str(8.0.11)
     -> container.id: Str(78b452a43bbaa3354a3cb474010efd6ae2367165a1356f4b4000be031b10c5aa)
     -> telemetry.sdk.name: Str(opentelemetry)
     -> telemetry.sdk.language: Str(dotnet)
     -> telemetry.sdk.version: Str(1.9.0)
     -> service.name: Str(helloworld)
     -> deployment.environment: Str(otel-derek-1)
     -> k8s.pod.ip: Str(10.42.0.15)
     -> k8s.pod.labels.app: Str(helloworld)
     -> k8s.pod.name: Str(helloworld-84865965d9-nkqsx)
     -> k8s.namespace.name: Str(default)
     -> k8s.pod.uid: Str(38d39bc6-1309-4022-a569-8acceef50942)
     -> k8s.node.name: Str(derek-1)
     -> k8s.cluster.name: Str(derek-1-cluster)
````

また、以下のようなログエントリも表示されます。

````
2024-12-20T01:43:53.215Z info Logs {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 2}
2024-12-20T01:43:53.215Z info ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> splunk.distro.version: Str(1.8.0)
     -> telemetry.distro.name: Str(splunk-otel-dotnet)
     -> telemetry.distro.version: Str(1.8.0)
     -> os.type: Str(linux)
     -> os.description: Str(Debian GNU/Linux 12 (bookworm))
     -> os.build_id: Str(6.8.0-1021-aws)
     -> os.name: Str(Debian GNU/Linux)
     -> os.version: Str(12)
     -> host.name: Str(derek-1)
     -> process.owner: Str(app)
     -> process.pid: Int(1)
     -> process.runtime.description: Str(.NET 8.0.11)
     -> process.runtime.name: Str(.NET)
     -> process.runtime.version: Str(8.0.11)
     -> container.id: Str(78b452a43bbaa3354a3cb474010efd6ae2367165a1356f4b4000be031b10c5aa)
     -> telemetry.sdk.name: Str(opentelemetry)
     -> telemetry.sdk.language: Str(dotnet)
     -> telemetry.sdk.version: Str(1.9.0)
     -> service.name: Str(helloworld)
     -> deployment.environment: Str(otel-derek-1)
     -> k8s.node.name: Str(derek-1)
     -> k8s.cluster.name: Str(derek-1-cluster)
````

しかし、Splunk Observability Cloudに戻ると、アプリケーションからトレースとログが送信されなくなっていることに気づくでしょう。

なぜそうなったのでしょうか？次のセクションで確認しましょう。
