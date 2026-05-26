---
title: Monitor the Vector Database
linkTitle: 5. Monitor the Vector Database
weight: 5
time: 5 minutes
---

In this step, we'll configure the Prometheus receiver to monitor the Weaviate vector database. 

## What is a Vector Database? 

A **vector database** stores and indexes data as numerical "vector embeddings," which capture
the **semantic meaning** of information like text or images. Unlike traditional databases,
they excel at **similarity searches**, finding conceptually related data points rather
than exact matches.

## How is a Vector Database Used? 

Vector databases play a key role in a pattern called
**Retrieval Augmented Generation (RAG)**, which is widely used by 
applications that leverage Large Language Models (LLMs). 

The pattern is as follows: 

* The end-user asks a question to the application 
* The application takes the question and calculates a vector embedding for it
* The app then performs a similarity search, looking for related documents in the vector database
* The app then takes the original question and the related documents, and sends it to the LLM as context 
* The LLM reviews the context and returns a response to the application 

## Capture Weaviate Metrics with Prometheus

Let's modify the OpenTelemetry collector configuration to scrape Weaviate's Prometheus 
metrics. 

To do so, let's add an additional Prometheus **receiver** creator section 
to the `otel-collector-values.yaml` file.  Add it after the `receiver_creator/nvidia` 
section but before the `pipelines` section: 

``` yaml
      receiver_creator/weaviate:
        # Name of the extensions to watch for endpoints to start and stop.
        watch_observers: [ k8s_observer ]
        receivers:
          prometheus/weaviate:
            config:
              config:
                scrape_configs:
                  - job_name: weaviate-metrics
                    scrape_interval: 60s
                    static_configs:
                      - targets:
                          - '`endpoint`:2112'
            rule: type == "pod" && labels["app"] == "weaviate"
```

We'll need to ensure that Weaviate's metrics are added to the `filter/metrics_to_be_included` filter 
processor configuration as well: 

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
              - object_count
              - vector_index_size
              - vector_index_operations
              - vector_index_tombstones
              - vector_index_tombstone_cleanup_threads
              - vector_index_tombstone_cleanup_threads
              - requests_total
              - objects_durations_ms_sum
              - objects_durations_ms_count
              - batch_delete_durations_ms_sum
              - batch_delete_durations_ms_count
```

> Note: add just the new metrics starting with `object_count`

We also want to add a Resource **processor** to the configuration file with 
the following configuration. Add it after the `filter/metrics_to_be_included` **processor** 
but before the `receivers` section: 

``` yaml
      resource/weaviate:
        attributes:
          - key: weaviate.instance.id
            from_attribute: service.instance.id
            action: insert
```

This **processor** takes the `service.instance.id` property on the Weaviate metrics 
and copies it into a new property called `weaviate.instance.id`. This is done so
that we can more easily distinguish Weaviate metrics from other metrics that use 
`service.instance.id`, which is a standard OpenTelemetry property used in 
Splunk Observability Cloud. 

We'll need to add a new metrics **pipeline** for Weaviate metrics as well (we 
need to use a separate **pipeline** since we don't want the `weaviate.instance.id` 
metric to be added to non-Weaviate metrics). Add the following to the bottom of the file: 

``` yaml
        metrics/weaviate:
          exporters:
            - signalfx
          processors:
            - memory_limiter
            - filter/metrics_to_be_included
            - resource/weaviate
            - batch
            - resourcedetection
            - resource
          receivers:
            - receiver_creator/weaviate
```

Take a moment to compare the
contents of your modified `otel-collector-values.yaml` file with the 
`otel-collector-values-with-weaviate.yaml` file. Remember that indentation
is important for `yaml` files, and needs to be precise:

``` bash
diff otel-collector-values.yaml otel-collector-values-with-weaviate.yaml
```

Update your file if needed to ensure the contents match.


{{% notice title="Don't restart the collector yet" style="warning" %}}

Because restarting the collector in an OpenShift environment takes 3 minutes per node,
we'll wait until we've completed all configuration changes before initiating a restart.

{{% /notice %}}
