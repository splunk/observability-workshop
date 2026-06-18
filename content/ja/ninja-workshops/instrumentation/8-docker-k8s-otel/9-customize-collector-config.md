---
title: OpenTelemetry Collector 設定のカスタマイズ
linkTitle: 9. OpenTelemetry Collector 設定のカスタマイズ
weight: 9
time: 20 minutes
---

K8s クラスターにデフォルト設定で Splunk Distribution of the OpenTelemetry Collector をデプロイしました。このセクションでは、Collector の設定をカスタマイズする方法をいくつかの例を通して説明します。

## Collector 設定の確認

Collector の設定をカスタマイズする前に、現在の設定がどのようになっているかを確認するにはどうすればよいでしょうか？

Kubernetes 環境では、Collector の設定は Config Map を使用して保存されています。

クラスター内に存在する Config Map を確認するには、次のコマンドを使用します

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

> なぜ 2 つの Config Map があるのでしょうか？

次のコマンドで Collector エージェントの Config Map を表示できます

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

## K8s での Collector 設定の更新方法

Linux インスタンスで Collector を実行した前の例では、Collector の設定は `/etc/otel/collector/agent_config.yaml` ファイルにありました。その場合、Collector の設定を変更するには、このファイルを編集して保存し、Collector を再起動するだけでした。

K8s では少し異なる方法で動作します。`agent_config.yaml` を直接変更するのではなく、Helm チャートのデプロイに使用する `values.yaml` ファイルを変更することで Collector の設定をカスタマイズします。

[GitHub](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/helm-charts/splunk-otel-collector/values.yaml) にある values.yaml ファイルには、利用可能なカスタマイズオプションが記載されています。

例を見てみましょう。

## Infrastructure Events Monitoring の追加

最初の例として、K8s クラスターのインフラストラクチャイベント監視を有効にします。

> これにより、チャートの Events Feed セクションで Kubernetes イベントを確認できるようになります。
> クラスターレシーバーは、kubernetes-events モニターを使用した Smart Agent レシーバーで構成され、カスタムイベントを送信します。詳細については [Collect Kubernetes events](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-kubernetes/kubernetes-config-logs.html#collect-kubernetes-events) を参照してください。

これは `values.yaml` ファイルに次の行を追加することで実現します

> ヒント：vi でファイルを開いて保存する手順は前のステップにあります。

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
...
```

ファイルを保存したら、次のコマンドで変更を適用します

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

次に、Config Map を表示して変更が適用されたことを確認します

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl describe cm splunk-otel-collector-otel-k8s-cluster-receiver
```

{{% /tab %}}
{{% tab title="Example Output" %}}

エージェントの設定に `smartagent/kubernetes-events` が含まれていることを確認します

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

> これらの変更はクラスターレシーバーの Config Map に適用されるため、クラスターレシーバーの Config Map を指定していることに注意してください。

## Debug Exporter の追加

Collector に送信されるトレースとログを確認して、Splunk に送信する前に検査したいとします。この目的には debug exporter を使用できます。これは OpenTelemetry 関連の問題のトラブルシューティングに役立ちます。

values.yaml ファイルの末尾に次のように debug exporter を追加します

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

ファイルを保存したら、次のコマンドで変更を適用します

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

curl を使ってアプリケーションを数回実行し、次のコマンドでエージェント Collector のログを tail します

``` bash
kubectl logs -l component=otel-collector-agent -f
```

エージェント Collector のログに次のようなトレースが書き込まれているのが確認できるはずです

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

また、次のようなログエントリも確認できます

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

ただし、Splunk Observability Cloud に戻ると、アプリケーションからトレースとログが送信されなくなっていることに気づくでしょう。

なぜそうなったと思いますか？次のセクションで確認しましょう。
