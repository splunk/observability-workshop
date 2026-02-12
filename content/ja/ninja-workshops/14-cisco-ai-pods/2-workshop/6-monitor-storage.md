---
title: ストレージのモニタリング
linkTitle: 6. ストレージのモニタリング
weight: 6
time: 5 minutes
---

このステップでは、ストレージをモニタリングするために Prometheus レシーバーを設定します。

## Cisco AI PODs はどのようなストレージを使用しているか？

Cisco AI PODs には、Pure Storage、VAST、NetApp など、さまざまなストレージオプションがあります。

このワークショップでは Pure Storage に焦点を当てます。

## Pure Storage メトリクスをどのように取得するか？

Pure Storage を使用する Cisco AI PODs は、Kubernetes に永続ストレージを提供する Portworx というテクノロジーも使用しています。

Portworx には Prometheus レシーバーでスクレイプできるメトリクスエンドポイントがあります。

## Prometheus でストレージメトリクスを取得する

OpenTelemetry Collector の設定を変更して、Prometheus レシーバーで Portworx メトリクスをスクレイプしましょう。

`otel-collector-values.yaml` ファイルに追加の Prometheus レシーバークリエーターセクションを追加します：

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

Portworx メトリクスが `filter/metrics_to_be_included` フィルタープロセッサーの設定にも追加されていることを確認する必要があります：

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

変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-portworx.yaml` ファイルと比較してください。内容が一致するように、必要に応じてファイルを更新してください。`yaml` ファイルではインデントが重要であり、正確である必要があることを忘れないでください。

OpenShift 環境では Collector の再起動に約3分かかるため、すべての設定変更が完了するまで再起動は待ちます。
