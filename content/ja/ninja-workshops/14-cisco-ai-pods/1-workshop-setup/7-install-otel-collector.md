---
title: OpenTelemetry Collector のインストール
linkTitle: 7. OpenTelemetry Collector のインストール
weight: 7
time: 5 minutes
---

このセクションでは、clusterReceiver のみを有効にした OpenTelemetry Collector をインストールします（ワークショップ参加者は各自の Namespace に独自のエージェントをインストールするため）。その後、この Collector のインストールによって作成された ClusterRole を各ワークショップ参加者の Namespace にバインドします。

## OpenTelemetry Collector のインストール

まず、Collector 用の新しいプロジェクトを作成し、そのプロジェクトに切り替えます：

```bash
oc new-project admin-otel
```

Splunk OpenTelemetry Collector for Kubernetes の Helm チャートリポジトリを追加します：

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

リポジトリが最新であることを確認します：

```bash
helm repo update
````

`./admin-otel-collector/admin-otel-collector-values.yaml` というファイルを確認してください。このファイルを使用して OpenTelemetry Collector をインストールします。

Collector がデータを送信する Splunk 環境を設定するための環境変数を設定します：

``` bash
export CLUSTER_NAME=ai-pod-workshop-admin
export ENVIRONMENT_NAME=ai-pod-workshop-admin
export SPLUNK_ACCESS_TOKEN=<your access token for Splunk Observability Cloud>
export SPLUNK_REALM=<your realm for Splunk Observability Cloud i.e. us0, us1, eu0, etc.>
export SPLUNK_HEC_URL=<HEC endpoint to send logs to Splunk platform i.e. https://<hostname>:443/services/collector/event>
export SPLUNK_HEC_TOKEN=<HEC token to send logs to Splunk platform>
export SPLUNK_INDEX=splunk4rookies-workshop
```

次に、以下のコマンドを使用して Collector をインストールします：

```bash
helm install splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$SPLUNK_ACCESS_TOKEN" \
  --set="splunkObservability.realm=$SPLUNK_REALM" \
  --set="splunkPlatform.endpoint=$SPLUNK_HEC_URL" \
  --set="splunkPlatform.token=$SPLUNK_HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./admin-otel-collector/admin-otel-collector-values.yaml \
  -n admin-otel \
  splunk-otel-collector-chart/splunk-otel-collector
```

以下のコマンドを実行して、すべての Collector Pod が実行中であることを確認します：

````
oc get pods -n admin-otel

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-k8s-cluster-receiver-7b7f5cdc5b-rhxsj   1/1     Running   0          6m40s
````

## 各ワークショップ参加者用の Service Account の作成と Cluster Role へのバインド

``` bash
for i in {1..30}; do
  ns="workshop-participant-$i"

  oc get ns "$ns" >/dev/null 2>&1 || continue
  oc -n "$ns" create sa splunk-otel-collector 2>/dev/null || true

  oc apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: splunk-otel-collector-${ns}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: splunk-otel-collector
subjects:
- kind: ServiceAccount
  name: splunk-otel-collector
  namespace: ${ns}
EOF
done
```

また、各 Namespace の ServiceAccount に SecurityContextConstraint (SCC) を付与する必要があります：

``` bash
for i in {1..30}; do
  ns="workshop-participant-$i"
  oc get ns "$ns" >/dev/null 2>&1 || continue
  oc -n "$ns" adm policy add-scc-to-user splunk-otel-collector -z splunk-otel-collector
done
```
