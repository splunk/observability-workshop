---
title: ベクトルデータベースのデプロイ
linkTitle: 8. ベクトルデータベースのデプロイ
weight: 8
time: 10 minutes
---

このステップでは、OpenShiftクラスターにベクトルデータベースをデプロイし、テストデータを投入します。

## ベクトルデータベースとは

**ベクトルデータベース**は、テキストや画像などの情報の**意味的な意味**をキャプチャする数値的な「ベクトル埋め込み」としてデータを保存およびインデックス化します。従来のデータベースとは異なり、完全一致ではなく概念的に関連するデータポイントを見つける**類似検索**に優れています。

## ベクトルデータベースはどのように使用されるか

ベクトルデータベースは、Large Language Models (LLMs)を活用するアプリケーションで広く使用されている**Retrieval Augmented Generation (RAG)**と呼ばれるパターンで重要な役割を果たします。

パターンは以下の通りです：

* エンドユーザーがアプリケーションに質問をします
* アプリケーションは質問を受け取り、そのベクトル埋め込みを計算します
* アプリケーションは類似検索を実行し、ベクトルデータベース内の関連ドキュメントを探します
* アプリケーションは元の質問と関連ドキュメントを取得し、コンテキストとしてLLMに送信します
* LLMはコンテキストを確認し、アプリケーションに応答を返します

## ベクトルデータベースのデプロイ

このワークショップでは、[Weaviate](https://weaviate.io/)というオープンソースのベクトルデータベースをデプロイします。

まず、Weaviate Helmチャートを含むWeaviate Helmリポジトリを追加します：

``` bash
helm repo add weaviate https://weaviate.github.io/weaviate-helm
helm repo update
```

`weaviate/weaviate-values.yaml`ファイルには、Weaviateベクトルデータベースをデプロイするために使用する設定が含まれています。

WeaviateがPrometheusレシーバーで後でスクレイプできるメトリクスを公開するように、以下の環境変数を`TRUE`に設定しています：

````
  PROMETHEUS_MONITORING_ENABLED: true
  PROMETHEUS_MONITORING_GROUP: true
````

利用可能な追加のカスタマイズオプションについては、[Weaviateドキュメント](https://docs.weaviate.io/deploy/installation-guides/k8s-installation)を参照してください。

新しいnamespaceを作成しましょう：

``` bash
oc create namespace weaviate
```

以下のコマンドを実行して、Weaviateが特権コンテナを実行できるようにします：

> 注意: このアプローチは本番環境では推奨されません

``` bash
oc adm policy add-scc-to-user privileged -z default -n weaviate
```

次に、Weaviateをデプロイします：

``` bash
helm upgrade --install \
  "weaviate" \
  weaviate/weaviate \
  --namespace "weaviate" \
  --values ./weaviate/weaviate-values.yaml
```

## PrometheusでWeaviateメトリクスをキャプチャする

WeaviateがOpenShiftクラスターにインストールされたので、OpenTelemetry Collectorの設定を変更してWeaviateのPrometheusメトリクスをスクレイプしましょう。

これを行うには、`otel-collector-values.yaml`ファイルに追加のPrometheusレシーバー作成セクションを追加します：

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
                    scrape_interval: 10s
                    static_configs:
                      - targets:
                          - '`endpoint`:2112'
            rule: type == "pod" && labels["app"] == "weaviate"
```

Weaviateのメトリクスが`filter/metrics_to_be_included`フィルタープロセッサの設定にも追加されていることを確認する必要があります：

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

また、以下の設定でResourceプロセッサを設定ファイルに追加します：

``` yaml
      resource/weaviate:
        attributes:
          - key: weaviate.instance.id
            from_attribute: service.instance.id
            action: insert
```

このプロセッサは、Weaviateメトリクスの`service.instance.id`プロパティを取得し、`weaviate.instance.id`という新しいプロパティにコピーします。これは、Splunk Observability Cloudで使用される標準的なOpenTelemetryプロパティである`service.instance.id`を使用する他のメトリクスからWeaviateメトリクスをより簡単に区別できるようにするためです。

Weaviateメトリクス用の新しいメトリクスパイプラインも追加する必要があります（`weaviate.instance.id`メトリクスがWeaviate以外のメトリクスに追加されないように、別のパイプラインを使用する必要があります）：  

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

コレクターに設定変更を適用する前に、修正した`otel-collector-values.yaml`ファイルの内容を`otel-collector-values-with-weaviate.yaml`ファイルと比較してみてください。内容が一致するように、必要に応じてファイルを更新してください。`yaml`ファイルではインデントが重要であり、正確である必要があることを忘れないでください。

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

Splunk Observability Cloudで、`Infrastructure` -> `AI Frameworks` -> `Weaviate`に移動します。対象の`k8s.cluster.name`でフィルタリングし、以下の例のようにナビゲーターが表示されていることを確認してください：

![Kubernetes Pods](../images/WeaviateNavigator.png)

## ベクトルデータベースへのデータ投入

Weaviateが起動して実行され、メトリクスをキャプチャしているので、カスタムアプリケーションを使用するワークショップの次のパートで使用するデータを追加しましょう。

これを行うために使用されるアプリケーションは、[NeMo Retriever Text Embedding NIM用のLangChain Playbook](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/playbook.html#generate-embeddings-with-text-embedding-nim)に基づいています。

`./load-embeddings/k8s-job.yaml`の設定に従って、[NVIDIA H200 Tensor Core GPUのデータシート](https://nvdam.widen.net/content/udc6mzrk7a/original/hpc-datasheet-sc23-h200-datasheet-3002446.pdf)をベクトルデータベースにロードします。

このドキュメントには、大規模言語モデルがトレーニングされていないNVIDIAのH200 GPUに関する情報が含まれています。ワークショップの次のパートでは、ベクトルデータベースにロードされるこのドキュメントからのコンテキストを使用して質問に答えるLLMを使用するアプリケーションを構築します。

embeddingsをロードするために、OpenShiftクラスターにKubernetes Jobをデプロイします。このプロセスが一度だけ実行されるように、PodではなくKubernetes Jobを使用します：

``` bash
oc create namespace llm-app
oc apply -f ./load-embeddings/k8s-job.yaml
```

> 注意: embeddingsをWeaviateにロードするPythonアプリケーション用のDockerイメージをビルドするには、以下のコマンドを実行しました：
>
> ``` bash
> cd workshop/cisco-ai-pods/load-embeddings
> docker build --platform linux/amd64 -t derekmitchell399/load-embeddings:1.0 .
> docker push derekmitchell399/load-embeddings:1.0
> ```
