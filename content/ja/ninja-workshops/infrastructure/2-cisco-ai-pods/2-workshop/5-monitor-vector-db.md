---
title: ベクトルデータベースのモニタリング
linkTitle: 5. ベクトルデータベースのモニタリング
weight: 5
time: 5 minutes
---

このステップでは、Weaviateベクトルデータベースをモニタリングするために Prometheus Receiver を設定します。

## ベクトルデータベースとは

**ベクトルデータベース** は、テキストや画像などの情報の **意味的な意味** を捉える数値的な「ベクトル埋め込み」としてデータを保存し、インデックスを作成します。従来のデータベースとは異なり、完全一致ではなく概念的に関連するデータポイントを見つける **類似性検索** に優れています。

## ベクトルデータベースの使われ方

ベクトルデータベースは、大規模言語モデル（LLM）を活用するアプリケーションで広く使用されている **Retrieval Augmented Generation（RAG）** と呼ばれるパターンで重要な役割を果たします。

パターンは以下のとおりです。

* エンドユーザーがアプリケーションに質問をする
* アプリケーションが質問を受け取り、ベクトル埋め込みを計算する
* アプリがベクトルデータベース内の関連ドキュメントを類似性検索で探す
* アプリが元の質問と関連ドキュメントをコンテキストとしてLLMに送信する
* LLMがコンテキストを確認し、アプリケーションにレスポンスを返す

## PrometheusでWeaviateメトリクスを取得する

OpenTelemetry Collectorの設定を変更して、WeaviateのPrometheusメトリクスをスクレイプします。

`otel-collector-values.yaml` ファイルに追加のPrometheus **Receiver** クリエーターセクションを追加します。`receiver_creator/nvidia` セクションの後、`pipelines` セクションの前に追加します。

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

Weaviateのメトリクスを `filter/metrics_to_be_included` フィルター Processor の設定にも追加する必要があります。

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

> 注意: `object_count` 以降の新しいメトリクスのみを追加します

また、設定ファイルにResource **Processor** を追加します。以下の設定を `filter/metrics_to_be_included` **Processor** の後、`receivers` セクションの前に追加します。

``` yaml
      resource/weaviate:
        attributes:
          - key: weaviate.instance.id
            from_attribute: service.instance.id
            action: insert
```

この **Processor** は、Weaviateメトリクスの `service.instance.id` プロパティを取得し、`weaviate.instance.id` という新しいプロパティにコピーします。これは、Splunk Observability Cloudで使用される標準的なOpenTelemetryプロパティである `service.instance.id` を使用する他のメトリクスと、Weaviateメトリクスをより簡単に区別するために行います。

Weaviateメトリクス用の新しいメトリクス **pipeline** も追加する必要があります（Weaviate以外のメトリクスに `weaviate.instance.id` が追加されないように、別の **pipeline** を使用します）。ファイルの末尾に以下を追加します。

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

変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-weaviate.yaml` ファイルと比較します。`yaml` ファイルではインデントが重要であり、正確である必要があることに注意してください。

``` bash
diff otel-collector-values.yaml otel-collector-values-with-weaviate.yaml
```

必要に応じてファイルを更新し、内容が一致することを確認します。

{{% notice title="まだCollectorを再起動しないでください" style="warning" %}}

OpenShift環境ではCollectorの再起動にノードごとに3分かかるため、すべての設定変更が完了するまで再起動を待ちます。

{{% /notice %}}
