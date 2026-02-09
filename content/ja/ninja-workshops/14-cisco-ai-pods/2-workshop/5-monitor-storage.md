---
title: ストレージの監視
linkTitle: 5. ストレージの監視
weight: 5
time: 10 minutes
---

このステップでは、ストレージを監視するために Prometheus レシーバーを設定します。

## Cisco AI PODs はどのようなストレージを利用していますか？

Cisco AI PODs には、Pure Storage、VAST、NetApp など、さまざまなストレージオプションがあります。

このワークショップでは Pure Storage に焦点を当てます。

## Pure Storage のメトリクスはどのように取得しますか？

Pure Storage を利用する Cisco AI PODs は、Portworx と呼ばれる技術も使用しています。これは Kubernetes に永続ストレージを提供するものです。

Portworx には、Prometheus レシーバーを使用してスクレイプできるメトリクスエンドポイントが含まれています。

## Prometheus でストレージメトリクスを取得する

Prometheus レシーバーで Portworx メトリクスをスクレイプするために、OpenTelemetry コレクターの設定を変更しましょう。

これを行うには、`otel-collector-values.yaml` ファイルに追加の Prometheus レシーバークリエーターセクションを追加します：

``` yaml
      receiver_creator/storage:
        # Name of the extensions to watch for endpoints to start and stop.
        watch_observers: [ k8s_observer ]
        receivers:
          prometheus/portworx:
            config:
              config:
                scrape_configs:
                  - job_name: portworx-metrics
                    static_configs:
                      - targets:
                          - '`endpoint`:17001'
                          - '`endpoint`:17018'
            rule: type == "pod" && labels["app"] == "portworx-metrics-sim"
```

Portworx メトリクスを `filter/metrics_to_be_included` フィルタープロセッサーの設定にも追加する必要があります：

``` yaml
    processors:
      filter/metrics_to_be_included:
        metrics:
          # Include only metrics used in charts and detectors
          include:
            match_type: strict
            metric_names:
              - DCGM_FI_DEV_FB_FREE
              - ...
              - px_cluster_cpu_percent
              - px_cluster_disk_total_bytes
              - px_cluster_disk_utilized_bytes
              - px_cluster_status_nodes_offline
              - px_cluster_status_nodes_online
              - px_volume_read_latency_seconds
              - px_volume_reads_total
              - px_volume_readthroughput
              - px_volume_write_latency_seconds
              - px_volume_writes_total
              - px_volume_writethroughput
```

Portworx メトリクス用の新しいメトリクスパイプラインも追加する必要があります：

``` yaml
        metrics/storage:
          exporters:
            - signalfx
          processors:
            - memory_limiter
            - filter/metrics_to_be_included
            - batch
            - resourcedetection
            - resource
          receivers:
            - receiver_creator/storage
```

コレクターに設定変更を適用する前に、変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-portworx.yaml` ファイルと比較してください。必要に応じてファイルを更新し、内容が一致するようにしてください。`yaml` ファイルではインデントが重要であり、正確である必要があることを覚えておいてください。

次に、以下の Helm コマンドを実行して OpenTelemetry コレクターの設定を更新します：

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

## メトリクスが Splunk に送信されていることを確認する

Splunk Observability Cloud で `Dashboards` に移動し、`Built-in dashboard groups` に含まれている `Cisco AI PODs Dashboard` を検索します。`PURE STORAGE` タブに移動し、ダッシュボードが OpenShift クラスター名でフィルタリングされていることを確認してください。チャートは以下の例のように表示されるはずです：

![Pure Storage Dashboard](../../images/PureStorage.png)
