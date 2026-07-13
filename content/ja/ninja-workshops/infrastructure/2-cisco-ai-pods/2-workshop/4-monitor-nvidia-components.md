---
title: NVIDIAコンポーネントのモニタリング
linkTitle: 4. NVIDIAコンポーネントのモニタリング
weight: 4
time: 10 minutes
---

このセクションでは、OpenTelemetry CollectorでPrometheus **receiver** を使用して、OpenShiftクラスターで実行されているNVIDIAコンポーネントをモニタリングします。まず、Collectorの設定ファイルが格納されているディレクトリに移動します。

``` bash
cd otel-collector
```

## NVIDIA DCGM Exporterメトリクスの取得

[NVIDIA DCGM exporter](https://github.com/NVIDIA/dcgm-exporter)がOpenShiftクラスターで実行されています。これはSplunkに送信できるGPUメトリクスを公開しています。

これを行うために、Collectorのデプロイ時に使用した `otel-collector-values.yaml` ファイルを編集して、Collectorの設定をカスタマイズします。

以下の内容を `kubeletstats` **receiver** のすぐ下に追加します。

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
                    scrape_interval: 60s
                    static_configs:
                      - targets:
                          - '`endpoint`:9400'
            rule: type == "pod" && labels["app"] == "nvidia-dcgm-exporter"
```

これにより、Collectorは `app=nvidia-dcgm-exporter` というラベルを持つPodを探します。このラベルを持つPodを見つけると、そのPodのポート9400に接続し、デフォルトのメトリクスエンドポイント（`/v1/metrics`）をスクレイプします。

> なぜ **Prometheus** receiver ではなく **receiver_creator** receiver を使用するのか？
>
> * **Prometheus** receiver は、事前定義されたエンドポイントからメトリクスをスクレイプする静的な設定を使用します。
> * **receiver_creator** receiver は、ランタイム情報に基づいてReceiver（Prometheus Receiverを含む）を動的に作成でき、スケーラブルで柔軟なスクレイプ設定を可能にします。
> * **receiver_creator** を使用すると、動的な環境で複数のPrometheusスクレイプターゲットの管理を自動化し、設定を簡素化できます。

この新しい **receiver** が使用されるようにするため、`otel-collector-values.yaml` ファイルに新しい **pipeline** を追加する必要があります。

ファイルの末尾に以下のコードを追加します。

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

次のセクションで、NVIDIAに関連するもう1つのPrometheus **receiver** を追加します。

## NVIDIA NIMメトリクスの取得

`meta-llama-3-2-1b-instruct` 大規模言語モデルは、NVIDIA NIMを使用してOpenShiftクラスターにデプロイされています。これにはCollectorでスクレイプできるPrometheusエンドポイントが含まれています。以下を `otel-collector-values.yaml` ファイルの、先ほど追加した `prometheus/dcgm` **receiver** のすぐ下に追加します。

``` yaml
          prometheus/nim-llm:
            config:
              config:
                scrape_configs:
                  - job_name: nim-for-llm-metrics
                    scrape_interval: 60s
                    metrics_path: /v1/metrics
                    static_configs:
                      - targets:
                          - '`endpoint`:8000'
            rule: type == "pod" && labels["app"] == "meta-llama-3-2-1b-instruct"
```

これにより、Collectorは `app=meta-llama-3-2-1b-instruct` というラベルを持つPodを探します。このラベルを持つPodを見つけると、そのPodのポート8000に接続し、`/v1/metrics` メトリクスエンドポイントをスクレイプします。

この **receiver** は `receiver_creator/nvidia` Receiverの一部として既に取得されるため、**pipeline** を変更する必要はありません。

## Filter Processorの追加

Prometheusエンドポイントのスクレイプにより、大量のメトリクスが生成されることがあり、カーディナリティが高くなる場合があります。

Splunkに送信するメトリクスを正確に定義するフィルター **processor** を追加します。具体的には、ダッシュボードのチャートまたはアラートディテクターで使用されるメトリクス **のみ** を送信します。

以下のコードを `otel-collector-values.yaml` ファイルの **exporters** セクションの後、**receivers** セクションの前に追加します。

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

先ほど追加した `metrics/nvidia-metrics` **pipeline** に `filter/metrics_to_be_included` **processor** が含まれていることを確認します。

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

変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-nvidia.yaml` ファイルと比較します。`yaml` ファイルではインデントが重要であり、正確である必要があることに注意してください。

``` bash
diff otel-collector-values.yaml otel-collector-values-with-nvidia.yaml
```

内容が一致するように、必要に応じてファイルを更新します。

{{% notice title="まだCollectorを再起動しないでください" style="warning" %}}

OpenShift環境ではCollectorの再起動にノードあたり3分かかるため、すべての設定変更が完了するまで再起動を待ちます。

{{% /notice %}}
