---
title: NVIDIA コンポーネントのモニタリング
linkTitle: 4. NVIDIA コンポーネントのモニタリング
weight: 4
time: 10 minutes
---

このセクションでは、OpenTelemetry Collector で Prometheus レシーバーを使用して、OpenShift クラスターで動作している NVIDIA コンポーネントをモニタリングします。まず、Collector の設定ファイルが保存されているディレクトリに移動します。

``` bash
cd otel-collector
```

## NVIDIA DCGM Exporter メトリクスの取得

[NVIDIA DCGM exporter](https://github.com/NVIDIA/dcgm-exporter) は OpenShift クラスターで動作しています。これは Splunk に送信できる GPU メトリクスを公開します。

これを行うために、Collector のデプロイ時に使用した `otel-collector-values.yaml` ファイルを編集して、Collector の設定をカスタマイズしましょう。

`kubeletstats` レシーバーの直下に、以下の内容を追加します。

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

これにより、Collector は `app=nvidia-dcgm-exporter` というラベルを持つ Pod を検索します。このラベルを持つ Pod が見つかると、その Pod のポート 9400 に接続し、デフォルトのメトリクスエンドポイント（`/v1/metrics`）をスクレイプします。

> なぜ **Prometheus** レシーバーだけでなく **receiver_creator** レシーバーを使用するのでしょうか?
> * **Prometheus** レシーバーは、事前に定義されたエンドポイントからメトリクスをスクレイプする静的な設定を使用します。
> * **receiver_creator** レシーバーは、ランタイム情報に基づいてレシーバー（Prometheus レシーバーを含む）を動的に作成でき、スケーラブルで柔軟なスクレイプ設定を可能にします。
> * **receiver_creator** を使用すると、動的な環境で複数の Prometheus スクレイプターゲットの管理を自動化し、設定を簡素化できます。

この新しいレシーバーが使用されるようにするために、`otel-collector-values.yaml` ファイルに新しいパイプラインも追加する必要があります。

以下のコードをファイルの末尾に追加します。

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

次のセクションで、NVIDIA に関連するもう 1 つの Prometheus レシーバーを追加します。

## NVIDIA NIM メトリクスの取得

`meta-llama-3-2-1b-instruct` 大規模言語モデルは、NVIDIA NIM を使用して OpenShift クラスターにデプロイされました。Collector でスクレイプできる Prometheus エンドポイントが含まれています。以下を `otel-collector-values.yaml` ファイルの、先ほど追加した `prometheus/dcgm` レシーバーの直下に追加しましょう。

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

これにより、Collector は `app=meta-llama-3-2-1b-instruct` というラベルを持つ Pod を検索します。このラベルを持つ Pod が見つかると、その Pod のポート 8000 に接続し、`/v1/metrics` メトリクスエンドポイントをスクレイプします。

このレシーバーは `receiver_creator/nvidia` レシーバーの一部として既に取得されるため、パイプラインを変更する必要はありません。

## フィルタープロセッサーの追加

Prometheus エンドポイントのスクレイプは、大量のメトリクスを生成することがあり、カーディナリティが高くなる場合があります。

Splunk に送信するメトリクスを正確に定義するフィルタープロセッサーを追加しましょう。具体的には、ダッシュボードのチャートまたはアラートディテクターで使用されているメトリクス **のみ** を送信します。

以下のコードを `otel-collector-values.yaml` ファイルの、exporters セクションの後、receivers セクションの前に追加します。

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

先ほど追加した `metrics/nvidia-metrics` パイプラインに `filter/metrics_to_be_included` プロセッサーが含まれていることを確認します。

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

修正した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-nvidia.yaml` ファイルと比較してください。
必要に応じてファイルを更新し、内容が一致することを確認してください。`yaml` ファイルではインデントが重要であり、正確である必要があることを忘れないでください。

OpenShift 環境では Collector の再起動に約 3 分かかるため、すべての設定変更が完了するまで再起動は待ちます。
