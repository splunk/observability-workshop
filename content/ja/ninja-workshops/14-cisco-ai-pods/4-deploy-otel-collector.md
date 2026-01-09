---
title: OpenTelemetry Collectorのデプロイ
linkTitle: 4. OpenTelemetry Collectorのデプロイ
weight: 4
time: 10 minutes
---

OpenShiftクラスターが起動して実行されたので、OpenTelemetry Collectorをデプロイしましょう。これは、クラスター内で実行されているインフラストラクチャとアプリケーションからメトリクス、ログ、トレースを収集し、結果のデータをSplunk Observability Cloudに送信します。

## OpenTelemetry Collectorのデプロイ

まず、コレクター用の新しいプロジェクトを作成し、そのプロジェクトに切り替えます：

```bash
oc new-project otel
```

Helmがインストールされていることを確認します：

``` bash
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

Splunk OpenTelemetry Collector for KubernetesのHelmチャートリポジトリを追加します：

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

リポジトリが最新であることを確認します：

```bash
helm repo update
````

`./otel-collector/otel-collector-values.yaml`というファイルを確認してください。OpenTelemetry Collectorのインストールに使用します。

コレクターがデータを送信するSplunk環境を設定するための環境変数を設定します：

``` bash
export ENVIRONMENT_NAME=<which environment to send data to for Splunk Observability Cloud>
export SPLUNK_ACCESS_TOKEN=<your access token for Splunk Observability Cloud>
export SPLUNK_REALM=<your realm for Splunk Observability Cloud i.e. us0, us1, eu0, etc.>
export SPLUNK_HEC_URL=<HEC endpoint to send logs to Splunk platform i.e. https://<hostname>:443/services/collector/event>
export SPLUNK_HEC_TOKEN=<HEC token to send logs to Splunk platform>
export SPLUNK_INDEX=<name of index to send logs to in Splunk platform>
```

次に、以下のコマンドを使用してコレクターをインストールします：

```bash
helm install splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$SPLUNK_ACCESS_TOKEN" \
  --set="splunkObservability.realm=$SPLUNK_REALM" \
  --set="splunkPlatform.endpoint=$SPLUNK_HEC_URL" \
  --set="splunkPlatform.token=$SPLUNK_HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./otel-collector/otel-collector-values.yaml \
  -n otel \
  splunk-otel-collector-chart/splunk-otel-collector
```

以下のコマンドを実行して、すべてのコレクターPodが実行されていることを確認します：

````
oc get pods

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-58rwm                             1/1     Running   0          6m40s
splunk-otel-collector-agent-8dndr                             1/1     Running   0          6m40s
splunk-otel-collector-k8s-cluster-receiver-7b7f5cdc5b-rhxsj   1/1     Running   0          6m40s
````

Splunk Observability Cloudでクラスターが表示されることを確認します。Infrastructure Monitoring -> Kubernetes -> Kubernetes Podsに移動し、クラスター名でフィルタリングしてください：

![Kubernetes Pods](../images/KubernetesPods.png)