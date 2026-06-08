---
title: 複雑な環境のデプロイとメトリクスの収集
linkTitle: 2. デプロイ
weight: 2
---

**目的:** Kafka や MongoDB などの複雑なインフラストラクチャコンポーネントを効率的にデプロイし、Splunk O11y IM インテグレーションによるメトリクス収集をデモンストレーションする方法を学びます

**所要時間**: 15分

## シナリオ

見込み客が環境内で Kafka と MongoDB を使用しています。これらのサービスにはインテグレーションが存在するため、見込み客にデモンストレーションしたいと考えています。これらのサービスを含むライブ環境をセットアップし、メトリクスを収集するための迅速かつ効率的な方法は何でしょうか？

### 1. Helm チャートはどこで見つけられますか？

- Google で「myservice helm chart」を検索します
- `https://artifacthub.io/` (**注意:** 信頼できる組織が提供し、スター数が多く、頻繁に更新されているチャートを探してください)

### 2. [Apache Kafka packaged by Bitnami](https://github.com/bitnami/charts/tree/main/bitnami/kafka/#installing-the-chart) の確認

以下のオプションを有効にして Helm チャートをデプロイします

- `replicaCount=3`
- `metrics.jmx.enabled=true`
- `metrics.kafka.enabled=true`
- `deleteTopicEnable=true`

### 3. [MongoDB(R) packaged by Bitnami](https://github.com/bitnami/charts/tree/master/bitnami/mongodb/#installing-the-chart) の確認

以下のオプションを有効にして Helm チャートをデプロイします

- `version 12.1.31`
- `metrics.enabled=true`
- `global.namespaceOverride=default`
- `auth.rootUser=root`
- `auth.rootPassword=splunk`
- `auth.enabled=false`

### 4. Helm チャートで Kafka と MongoDB をインストールする

``` bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

``` bash
helm install kafka --set replicaCount=3 --set metrics.jmx.enabled=true --set metrics.kafka.enabled=true  --set deleteTopicEnable=true bitnami/kafka
```

``` bash
helm install mongodb --set metrics.enabled=true bitnami/mongodb --set global.namespaceOverride=default --set auth.rootUser=root --set auth.rootPassword=splunk --set auth.enabled=false --version 12.1.31
```

Helm チャートのインストールを確認します

{{< tabs >}}
{{% tab title="helm list" %}}

```bash
helm list
```

{{% /tab %}}
{{% tab title="helm list output" %}}

``` text
NAME    NAMESPACE   REVISION    UPDATED                                 STATUS      CHART           APP VERSION
kafka   default     1           2022-11-14 11:21:36.328956822 -0800 PST deployed    kafka-19.1.3    3.3.1
mongodb default     1           2022-11-14 11:19:36.507690487 -0800 PST deployed    mongodb-12.1.31 5.0.10
```

{{% /tab %}}
{{< /tabs >}}

Helm チャートのインストールを確認します

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="kubectl get pods Output" %}}

``` text
NAME                              READY   STATUS              RESTARTS   AGE
kafka-exporter-595778d7b4-99ztt   0/1     ContainerCreating   0          17s
mongodb-b7c968dbd-jxvsj           0/2     Pending             0          6s
kafka-1                           0/2     ContainerCreating   0          16s
kafka-2                           0/2     ContainerCreating   0          16s
kafka-zookeeper-0                 0/1     Pending             0          17s
kafka-0                           0/2     Pending             0          17s
```

{{% /tab %}}
{{< /tabs >}}

各 Helm チャートと Splunk O11y Data Setup の情報を使用して、Kafka と MongoDB からメトリクスを収集するための values.yaml を生成します。

{{% notice title="Note" style="info" %}}
各サービスの `values.yaml` は、Splunk Helm Chart のインストール時に渡されます。これにより、OTEL コレクターがこれらのサービスからメトリクスを収集するように設定されます。
{{% /notice %}}

- 参考資料:
  - [Apache Kafka packaged by Bitnami](https://github.com/bitnami/charts/tree/master/bitnami/spark/#installing-the-chart)
  - [Configure application receivers for databases » Apache Kafka](https://docs.splunk.com/Observability/gdi/kafka/kafka.html)
  - [Kafkametricsreceiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/kafkametricsreceiver)

#### 4.1 kafka.values.yaml の例

``` yaml
otelAgent:
config:
    receivers:
    receiver_creator:
        receivers:
        smartagent/kafka:
            rule: type == "pod" && name matches "kafka"
            config:
                    #endpoint: '`endpoint`:5555'
            port: 5555
            type: collectd/kafka
            clusterName: sl-kafka
otelK8sClusterReceiver:
k8sEventsEnabled: true
config:
    receivers:
    kafkametrics:
        brokers: kafka:9092
        protocol_version: 2.0.0
        scrapers:
        - brokers
        - topics
        - consumers
    service:
    pipelines:
        metrics:
        receivers:
                #- prometheus
        - k8s_cluster
        - kafkametrics
```

#### 4.2 mongodb.values.yaml の例

``` yaml
otelAgent:
    config:
        receivers:
        receiver_creator:
            receivers:
            smartagent/mongodb:
                rule: type == "pod" && name matches "mongo"
                config:
                type: collectd/mongodb
                host: mongodb.default.svc.cluster.local
                port: 27017
                databases: ["admin", "O11y", "local", "config"]
                sendCollectionMetrics: true
                sendCollectionTopMetrics: true
```

#### 4.3 zookeeper.values.yaml の例

``` yaml
otelAgent:
    config:
        receivers:
        receiver_creator:
            receivers:
            smartagent/zookeeper:
                rule: type == "pod" && name matches "kafka-zookeeper"
                config:
                type: collectd/zookeeper
                host: kafka-zookeeper
                port: 2181
```

### 5. Splunk OTEL Helm チャートをインストールする

``` bash
cd /home/splunk/realtime_enrichment/otel_yamls/ 

helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

helm repo update
```

``` bash
helm install --set provider=' ' --set distro=' ' --set splunkObservability.accessToken=$ACCESS_TOKEN --set clusterName=$clusterName --set splunkObservability.realm=$REALM --set otelCollector.enabled='false' --set gateway.enabled='false' --values kafka.values.yaml --values mongodb.values.yaml --values zookeeper.values.yaml --values alwayson.values.yaml --values k3slogs.yaml --generate-name splunk-otel-collector-chart/splunk-otel-collector
```

### 6. インストールの確認

Kafka、MongoDB、および Splunk OTEL Collector の Helm チャートがインストールされていることを確認します。名前が異なる場合があることに注意してください。

{{< tabs >}}
{{% tab title="helm list" %}}

``` bash
helm list
```

{{% /tab %}}
{{% tab title="helm list Output" %}}

``` text
NAME                                NAMESPACE   REVISION    UPDATED                                 STATUS      CHART                           APP VERSION
kafka                               default     1           2021-12-07 12:48:47.066421971 -0800 PST deployed    kafka-14.4.1                    2.8.1
mongodb                             default     1           2021-12-07 12:49:06.132771625 -0800 PST deployed    mongodb-10.29.2                 4.4.10
splunk-otel-collector-1638910184    default     1           2021-12-07 12:49:45.694013749 -0800 PST deployed    splunk-otel-collector-0.37.1    0.37.1
```

{{% /tab %}}
{{< /tabs >}}

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="kubectl get pods Output" %}}

``` text
NAME                                                              READY   STATUS    RESTARTS   AGE
kafka-zookeeper-0                                                 1/1     Running   0          18m
kafka-2                                                           2/2     Running   1          18m
mongodb-79cf87987f-gsms8                                          2/2     Running   0          18m
kafka-1                                                           2/2     Running   1          18m
kafka-exporter-7c65fcd646-dvmtv                                   1/1     Running   3          18m
kafka-0                                                           2/2     Running   1          18m
splunk-otel-collector-1638910184-agent-27s5c                      2/2     Running   0          17m
splunk-otel-collector-1638910184-k8s-cluster-receiver-8587qmh9l   1/1     Running   0          17m
```

{{% /tab %}}
{{< /tabs >}}

### 7. ダッシュボードの確認

Kafka、MongoDB、および Zookeeper のすぐに使えるダッシュボードが Infrastructure Monitor のランディングページに表示されていることを確認します。各コンポーネントにドリルダウンして、各サービスの詳細情報を表示します。

> [!TIP]
> フィルター `k8s.cluster.name` にクラスター名を指定して、ご自身のインスタンスを見つけることができます。

- Infrastructure Monitoring ランディングページ:

![IM-landing-page](../images/inframon.jpg)

- K8 Navigator:

![k8-navigator](../images/k8navigator.jpg)

- MongoDB Dashboard:

![mongodb-dash](../images/mongoDB.jpg)

- Kafka Dashboard:

![kafka-dash](../images/kafka.jpg)
