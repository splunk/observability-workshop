---
title: ベクターデータベースの監視
linkTitle: 5. ベクターデータベースの監視
weight: 5
time: 5 minutes
---

このステップでは、Weaviate ベクターデータベースを監視するために Prometheus レシーバーを設定します。

## ベクターデータベースとは

**ベクターデータベース**は、データを数値の「ベクター埋め込み (vector embeddings)」として保存・インデックス化するデータベースで、テキストや画像などの情報の**意味的な意味 (semantic meaning)** を捉えます。従来のデータベースとは異なり、完全一致ではなく概念的に関連したデータポイントを見つける**類似検索 (similarity searches)** に優れています。

## ベクターデータベースの利用方法

ベクターデータベースは、**Retrieval Augmented Generation (RAG)** と呼ばれるパターンで重要な役割を果たします。このパターンは、大規模言語モデル (LLM) を活用するアプリケーションで広く使用されています。

このパターンは次のとおりです。

* エンドユーザーがアプリケーションに質問する
* アプリケーションが質問を受け取り、ベクター埋め込みを計算する
* アプリケーションがベクターデータベースで類似検索を行い、関連ドキュメントを探す
* アプリケーションは元の質問と関連ドキュメントを LLM にコンテキストとして送信する
* LLM はコンテキストを確認し、アプリケーションに応答を返す

## Prometheus で Weaviate のメトリクスを取得する

OpenTelemetry コレクターの設定を変更して、Weaviate の Prometheus メトリクスをスクレイプするようにします。

そのために、`otel-collector-values.yaml` ファイルに追加の Prometheus **receiver** creator セクションを追加します。`receiver_creator/nvidia` セクションの後、かつ `pipelines` セクションの前に追加してください。

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

Weaviate のメトリクスを `filter/metrics_to_be_included` フィルタープロセッサーの設定にも追加する必要があります。

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

> 注意: `object_count` で始まる新しいメトリクスのみを追加してください

また、設定ファイルに以下の設定で Resource **processor** を追加します。`filter/metrics_to_be_included` **processor** の後、かつ `receivers` セクションの前に追加してください。

``` yaml
      resource/weaviate:
        attributes:
          - key: weaviate.instance.id
            from_attribute: service.instance.id
            action: insert
```

この **processor** は、Weaviate メトリクスの `service.instance.id` プロパティを取得し、`weaviate.instance.id` という新しいプロパティにコピーします。これは、`service.instance.id`（Splunk Observability Cloud で使用される標準的な OpenTelemetry プロパティ）を使用する他のメトリクスと Weaviate メトリクスをより簡単に区別できるようにするためです。

Weaviate メトリクス用の新しいメトリクス **pipeline** も追加する必要があります（`weaviate.instance.id` メトリクスを Weaviate 以外のメトリクスに追加したくないため、別の **pipeline** を使用する必要があります）。ファイルの末尾に次の内容を追加してください。

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

少し時間をとって、変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-weaviate.yaml` ファイルと比較してください。`yaml` ファイルではインデントが重要で、正確である必要があることを忘れないでください。

``` bash
diff otel-collector-values.yaml otel-collector-values-with-weaviate.yaml
```

内容が一致するように、必要に応じてファイルを更新してください。

{{% notice title="まだコレクターを再起動しないでください" style="warning" %}}

OpenShift 環境でコレクターを再起動するにはノードあたり 3 分かかるため、すべての設定変更が完了してから再起動を実行します。

{{% /notice %}}
