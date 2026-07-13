---
title: ストレージのモニタリング
linkTitle: 6. Monitor Storage
weight: 6
time: 5 minutes
---

このステップでは、ストレージをモニタリングするためにPrometheus Receiverを設定します。

## Cisco AI PODsはどのようなストレージを利用しているか

Cisco AI PODsには、Pure Storage、VAST、NetAppなど、さまざまなストレージオプションがあります。

このワークショップではPure Storageに焦点を当てます。

## Pure Storageのメトリクスをどのように取得するか

Pure Storageを利用するCisco AI PODsは、Kubernetesの永続ストレージを提供するPortworxというテクノロジーも使用しています。

Portworxには、Prometheus Receiverを使用してスクレイピングできるメトリクスエンドポイントが含まれています。

## Prometheusでストレージメトリクスを取得する

OpenTelemetry Collectorの設定を変更して、Prometheusの **Receiver** でPortworxメトリクスをスクレイピングします。

追加のPrometheus **receiver creator** セクションを `otel-collector-values.yaml` ファイルに追加します。`receiver_creator/weaviate` セクションの後、`pipelines` セクションの前に追加してください。

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

Portworxメトリクスを `filter/metrics_to_be_included` フィルターのProcessor設定にも追加する必要があります。

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

> 注意: `px_cluster_cpu_percent` から始まる新しいメトリクスのみを追加します

Portworxメトリクス用の新しいメトリクス **pipeline** も追加する必要があります。ファイルの末尾に以下を追加します。

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

変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-portworx.yaml` ファイルと比較してみましょう。`yaml` ファイルではインデントが重要であり、正確である必要があります。

``` bash
diff otel-collector-values.yaml otel-collector-values-with-portworx.yaml
```

内容が一致するように、必要に応じてファイルを更新してください。

{{% notice title="まだCollectorを再起動しないでください" style="warning" %}}

OpenShift環境ではCollectorの再起動にノードあたり3分かかるため、すべての設定変更が完了するまで再起動を待ちます。

{{% /notice %}}
