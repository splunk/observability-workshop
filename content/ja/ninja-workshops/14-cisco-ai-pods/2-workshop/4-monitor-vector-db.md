---
title: ベクトルデータベースの監視
linkTitle: 4. ベクトルデータベースの監視
weight: 4
time: 10 minutes
---

このステップでは、Weaviate ベクトルデータベースを監視するために Prometheus レシーバーを設定します。

## ベクトルデータベースとは？

**ベクトルデータベース**は、テキストや画像などの情報の**意味的な意味**を捉える数値の「ベクトル埋め込み」としてデータを保存およびインデックス化します。従来のデータベースとは異なり、完全一致ではなく概念的に関連するデータポイントを見つける**類似性検索**に優れています。

## ベクトルデータベースはどのように使用されるか？

ベクトルデータベースは、大規模言語モデル（LLM）を活用するアプリケーションで広く使用されている**検索拡張生成（RAG）**と呼ばれるパターンで重要な役割を果たします。

パターンは以下の通りです：

* エンドユーザーがアプリケーションに質問をします
* アプリケーションは質問を受け取り、そのベクトル埋め込みを計算します
* アプリはベクトルデータベースで関連ドキュメントを探す類似性検索を実行します
* アプリは元の質問と関連ドキュメントをコンテキストとして LLM に送信します
* LLM はコンテキストを確認し、アプリケーションに応答を返します

## Prometheus で Weaviate メトリクスを取得する

Weaviate の Prometheus メトリクスをスクレイプするために、OpenTelemetry コレクターの設定を変更しましょう。

そのために、`otel-collector-values.yaml` ファイルに追加の Prometheus レシーバー作成セクションを追加しましょう：

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

Weaviate のメトリクスが `filter/metrics_to_be_included` フィルタープロセッサーの設定にも追加されていることを確認する必要があります：

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

また、以下の設定で Resource プロセッサーを設定ファイルに追加します：

``` yaml
      resource/weaviate:
        attributes:
          - key: weaviate.instance.id
            from_attribute: service.instance.id
            action: insert
```

このプロセッサーは、Weaviate メトリクスの `service.instance.id` プロパティを取得し、`weaviate.instance.id` という新しいプロパティにコピーします。これは、Splunk Observability Cloud で使用される標準的な OpenTelemetry プロパティである `service.instance.id` を使用する他のメトリクスと Weaviate メトリクスをより簡単に区別できるようにするためです。

Weaviate メトリクス用の新しいメトリクスパイプラインも追加する必要があります（`weaviate.instance.id` メトリクスを Weaviate 以外のメトリクスに追加したくないため、別のパイプラインを使用する必要があります）：

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

コレクターに設定変更を適用する前に、変更した `otel-collector-values.yaml` ファイルの内容を `otel-collector-values-with-weaviate.yaml` ファイルと比較してください。内容が一致するように必要に応じてファイルを更新してください。`yaml` ファイルではインデントが重要であり、正確である必要があることを覚えておいてください。

次に、以下の Helm コマンドを実行して OpenTelemetry コレクターの設定を更新できます：

``` bash
helm upgrade splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./otel-collector-values.yaml \
  -n $USER_NAME \
  splunk-otel-collector-chart/splunk-otel-collector
```

Splunk Observability Cloud で、`Infrastructure` -> `AI Frameworks` -> `Weaviate` に移動します。対象の `k8s.cluster.name` でフィルタリングし、以下の例のようにナビゲーターが表示されていることを確認してください：

![Kubernetes Pods](../../images/WeaviateNavigator.png)

