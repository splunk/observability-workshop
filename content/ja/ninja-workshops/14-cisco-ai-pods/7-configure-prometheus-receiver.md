---
title: Prometheusレシーバーの設定
linkTitle: 7. Prometheusレシーバーの設定
weight: 7
time: 10 minutes
---

LLMが起動して実行されたので、OpenTelemetry CollectorにPrometheusレシーバーを追加して、LLMからメトリクスを収集します。

## NVIDIA DCGM Exporterメトリクスのキャプチャ

NVIDIA DCGM ExporterはOpenShiftクラスターで実行されています。Splunkに送信できるGPUメトリクスを公開しています。

これを行うには、コレクターのデプロイ時に使用した`otel-collector-values.yaml`ファイルを編集して、コレクターの設定をカスタマイズしましょう。

`kubeletstats`セクションのすぐ下に以下の内容を追加します： 

``` yaml
      receiver_creator/nvidia:
        # Name of the extensions to watch for endpoints to start and stop.
        watch_observers: [ k8s_observer ]
        receivers:
          prometheus/dcgm:
            config:
              config:
                scrape_configs:
                  - job_name: gpu-metrics
                    scrape_interval: 10s
                    static_configs:
                      - targets:
                          - '`endpoint`:9400'
            rule: type == "pod" && labels["app"] == "nvidia-dcgm-exporter"
```

これにより、コレクターは`app=nvidia-dcgm-exporter`というラベルを持つPodを探します。このラベルを持つPodが見つかると、ポート9400を使用して`/v1/metrics`エンドポイントをスクレイプします。

レシーバーが使用されるようにするために、`otel-collector-values.yaml`ファイルにも新しいパイプラインを追加する必要があります。

ファイルの末尾に以下のコードを追加します： 

``` yaml
    service:
      pipelines:
        metrics/nvidia-metrics:
          exporters:
            - signalfx
          processors:
            - memory_limiter
            - batch
            - resourcedetection
            - resource
          receivers:
            - receiver_creator/nvidia
```

変更を適用する前に、次のセクションでもう1つPrometheusレシーバーを追加しましょう。

## NVIDIA NIMメトリクスのキャプチャ

NVIDIA NIMでデプロイした`meta-llama-3-2-1b-instruct` LLMには、コレクターでスクレイプできるPrometheusエンドポイントも含まれています。先ほど追加したレシーバーのすぐ下に、`otel-collector-values.yaml`ファイルに以下を追加しましょう： 

``` yaml
          prometheus/nim-llm:
            config:
              config:
                scrape_configs:
                  - job_name: nim-for-llm-metrics
                    scrape_interval: 10s
                    metrics_path: /v1/metrics
                    static_configs:
                      - targets:
                          - '`endpoint`:8000'
            rule: type == "pod" && labels["app"] == "meta-llama-3-2-1b-instruct"
```

これにより、コレクターは`app=meta-llama-3-2-1b-instruct`というラベルを持つPodを探します。このラベルを持つPodが見つかると、ポート8000を使用して`/v1/metrics`エンドポイントをスクレイプします。

このレシーバーは`receiver_creator/nvidia`レシーバーの一部として既に取り込まれるため、パイプラインを変更する必要はありません。

## フィルタープロセッサの追加

Prometheusエンドポイントは、時として高いカーディナリティを持つ多数のメトリクスを公開することがあります。

Splunkに送信するメトリクスを正確に定義するフィルタープロセッサを追加しましょう。具体的には、ダッシュボードチャートまたはアラートディテクターで使用されるメトリクスのみを送信します。

exportersセクションの後、receiversセクションの前に、以下のコードを`otel-collector-values.yaml`ファイルに追加します：

``` yaml
    processors:
      filter/metrics_to_be_included:
        metrics:
          # Include only metrics used in charts and detectors
          include:
            match_type: strict
            metric_names:
              - DCGM_FI_DEV_FB_FREE
              - DCGM_FI_DEV_FB_USED
              - DCGM_FI_DEV_GPU_TEMP
              - DCGM_FI_DEV_GPU_UTIL
              - DCGM_FI_DEV_MEM_CLOCK
              - DCGM_FI_DEV_MEM_COPY_UTIL
              - DCGM_FI_DEV_MEMORY_TEMP
              - DCGM_FI_DEV_POWER_USAGE
              - DCGM_FI_DEV_SM_CLOCK
              - DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION
              - DCGM_FI_PROF_DRAM_ACTIVE
              - DCGM_FI_PROF_GR_ENGINE_ACTIVE
              - DCGM_FI_PROF_PCIE_RX_BYTES
              - DCGM_FI_PROF_PCIE_TX_BYTES
              - DCGM_FI_PROF_PIPE_TENSOR_ACTIVE
              - generation_tokens_total
              - go_info
              - go_memstats_alloc_bytes
              - go_memstats_alloc_bytes_total
              - go_memstats_buck_hash_sys_bytes
              - go_memstats_frees_total
              - go_memstats_gc_sys_bytes
              - go_memstats_heap_alloc_bytes
              - go_memstats_heap_idle_bytes
              - go_memstats_heap_inuse_bytes
              - go_memstats_heap_objects
              - go_memstats_heap_released_bytes
              - go_memstats_heap_sys_bytes
              - go_memstats_last_gc_time_seconds
              - go_memstats_lookups_total
              - go_memstats_mallocs_total
              - go_memstats_mcache_inuse_bytes
              - go_memstats_mcache_sys_bytes
              - go_memstats_mspan_inuse_bytes
              - go_memstats_mspan_sys_bytes
              - go_memstats_next_gc_bytes
              - go_memstats_other_sys_bytes
              - go_memstats_stack_inuse_bytes
              - go_memstats_stack_sys_bytes
              - go_memstats_sys_bytes
              - go_sched_gomaxprocs_threads
              - gpu_cache_usage_perc
              - gpu_total_energy_consumption_joules
              - http.server.active_requests
              - num_request_max
              - num_requests_running
              - num_requests_waiting
              - process_cpu_seconds_total
              - process_max_fds
              - process_open_fds
              - process_resident_memory_bytes
              - process_start_time_seconds
              - process_virtual_memory_bytes
              - process_virtual_memory_max_bytes
              - promhttp_metric_handler_requests_in_flight
              - promhttp_metric_handler_requests_total
              - prompt_tokens_total
              - python_gc_collections_total
              - python_gc_objects_collected_total
              - python_gc_objects_uncollectable_total
              - python_info
              - request_finish_total
              - request_success_total
              - system.cpu.time
              - e2e_request_latency_seconds
              - time_to_first_token_seconds
              - time_per_output_token_seconds
              - request_prompt_tokens
              - request_generation_tokens
```

このプロセッサがファイルの末尾に先ほど追加したパイプラインに含まれていることを確認します： 

``` bash
    service:
      pipelines:
        metrics/nvidia-metrics:
          exporters:
            - signalfx
          processors:
            - memory_limiter
            - filter/metrics_to_be_included
            - batch
            - resourcedetection
            - resource
          receivers:
            - receiver_creator/nvidia
```

## 変更の確認

コレクターに設定変更を適用する前に、修正した`otel-collector-values.yaml`ファイルの内容を`otel-collector-values-with-nvidia.yaml`ファイルと比較してみてください。内容が一致するように、必要に応じてファイルを更新してください。`yaml`ファイルではインデントが重要であり、正確である必要があることを忘れないでください。

## OpenTelemetry Collector設定の更新

以下のHelmコマンドを実行して、OpenTelemetry Collectorの設定を更新できます： 

``` bash
helm upgrade splunk-otel-collector \
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

## メトリクスがSplunkに送信されていることの確認

Splunk Observability Cloudの[Cisco AI Pod](https://app.us1.signalfx.com/#/dashboard/GvmWJyPA4Ak?startTime=-15m&endTime=Now&variables%5B%5D=K8s%20cluster%3Dk8s.cluster.name:%5B%22rosa-test%22%5D&groupId=GvmVcarA4AA&configId=GuzVkWWA4BE)ダッシュボードに移動します。OpenShiftクラスター名でフィルタリングされていることを確認し、以下の例のようにチャートが表示されていることを確認してください：

![Kubernetes Pods](../images/Cisco-AI-Pod-dashboard.png)