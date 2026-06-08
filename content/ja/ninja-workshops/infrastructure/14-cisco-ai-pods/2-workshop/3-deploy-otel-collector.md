---
title: OpenTelemetry Collector のデプロイ
linkTitle: 3. OpenTelemetry Collector のデプロイ
weight: 3
time: 10 minutes
---

このセクションでは、OpenShift ネームスペースに OpenTelemetry Collector をデプロイします。これにより、クラスター内で実行されているインフラストラクチャやアプリケーションからメトリクス、ログ、トレースを収集し、Splunk Observability Cloud にデータを送信します。

## OpenTelemetry Collector のデプロイ

### Helm がインストールされていることを確認する

以下のコマンドを実行して、Helm がインストールされていることを確認します

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

インストールされていない場合は、以下のコマンドを実行します

``` bash
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### Splunk OpenTelemetry Collector Helm Chart の追加

Splunk OpenTelemetry Collector for Kubernetes の Helm chart リポジトリを追加します

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

リポジトリが最新であることを確認します

```bash
helm repo update
````

### 環境変数の設定

Collector がデータを送信する Splunk 環境を設定するために、環境変数を設定します

``` bash
export USER_NAME=workshop-participant-$PARTICIPANT_NUMBER
export CLUSTER_NAME=ai-pod-$USER_NAME
export ENVIRONMENT_NAME=ai-pod-$USER_NAME
export SPLUNK_INDEX=splunk4rookies-workshop
```

環境名が設定されていることを確認します

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

### Collector のデプロイ

ワークショップディレクトリに移動します

``` bash
cd ~/workshop/cisco-ai-pods
```

次に、以下のコマンドを使用して、ネームスペースに Collector をインストールします

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

> Note: `Missing variables` というエラーが表示された場合は、環境変数を再定義する必要があります。以下のコマンドを実行する前に、参加者番号を追加してください
>
> ``` bash
> export PARTICIPANT_NUMBER=<your participant number>
> export USER_NAME=workshop-participant-$PARTICIPANT_NUMBER
> export CLUSTER_NAME=ai-pod-$USER_NAME
> export ENVIRONMENT_NAME=ai-pod-$USER_NAME
> export SPLUNK_INDEX=splunk4rookies-workshop
> ```

以下のコマンドを実行して、Collector の Pod が実行中であることを確認します

````
watch -n 1 oc get pods

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-58rwm                             1/1     Running   0          6m40s
splunk-otel-collector-agent-8dndr                             1/1     Running   0          6m40s
````

> Note: OpenShift 環境では、Collector が起動して `Running` 状態に遷移するまで約3分かかります。

### Splunk Observability Cloud で Collector データを確認する

**Splunk Observability Cloud** でクラスターが表示されることを確認します。**Infrastructure Monitoring** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、`k8s.cluster.name` にクラスター名（例`ai-pod-workshop-participant-1`）でフィルターを追加します

![Kubernetes Pods](../../images/KubernetesPods.png)
