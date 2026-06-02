---
title: Deploy the Vector Database
linkTitle: 8. Deploy the Vector Database
weight: 8
time: 10 minutes
---

このステップでは、OpenShiftクラスターにベクトルデータベースをデプロイし、ワークショップ参加者が使用するテストデータを投入します。

## Deploy a Vector Database

このワークショップでは、オープンソースのベクトルデータベースである [Weaviate](https://weaviate.io/) をデプロイします。

まず、Weaviate helm chartが含まれているWeaviate helmリポジトリを追加します。

``` bash
helm repo add weaviate https://weaviate.github.io/weaviate-helm
helm repo update
```

`weaviate/weaviate-values.yaml` ファイルには、Weaviateベクトルデータベースをデプロイするために使用する設定が含まれています。

後ほどPrometheus receiverでスクレイプできるメトリクスをWeaviateが公開するように、以下の環境変数を `TRUE` に設定しています。

````
  PROMETHEUS_MONITORING_ENABLED: true
  PROMETHEUS_MONITORING_GROUP: true
````

利用可能なその他のカスタマイズオプションについては、[Weaviate documentation](https://docs.weaviate.io/deploy/installation-guides/k8s-installation) を参照してください。

新しいnamespaceを作成します。

``` bash
oc create namespace weaviate
```

Weaviateが特権コンテナを実行できるように、以下のコマンドを実行します。

> 注: このアプローチは本番環境では推奨されません

``` bash
oc adm policy add-scc-to-user privileged -z default -n weaviate
```

続いてWeaviateをデプロイします。

``` bash
helm upgrade --install \
  "weaviate" \
  weaviate/weaviate \
  --namespace "weaviate" \
  --values ./weaviate/weaviate-values.yaml
```

## Populate the Vector Database

Weaviateが起動したので、カスタムアプリケーションを使ってワークショップで利用するデータを投入していきます。

このために使用するアプリケーションは、[LangChain Playbook for NeMo Retriever Text Embedding NIM](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/playbook.html#generate-embeddings-with-text-embedding-nim) をベースにしています。

`./load-embeddings/k8s-job.yaml` の設定に従い、[datasheet for the NVIDIA H200 Tensor Core GPU](https://nvdam.widen.net/content/udc6mzrk7a/original/hpc-datasheet-sc23-h200-datasheet-3002446.pdf) をベクトルデータベースにロードします。

このドキュメントには、私たちが利用する大規模言語モデルが学習していないNVIDIA H200 GPUに関する情報が含まれています。ワークショップの次のパートでは、このドキュメントをベクトルデータベースにロードしたうえで、その内容をコンテキストとして利用してLLMが質問に回答するアプリケーションを構築します。

OpenShiftクラスターにKubernetes Jobをデプロイして、エンベディングをロードします。このプロセスを一度だけ実行することを保証するため、PodではなくKubernetes Jobを使用します。

``` bash
oc create namespace llm-app
oc apply -f ./load-embeddings/k8s-job.yaml
```

> 注: エンベディングをWeaviateにロードするPythonアプリケーションのDockerイメージをビルドする際には、以下のコマンドを実行しました。
>
> ``` bash
> cd workshop/cisco-ai-pods/load-embeddings
> docker build --platform linux/amd64 -t derekmitchell399/load-embeddings:1.0 .
> docker push derekmitchell399/load-embeddings:1.0
> ```
