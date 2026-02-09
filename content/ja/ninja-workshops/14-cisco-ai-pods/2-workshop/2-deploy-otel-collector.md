---
title: OpenTelemetry Collector のデプロイ
linkTitle: 2. OpenTelemetry Collector のデプロイ
weight: 2
time: 10 minutes
---

このセクションでは、OpenShift の名前空間に OpenTelemetry Collector をデプロイします。
OpenTelemetry Collector は、クラスター内で実行されているインフラストラクチャとアプリケーションからメトリクス、ログ、トレースを収集し、
結果のデータを Splunk Observability Cloud に送信します。

## OpenTelemetry Collector のデプロイ


Helm がインストールされていることを確認します:

``` bash
helm version
```

以下のような出力が返されるはずです:

````
version.BuildInfo{Version:"v3.19.4", GitCommit:"7cfb6e486dac026202556836bb910c37d847793e", GitTreeState:"clean", GoVersion:"go1.24.11"}
````

インストールされていない場合は、以下のコマンドを実行します:

``` bash
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

Splunk OpenTelemetry Collector for Kubernetes の Helm チャートリポジトリを追加します:

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

リポジトリが最新であることを確認します:

```bash
helm repo update
````

`./otel-collector/otel-collector-values.yaml` という名前のファイルを確認します。
このファイルを使用して OpenTelemetry Collector をインストールします。

Collector がデータを送信する Splunk 環境を設定するための環境変数を設定します:

> 注: 以下のコマンドを実行する前に、ワークショップ参加者番号を追加してください

``` bash
export USER_NAME=workshop-participant-<number>
export CLUSTER_NAME=ai-pod-$USER_NAME
export ENVIRONMENT_NAME=ai-pod-$USER_NAME
export SPLUNK_INDEX=splunk4rookies-workshop
```

ワークショップのディレクトリに移動します:

``` bash
cd ~/workshop/cisco-ai-pods
```

次に、以下のコマンドを使用して名前空間に Collector をインストールします:

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

以下のコマンドを実行して、Collector の Pod が実行中であることを確認します:

````
oc get pods

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-58rwm                             1/1     Running   0          6m40s
splunk-otel-collector-agent-8dndr                             1/1     Running   0          6m40s
````

Splunk Observability Cloud でクラスターが表示されることを確認します。
Infrastructure Monitoring -> Kubernetes -> Kubernetes Clusters に移動し、
クラスター名でフィルタリングします:

![Kubernetes Pods](../../images/KubernetesPods.png)
