---
title: ベクトルデータベースのデプロイ
linkTitle: 8. ベクトルデータベースのデプロイ
weight: 8
time: 10 minutes
---

このステップでは、OpenShiftクラスターにベクトルデータベースをデプロイし、ワークショップ参加者が使用するテストデータを投入します。

## ベクトルデータベースのデプロイ

このワークショップでは、オープンソースのベクトルデータベースである[Weaviate](https://weaviate.io/)をデプロイします。

まず、Weaviate Helmチャートを含むWeaviate Helmリポジトリを追加します。

``` bash
helm repo add weaviate https://weaviate.github.io/weaviate-helm
helm repo update
```

`weaviate/weaviate-values.yaml` ファイルには、Weaviateベクトルデータベースのデプロイに使用する設定が含まれています。

WeaviateがPrometheus Receiverで後からスクレイプできるメトリクスを公開するように、以下の環境変数を `TRUE` に設定しています。

````
  PROMETHEUS_MONITORING_ENABLED: true
  PROMETHEUS_MONITORING_GROUP: true
````

利用可能な追加のカスタマイズオプションについては、[Weaviateドキュメント](https://docs.weaviate.io/deploy/installation-guides/k8s-installation)を参照してください。

新しいnamespaceを作成します。

``` bash
oc create namespace weaviate
```

Weaviateが特権コンテナを実行できるようにするために、以下のコマンドを実行します。

> 注意: この方法は本番環境では推奨されません

``` bash
oc adm policy add-scc-to-user privileged -z default -n weaviate
```

次に、Weaviateをデプロイします。

``` bash
helm upgrade --install \
  "weaviate" \
  weaviate/weaviate \
  --namespace "weaviate" \
  --values ./weaviate/weaviate-values.yaml
```

## ベクトルデータベースへのデータ投入

Weaviateが起動したので、ワークショップでカスタムアプリケーションと共に使用するデータを追加します。

この処理に使用するアプリケーションは、[LangChain Playbook for NeMo Retriever Text Embedding NIM](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/playbook.html#generate-embeddings-with-text-embedding-nim)に基づいています。

`./load-embeddings/k8s-job.yaml` の設定に従い、[NVIDIA H200 Tensor Core GPUのデータシート](https://nvdam.widen.net/content/udc6mzrk7a/original/hpc-datasheet-sc23-h200-datasheet-3002446.pdf)をベクトルデータベースにロードします。

このドキュメントには、大規模言語モデルが学習していないNVIDIA H200 GPUに関する情報が含まれています。ワークショップの次のパートでは、ベクトルデータベースにロードされたこのドキュメントのコンテキストを使用して、LLMが質問に回答するアプリケーションを構築します。

OpenShiftクラスターにKubernetes Jobをデプロイして、エンベディングをロードします。このプロセスが一度だけ実行されるようにするために、PodではなくKubernetes Jobを使用します。

``` bash
oc create namespace llm-app
oc apply -f ./load-embeddings/k8s-job.yaml
```

> 注意: エンベディングをWeaviateにロードするPythonアプリケーションのDockerイメージをビルドするには、以下のコマンドを実行しました。
>
> ``` bash
> cd workshop/cisco-ai-pods/load-embeddings
> docker build --platform linux/amd64 -t derekmitchell399/load-embeddings:1.0 .
> docker push derekmitchell399/load-embeddings:1.0
> ```
