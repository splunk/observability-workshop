---
title: OpenTelemetryコレクター設定のカスタマイズ
linkTitle: 9. OpenTelemetryコレクター設定のカスタマイズ
weight: 9
time: 20 minutes
---

デフォルト設定を使用してK8sクラスターにSplunk Distribution of OpenTelemetryコレクターを
デプロイしました。このセクションでは、コレクター設定をカスタマイズする方法をいくつかの例で
説明します。

## コレクター設定の取得

コレクター設定をカスタマイズする前に、現在の設定がどのようになっているかを
どのように確認するのでしょうか？

Kubernetes環境では、コレクター設定はConfig Mapを使用して保存されます。

以下のコマンドで、クラスターに存在するconfig mapを確認できます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl get cm -l app=splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
NAME                                                 DATA   AGE
splunk-otel-collector-otel-k8s-cluster-receiver   1      3h37m
splunk-otel-collector-otel-agent                  1      3h37m
```

{{% /tab %}}
{{< /tabs >}}

> なぜ 2 つの config map があるのでしょうか？

次に、以下のようにコレクターエージェントのconfig mapを表示できます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe cm splunk-otel-collector-otel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
Name:         splunk-otel-collector-otel-agent
Namespace:    default
Labels:       app=splunk-otel-collector
              app.kubernetes.io/instance=splunk-otel-collector
              app.kubernetes.io/managed-by=Helm
              app.kubernetes.io/name=splunk-otel-collector
              app.kubernetes.io/version=0.113.0
              chart=splunk-otel-collector-0.113.0
              helm.sh/chart=splunk-otel-collector-0.113.0
              heritage=Helm
              release=splunk-otel-collector
Annotations:  meta.helm.sh/release-name: splunk-otel-collector
              meta.helm.sh/release-namespace: default

Data
====
relay:
----
exporters:
  otlphttp:
    headers:
      X-SF-Token: ${SPLUNK_OBSERVABILITY_ACCESS_TOKEN}
    metrics_endpoint: https://ingest.us1.signalfx.com/v2/datapoint/otlp
    traces_endpoint: https://ingest.us1.signalfx.com/v2/trace/otlp
    (followed by the rest of the collector config in yaml format)
```

{{% /tab %}}
{{< /tabs >}}

## K8s でコレクター設定を更新する方法

Linuxインスタンスでコレクターを実行した以前の例では、コレクター設定は
`/etc/otel/collector/agent_config.yaml` ファイルで利用可能でした。その場合にコレクター設定を
変更する必要があれば、単純にこのファイルを編集し、変更を保存してから
コレクターを再起動すればよかったのです。

K8sでは、少し異なる動作をします。`agent_config.yaml` を直接変更する代わりに、
helmチャートをデプロイするために使用される `values.yaml` ファイルを変更することで
コレクター設定をカスタマイズします。

[GitHub](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/helm-charts/splunk-otel-collector/values.yaml)のvalues.yamlファイルには、
利用可能なカスタマイズオプションが記載されています。

例を見てみましょう。

## Infrastructure Events Monitoring の追加

最初の例として、K8sクラスターのinfrastructure events monitoringを有効にしましょう。

> これにより、charts の Events Feed セクションの一部として Kubernetes イベントを確認できるようになります。
> cluster receiver は、kubernetes-events
> monitor を使用して Smart Agent receiver で設定され、custom イベントを送信します。詳細については[Collect Kubernetes events](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-kubernetes/kubernetes-config-logs.html#collect-kubernetes-events)を参照してください。

これは `values.yaml` ファイルに以下の行を追加することで実行されます：

> ヒント：vi での開き方と保存方法は前のステップにあります。

```yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
```

ファイルが保存されたら、以下のコマンドで変更を適用できます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
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

```bash
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

その後、config mapを表示して変更が適用されたことを確認できます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe cm splunk-otel-collector-otel-k8s-cluster-receiver
```

{{% /tab %}}
{{% tab title="Example Output" %}}

`smartagent/kubernetes-events` がagent configに含まれていることを確認してください：

```bash
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

> これらの特定の変更が適用されるのは
> cluster receiver config map なので、そちらを指定していることに注意してください。

## Debug Exporter の追加

collectorに送信されるtraceとlogを確認して、
Splunkに送信する前に検査したいとします。この目的のためにdebug exporterを使用できます。これは
OpenTelemetry関連の問題のトラブルシューティングに役立ちます。

values.yamlファイルの下部に以下のようにdebug exporterを追加しましょう：

```yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers: ...
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

ファイルが保存されたら、以下のコマンドで変更を適用できます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
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

```bash
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

curlを使用してアプリケーションを数回実行してから、以下のコマンドでagent collectorのlogをtailします：

```bash
kubectl logs -l component=otel-collector-agent -f
```

以下のようなtraceがagent collectorのlogに書き込まれているのが確認できるはずです：

```
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
```

そして以下のようなlogエントリも確認できます：

```
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
```

ただし、Splunk Observability Cloudに戻ると、アプリケーションからtraceとlogが
もはやそこに送信されていないことに気づくでしょう。

なぜそうなったと思いますか？次のセクションで詳しく説明します。
