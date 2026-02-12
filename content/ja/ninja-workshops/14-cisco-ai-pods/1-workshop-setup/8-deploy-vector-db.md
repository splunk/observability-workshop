---
title: ベクターデータベースのデプロイ
linkTitle: 8. ベクターデータベースのデプロイ
weight: 8
time: 10 minutes
---

このステップでは、OpenShift クラスターにベクターデータベースをデプロイし、ワークショップ参加者が使用するテストデータを投入します。

## ベクターデータベースのデプロイ

このワークショップでは、オープンソースのベクターデータベースである [Weaviate](https://weaviate.io/) をデプロイします。

まず、Weaviate の Helm チャートを含む Weaviate Helm リポジトリを追加します。

``` bash
helm repo add weaviate https://weaviate.github.io/weaviate-helm
helm repo update
```

`weaviate/weaviate-values.yaml` ファイルには、Weaviate ベクターデータベースのデプロイに使用する設定が含まれています。

Weaviate が Prometheus レシーバーでスクレイピングできるメトリクスを公開するように、以下の環境変数を `TRUE` に設定しています。

````
  PROMETHEUS_MONITORING_ENABLED: true
  PROMETHEUS_MONITORING_GROUP: true
````

追加のカスタマイズオプションについては、[Weaviate のドキュメント](https://docs.weaviate.io/deploy/installation-guides/k8s-installation)を参照してください。

新しい Namespace を作成します。

``` bash
oc create namespace weaviate
```

以下のコマンドを実行して、Weaviate が特権コンテナを実行できるようにします。

> 注意: この方法は本番環境では推奨されません。

``` bash
oc adm policy add-scc-to-user privileged -z default -n weaviate
```

次に、Weaviate をデプロイします。

``` bash
helm upgrade --install \
  "weaviate" \
  weaviate/weaviate \
  --namespace "weaviate" \
  --values ./weaviate/weaviate-values.yaml
```

## ベクターデータベースへのデータ投入

Weaviate が起動したので、ワークショップでカスタムアプリケーションと共に使用するデータを追加します。

この作業に使用するアプリケーションは、[LangChain Playbook for NeMo Retriever Text Embedding NIM](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/playbook.html#generate-embeddings-with-text-embedding-nim) に基づいています。

`./load-embeddings/k8s-job.yaml` の設定に従い、[NVIDIA H200 Tensor Core GPU のデータシート](https://nvdam.widen.net/content/udc6mzrk7a/original/hpc-datasheet-sc23-h200-datasheet-3002446.pdf)をベクターデータベースにロードします。

このドキュメントには、大規模言語モデルが学習していない NVIDIA H200 GPU に関する情報が含まれています。ワークショップの次のパートでは、ベクターデータベースにロードされたこのドキュメントのコンテキストを使用して、LLM が質問に回答するアプリケーションを構築します。

OpenShift クラスターに Kubernetes Job をデプロイしてエンベディングをロードします。
このプロセスが1回だけ実行されるようにするために、Pod ではなく Kubernetes Job を使用します。

``` bash
oc create namespace llm-app
oc apply -f ./load-embeddings/k8s-job.yaml
```

> 注意: エンベディングを Weaviate にロードする Python アプリケーションの Docker イメージをビルドするために、以下のコマンドを実行しました。
> ``` bash
> cd workshop/cisco-ai-pods/load-embeddings
> docker build --platform linux/amd64 -t derekmitchell399/load-embeddings:1.0 .
> docker push derekmitchell399/load-embeddings:1.0
> ```
