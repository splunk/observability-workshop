---
title: Monitor NVIDIA Components
linkTitle: 4. Monitor NVIDIA Components
weight: 4
time: 10 minutes
---

In this section, we'll use the Prometheus receiver with the OpenTelemetry collector 
to monitor the NVIDIA components running in the OpenShift cluster. We'll start by 
navigating to the directory where the collector configuration file is stored:

``` bash
cd otel-collector
```

## Capture the NVIDIA DCGM Exporter metrics 

The [NVIDIA DCGM exporter](https://github.com/NVIDIA/dcgm-exporter) is running 
in our OpenShift cluster. It exposes GPU metrics that we can send to Splunk.

To do this, let's customize the configuration of the collector by editing the 
`otel-collector-values.yaml` file that we used earlier when deploying the collector. 

Add the following content, just below the `kubeletstats` receiver: 

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

This tells the collector to look for pods with a label of `app=nvidia-dcgm-exporter`. 
And when it finds a pod with this label, it will connect to port 9400 of the pod and scrape 
the default metrics endpoint (`/v1/metrics`). 

> Why are we using the **receiver_creator** receiver instead of just the **Prometheus** receiver?
> * The **Prometheus** receiver uses a static configuration that scrapes metrics from predefined endpoints.
> * The **receiver_creator** receiver enables dynamic creation of receivers (including Prometheus receivers) based on runtime information, allowing for scalable and flexible scraping setups.
> * Using **receiver_creator** can simplify configurations in dynamic environments by automating the management of multiple Prometheus scraping targets.

To ensure this new receiver is used, we'll need to add a new pipeline to the 
`otel-collector-values.yaml` file as well.  

Add the following code to the bottom of the file: 

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

We'll add one more Prometheus receiver related to NVIDIA in the next section. 

## Capture the NVIDIA NIM metrics

The `meta-llama-3-2-1b-instruct` large language model was deployed to the 
OpenShift cluster using NVIDIA NIM. It includes a Prometheus endpoint 
that we can scrape with the collector.  Let's add the following to the 
`otel-collector-values.yaml` file, just below the `prometheus/dcgm` receiver 
we added earlier: 

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

This tells the collector to look for pods with a label of `app=meta-llama-3-2-1b-instruct`.
And when it finds a pod with this label, it will connect to port 8000 of the pod and scrape
the `/v1/metrics` metrics endpoint. 

There's no need to make changes to the pipeline, as this receiver will already be picked up 
as part of the `receiver_creator/nvidia` receiver. 

## Add a Filter Processor 

Scraping Prometheus endpoints can result in a large number of metrics, sometimes 
with high cardinality. 

Let's add a filter processor that defines exactly what metrics we want to send to Splunk. 
Specifically, we'll send **only** the metrics that are utilized by a dashboard chart or an 
alert detector. 

Add the following code to the `otel-collector-values.yaml` file, after the exporters section 
but before the receivers section:

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

Ensure the `filter/metrics_to_be_included` processor is included in the 
`metrics/nvidia-metrics` pipeline we added earlier: 

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

## Verify Changes 

Take a moment to compare the contents of your modified `otel-collector-values.yaml` 
file with the `otel-collector-values-with-nvidia.yaml` file. 
Update your file if needed to ensure the contents match.  Remember that indentation is important 
for `yaml` files, and needs to be precise. 

Because restarting the collector in an OpenShift environment takes about 3 minutes, 
we'll wait until we've completed all configuration changes before initiating a restart.
