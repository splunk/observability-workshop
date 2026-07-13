---
title: AI POD Dashboardの確認
linkTitle: 7. AI POD Dashboardの確認
weight: 7
time: 10 minutes
---

このセクションでは、Splunk Observability CloudのAI POD Dashboardを確認し、NVIDIA、Pure Storage、Weaviateからのデータが期待どおりに取得されていることを確認します。

## OpenTelemetry Collector設定の更新

以下のHelmコマンドを実行して、Collectorの設定変更を適用します。

``` bash
{ [ -z "$CLUSTER_NAME" ] || \
  [ -z "$ENVIRONMENT_NAME" ] || \
  [ -z "$USER_NAME" ]; } && \
  echo "Error: Missing variables" || \
  helm upgrade splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./otel-collector-values.yaml \
  -n $USER_NAME \
  splunk-otel-collector-chart/splunk-otel-collector
```

> 注意: `Missing variables` というエラーが表示された場合は、環境変数を再度定義する必要があります。以下のコマンドを実行する前に、参加者番号を設定してください。
>
> ``` bash
> export PARTICIPANT_NUMBER=<your participant number>
> export USER_NAME=workshop-participant-$PARTICIPANT_NUMBER
> export CLUSTER_NAME=ai-pod-$USER_NAME
> export ENVIRONMENT_NAME=ai-pod-$USER_NAME
> export SPLUNK_INDEX=splunk4rookies-workshop
> ```

## AI POD Overview Dashboardタブの確認

Splunk Observability Cloudで `Dashboards` に移動し、`Built-in dashboard groups` に含まれている `Cisco AI PODs Dashboard` を検索します。ダッシュボードがOpenShiftクラスター名でフィルタリングされていることを確認します。以下の例のようにチャートが表示されます。

![Kubernetes Pods](../../images/Cisco-AI-Pod-dashboard.png)

## Pure Storage Dashboardタブの確認

`PURE STORAGE` タブに移動し、ダッシュボードがOpenShiftクラスター名でフィルタリングされていることを確認します。以下の例のようにチャートが表示されます。

![Pure Storage Dashboard](../../images/PureStorage.png)

## Weaviate Infrastructure Navigatorの確認

WeaviateはデフォルトではAI PODに含まれていないため、標準のAI POD Dashboardには含まれていません。代わりに、Infrastructure Navigatorを使用してWeaviateのパフォーマンスデータを確認できます。

Splunk Observability Cloudで `Infrastructure` -> `AI Frameworks` -> `Weaviate` に移動します。対象の `k8s.cluster.name` でフィルタリングし、以下の例のようにNavigatorが表示されていることを確認します。

![Kubernetes Pods](../../images/WeaviateNavigator.png)
