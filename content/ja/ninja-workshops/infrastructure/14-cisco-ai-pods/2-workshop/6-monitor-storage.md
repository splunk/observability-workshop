---
title: Monitor Storage
linkTitle: 6. Monitor Storage
weight: 6
time: 5 minutes
---

このステップでは、ストレージを監視するために Prometheus receiver を設定します。

## Cisco AI PODs はどのようなストレージを利用していますか？

Cisco AI PODs には、Pure Storage、VAST、NetApp など、さまざまなストレージオプションがあります。

本ワークショップでは Pure Storage に焦点を当てます。

## Pure Storage のメトリクスをどのように取得しますか？

Pure Storage を利用する Cisco AI PODs は、Kubernetes に永続ストレージを提供する Portworx と呼ばれる技術も利用しています。

Portworx にはメトリクスエンドポイントが含まれており、Prometheus receiver を使ってスクレイピングできます。

## Prometheus でストレージメトリクスを取得する

OpenTelemetry collector の設定を変更し、Prometheus **receiver** で Portworx メトリクスをスクレイピングするようにします。

そのために、`otel-collector-values.yaml` ファイルに Prometheus **receiver creator** セクションを追加します。`receiver_creator/weaviate` セクションの後、`pipelines` セクションの前に追加してください。

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

また、`filter/metrics_to_be_included` フィルタープロセッサーの設定にも Portworx メトリクスが追加されていることを確認する必要があります。

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

> 注意: `px_cluster_cpu_percent` から始まる新しいメトリクスのみを追加してください

Portworx メトリクス用の新しいメトリクス **pipeline** も追加する必要があります。ファイルの末尾に以下を追加してください。

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

ここで、変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-portworx.yaml` ファイルと比較してみましょう。`yaml` ファイルではインデントが重要であり、正確である必要があることを覚えておいてください。

``` bash
diff otel-collector-values.yaml otel-collector-values-with-portworx.yaml
```

内容が一致するように、必要に応じてファイルを更新してください。

{{% notice title="まだ collector を再起動しないでください" style="warning" %}}

OpenShift 環境では collector の再起動にノードあたり 3 分かかるため、すべての設定変更が完了するまで再起動の開始は待ちます。

{{% /notice %}}
