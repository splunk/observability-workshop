---
title: OpenTelemetry Collectorのデプロイ
linkTitle: 3. OpenTelemetry Collectorのデプロイ
weight: 3
time: 10 minutes
---

このセクションでは、OpenShift名前空間にOpenTelemetry Collectorをデプロイします。Collectorはクラスター内で実行されているインフラストラクチャとアプリケーションからメトリクス、ログ、トレースを収集し、Splunk Observability Cloudにデータを送信します。

## OpenTelemetry Collectorのデプロイ

### Helmがインストールされていることを確認

以下のコマンドを実行して、Helmがインストールされていることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm version
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
version.BuildInfo{Version:"v3.19.4", GitCommit:"7cfb6e486dac026202556836bb910c37d847793e", GitTreeState:"clean", GoVersion:"go1.24.11"}
```

{{% /tab %}}
{{< /tabs >}}

インストールされていない場合は、以下のコマンドを実行します。

``` bash
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### Splunk OpenTelemetry Collector Helm Chartの追加

Splunk OpenTelemetry Collector for KubernetesのHelm Chartリポジトリを追加します。

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

リポジトリが最新であることを確認します。

```bash
helm repo update
````

### 環境変数の設定

Collectorがデータを送信するSplunk環境を設定するための環境変数を設定します。

``` bash
export USER_NAME=workshop-participant-$PARTICIPANT_NUMBER
export CLUSTER_NAME=ai-pod-$USER_NAME
export ENVIRONMENT_NAME=ai-pod-$USER_NAME
export SPLUNK_INDEX=splunk4rookies-workshop
```

環境名が設定されていることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
echo $ENVIRONMENT_NAME
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
ai-pod-workshop-participant-1
```

{{% /tab %}}
{{< /tabs >}}

### Collectorのデプロイ

ワークショップディレクトリに移動します。

``` bash
cd ~/workshop/cisco-ai-pods
```

次に、以下のコマンドを使用して名前空間にCollectorをインストールします。

```bash
{ [ -z "$CLUSTER_NAME" ] || \
  [ -z "$ENVIRONMENT_NAME" ] || \
  [ -z "$USER_NAME" ]; } && \
  echo "Error: Missing variables" || \
  helm upgrade --install splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./otel-collector/otel-collector-values.yaml \
  -n $USER_NAME \
  splunk-otel-collector-chart/splunk-otel-collector
```

> 注意: `Missing variables` というエラーが表示された場合は、環境変数を再度定義する必要があります。以下のコマンドを実行する前に、参加者番号を追加してください。
>
> ``` bash
> export PARTICIPANT_NUMBER=<your participant number>
> export USER_NAME=workshop-participant-$PARTICIPANT_NUMBER
> export CLUSTER_NAME=ai-pod-$USER_NAME
> export ENVIRONMENT_NAME=ai-pod-$USER_NAME
> export SPLUNK_INDEX=splunk4rookies-workshop
> ```

以下のコマンドを実行して、Collector Podが実行中であることを確認します。

````
watch -n 1 oc get pods

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-58rwm                             1/1     Running   0          6m40s
splunk-otel-collector-agent-8dndr                             1/1     Running   0          6m40s
````

> 注意: OpenShift環境では、Collectorが起動して `Running` 状態に遷移するまでに約3分かかります。

### Splunk Observability CloudでCollectorデータを確認

**Splunk Observability Cloud** でクラスターが表示されることを確認します。**Infrastructure Monitoring** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、`k8s.cluster.name` でクラスター名（例: `ai-pod-workshop-participant-1`）のフィルターを追加します。

![Kubernetes Pods](../../images/KubernetesPods.png)
