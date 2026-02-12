---
title: OpenTelemetry Collector のデプロイ
linkTitle: 3. OpenTelemetry Collector のデプロイ
weight: 3
time: 10 minutes
---

このセクションでは、OpenShift の Namespace に OpenTelemetry Collector をデプロイします。
Collector は、クラスター内で動作するインフラストラクチャとアプリケーションからメトリクス、ログ、トレースを収集し、結果のデータを Splunk Observability Cloud に送信します。

## OpenTelemetry Collector のデプロイ

### Helm がインストールされていることを確認する

以下のコマンドを実行して、Helm がインストールされていることを確認します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
helm version
```

{{% /tab %}}
{{% tab title="出力例" %}}

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

### Splunk OpenTelemetry Collector Helm Chart の追加

Splunk OpenTelemetry Collector for Kubernetes の Helm chart リポジトリを追加します。

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

リポジトリが最新であることを確認します。

```bash
helm repo update
````

### 環境変数の設定

Collector がデータを送信する Splunk 環境を設定するための環境変数を設定します。

``` bash
export USER_NAME=workshop-participant-$PARTICIPANT_NUMBER
export CLUSTER_NAME=ai-pod-$USER_NAME
export ENVIRONMENT_NAME=ai-pod-$USER_NAME
export SPLUNK_INDEX=splunk4rookies-workshop
```

### Collector のデプロイ

ワークショップディレクトリに移動します。

``` bash
cd ~/workshop/cisco-ai-pods
```

以下のコマンドを使用して、自分の Namespace に Collector をインストールします。

```bash
helm install splunk-otel-collector \
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

> Collector のインストール時に `otel-collector-values.yaml` という設定ファイルを参照していることに注意してください。このファイルにはカスタム設定が含まれています。

以下のコマンドを実行して、Collector の Pod が実行中であることを確認します。

````
oc get pods

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-58rwm                             1/1     Running   0          6m40s
splunk-otel-collector-agent-8dndr                             1/1     Running   0          6m40s
````

> 注意: OpenShift 環境では、Collector が起動して `Running` 状態に移行するまで約 3 分かかります。

### Splunk Observability Cloud で Collector データを確認する

**Splunk Observability Cloud** で自分のクラスターが表示されることを確認します。**Infrastructure Monitoring** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、`k8s.cluster.name` にクラスター名（例: `ai-pod-workshop-participant-1`）でフィルターを追加します。

![Kubernetes Pods](../../images/KubernetesPods.png)
