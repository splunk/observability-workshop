---
title: AI POD ダッシュボードの確認
linkTitle: 7. AI POD ダッシュボードの確認
weight: 7
time: 10 minutes
---

このセクションでは、Splunk Observability Cloud の AI POD ダッシュボードを確認し、NVIDIA、Pure Storage、および Weaviate からのデータが期待どおりに取り込まれていることを確認します。

## OpenTelemetry Collector 設定の更新

以下の Helm コマンドを実行して、Collector の設定変更を適用します:

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

> 注: `Missing variables` というエラーが表示された場合は、環境変数を再度定義する必要があります。以下のコマンドを実行する前に、参加者番号を設定してください:
>
> ``` bash
> export PARTICIPANT_NUMBER=<your participant number>
> export USER_NAME=workshop-participant-$PARTICIPANT_NUMBER
> export CLUSTER_NAME=ai-pod-$USER_NAME
> export ENVIRONMENT_NAME=ai-pod-$USER_NAME
> export SPLUNK_INDEX=splunk4rookies-workshop
> ```

## AI POD Overview ダッシュボードタブの確認

Splunk Observability Cloud で `Dashboards` に移動し、`Built-in dashboard groups` に含まれている `Cisco AI PODs Dashboard` を検索します。ダッシュボードがお使いの OpenShift クラスター名でフィルタリングされていることを確認してください。以下の例のようにチャートが表示されているはずです:

![Kubernetes Pods](../../images/Cisco-AI-Pod-dashboard.png)

## Pure Storage ダッシュボードタブの確認

`PURE STORAGE` タブに移動し、ダッシュボードがお使いの OpenShift クラスター名でフィルタリングされていることを確認します。以下の例のようにチャートが表示されているはずです:

![Pure Storage Dashboard](../../images/PureStorage.png)

## Weaviate Infrastructure Navigator の確認

Weaviate は AI POD にデフォルトで含まれていないため、標準の AI POD ダッシュボードには含まれていません。代わりに、Infrastructure Navigator を使用して Weaviate のパフォーマンスデータを確認できます。

Splunk Observability Cloud で `Infrastructure` -> `AI Frameworks` -> `Weaviate` に移動します。対象の `k8s.cluster.name` でフィルタリングし、以下の例のように Navigator が表示されていることを確認してください:

![Kubernetes Pods](../../images/WeaviateNavigator.png)
