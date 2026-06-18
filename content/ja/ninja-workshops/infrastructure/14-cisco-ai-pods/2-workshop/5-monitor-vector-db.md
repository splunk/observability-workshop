---
title: ベクトルデータベースの監視
linkTitle: 5. ベクトルデータベースの監視
weight: 5
time: 5 minutes
---

このステップでは、Weaviate ベクトルデータベースを監視するために Prometheus レシーバーを設定します。

## ベクトルデータベースとは？

**ベクトルデータベース**は、テキストや画像などの情報の**意味的な意味**を捉える数値的な「ベクトル埋め込み」としてデータを保存し、インデックスを作成します。従来のデータベースとは異なり、完全一致ではなく概念的に関連するデータポイントを見つける**類似性検索**に優れています。

## ベクトルデータベースはどのように使用されるか？

ベクトルデータベースは、Large Language Models (LLMs) を活用するアプリケーションで広く使用されている **Retrieval Augmented Generation (RAG)** と呼ばれるパターンで重要な役割を果たします。

パターンは以下の通りです

* エンドユーザーがアプリケーションに質問をします
* アプリケーションが質問を受け取り、そのベクトル埋め込みを計算します
* アプリがベクトルデータベース内の関連ドキュメントを探す類似性検索を実行します
* アプリが元の質問と関連ドキュメントをコンテキストとして LLM に送信します
* LLM がコンテキストを確認し、アプリケーションにレスポンスを返します

## Prometheus で Weaviate メトリクスを収集する

OpenTelemetry コレクターの設定を変更して、Weaviate の Prometheus メトリクスをスクレイプしましょう。

`otel-collector-values.yaml` ファイルに追加の Prometheus **receiver** クリエーターセクションを追加します。`receiver_creator/nvidia` セクションの後、`pipelines` セクションの前に追加してください

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

Weaviate のメトリクスを `filter/metrics_to_be_included` フィルタープロセッサーの設定にも追加する必要があります

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

> 注: `object_count` から始まる新しいメトリクスのみを追加してください

また、以下の設定で Resource **processor** を設定ファイルに追加します。`filter/metrics_to_be_included` **processor** の後、`receivers` セクションの前に追加してください

``` yaml
      resource/weaviate:
        attributes:
          - key: weaviate.instance.id
            from_attribute: service.instance.id
            action: insert
```

この **processor** は、Weaviate メトリクスの `service.instance.id` プロパティを取得し、`weaviate.instance.id` という新しいプロパティにコピーします。これは、Splunk Observability Cloud で使用される標準的な OpenTelemetry プロパティである `service.instance.id` を使用する他のメトリクスと Weaviate メトリクスをより簡単に区別するために行います。

Weaviate メトリクス用の新しいメトリクス **pipeline** も追加する必要があります（`weaviate.instance.id` メトリクスが Weaviate 以外のメトリクスに追加されないように、別の **pipeline** を使用する必要があります）。ファイルの末尾に以下を追加してください

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

変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-weaviate.yaml` ファイルと比較してみてください。`yaml` ファイルではインデントが重要であり、正確である必要があることを忘れないでください

``` bash
diff otel-collector-values.yaml otel-collector-values-with-weaviate.yaml
```

必要に応じてファイルを更新し、内容が一致するようにしてください。

{{% notice title="まだコレクターを再起動しないでください" style="warning" %}}

OpenShift 環境ではコレクターの再起動にノードあたり3分かかるため、すべての設定変更が完了するまで再起動を待ちます。

{{% /notice %}}
