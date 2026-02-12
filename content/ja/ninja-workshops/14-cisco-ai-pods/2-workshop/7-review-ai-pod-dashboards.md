---
title: AI POD ダッシュボードの確認
linkTitle: 7. AI POD ダッシュボードの確認
weight: 7
time: 10 minutes
---

このセクションでは、Splunk Observability Cloud の AI POD ダッシュボードを確認し、NVIDIA、Pure Storage、および Weaviate からのデータが期待通りに取得されていることを確認します。

## OpenTelemetry Collector の設定を更新する

以下の Helm コマンドを実行して、Collector の設定変更を適用できます：

``` bash
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

## AI POD 概要ダッシュボードタブの確認

Splunk Observability Cloud で `Dashboards` に移動し、`Built-in dashboard groups` に含まれている `Cisco AI PODs Dashboard` を検索してください。ダッシュボードが OpenShift クラスター名でフィルタリングされていることを確認してください。チャートは以下の例のように表示されるはずです：

![Kubernetes Pods](../../images/Cisco-AI-Pod-dashboard.png)

## Pure Storage ダッシュボードタブの確認

`PURE STORAGE` タブに移動し、ダッシュボードが OpenShift クラスター名でフィルタリングされていることを確認してください。チャートは以下の例のように表示されるはずです：

![Pure Storage Dashboard](../../images/PureStorage.png)

## Weaviate Infrastructure Navigator の確認

Weaviate は AI POD にデフォルトで含まれていないため、すぐに使える AI POD ダッシュボードには含まれていません。代わりに、Infrastructure Navigator の1つを使用して Weaviate のパフォーマンスデータを確認できます。

Splunk Observability Cloud で `Infrastructure` -> `AI Frameworks` -> `Weaviate` に移動してください。対象の `k8s.cluster.name` でフィルタリングし、以下の例のように Navigator が表示されていることを確認してください：

![Kubernetes Pods](../../images/WeaviateNavigator.png)
