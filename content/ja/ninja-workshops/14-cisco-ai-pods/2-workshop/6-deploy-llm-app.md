---
title: LLM アプリケーションのデプロイ
linkTitle: 6. LLM アプリケーションのデプロイ
weight: 6
time: 10 minutes
---

ワークショップの最終ステップでは、NVIDIA NIM operator を使用して先ほどデプロイした instruct モデルと embeddings モデルを使用するアプリケーションを OpenShift クラスターにデプロイします。

## アプリケーション概要

LLM と連携するほとんどのアプリケーションと同様に、このアプリケーションは Python で記述されています。また、LLM を活用したアプリケーションの開発を簡素化するオープンソースのオーケストレーションフレームワークである [LangChain](https://www.langchain.com/) を使用しています。

アプリケーションは、使用する2つの LLM に接続することから始まります：

* `meta/llama-3.2-1b-instruct`: ユーザーのプロンプトに応答するために使用
* `nvidia/llama-3.2-nv-embedqa-1b-v2`: embeddings を計算するために使用

``` python
# connect to a LLM NIM at the specified endpoint, specifying a specific model
llm = ChatNVIDIA(base_url=INSTRUCT_MODEL_URL, model="meta/llama-3.2-1b-instruct")

# Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                   base_url=EMBEDDINGS_MODEL_URL)
```

両方の LLM で使用される URL は `k8s-manifest.yaml` ファイルで定義されています：

``` yaml
    - name: INSTRUCT_MODEL_URL
      value: "http://meta-llama-3-2-1b-instruct.nim-service:8000/v1"
    - name: EMBEDDINGS_MODEL_URL
      value: "http://llama-32-nv-embedqa-1b-v2.nim-service:8000/v1"
```

次に、アプリケーションは LLM とのやり取りで使用されるプロンプトテンプレートを定義します：

``` python
prompt = ChatPromptTemplate.from_messages([
    ("system",
        "You are a helpful and friendly AI!"
        "Your responses should be concise and no longer than two sentences."
        "Do not hallucinate. Say you don't know if you don't have this information."
        "Answer the question using only the context"
        "\n\nQuestion: {question}\n\nContext: {context}"
    ),
    ("user", "{question}")
])
```

> LLM に対して、答えがわからない場合は正直にわからないと言うように明示的に指示していることに注目してください。これによりハルシネーションを最小限に抑えることができます。また、LLM が質問に答えるために使用できるコンテキストを提供するためのプレースホルダーもあります。

アプリケーションは Flask を使用しており、エンドユーザーからの質問に応答するために `/askquestion` という単一のエンドポイントを定義しています。このエンドポイントを実装するために、アプリケーションは Weaviate ベクトルデータベースに接続し、LangChain を使用してチェーンを呼び出します。このチェーンは、ユーザーの質問を受け取り、それを embedding に変換し、ベクトルデータベース内で類似のドキュメントを検索します。その後、関連ドキュメントと共にユーザーの質問を LLM に送信し、LLM のレスポンスを返します。

``` python
   # connect with the vector store that was populated earlier
    vector_store = WeaviateVectorStore(
        client=weaviate_client,
        embedding=embeddings_model,
        index_name="CustomDocs",
        text_key="page_content"
    )

    chain = (
        {
            "context": vector_store.as_retriever(),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke(question)
```

## OpenTelemetry によるアプリケーションの計装

アプリケーションからメトリクス、トレース、ログを収集するために、OpenTelemetry で計装しています。これには、`requirements.txt` ファイルに以下のパッケージを追加する必要があります（最終的に `pip install` でインストールされます）：

````
splunk-opentelemetry==2.8.0
````

また、このアプリケーションのコンテナイメージをビルドするために使用される `Dockerfile` に、追加の OpenTelemetry 計装パッケージをインストールするための以下の記述を追加しました：

``` dockerfile
# Add additional OpenTelemetry instrumentation packages
RUN opentelemetry-bootstrap --action=install
```

次に、アプリケーション実行時に `opentelemetry-instrument` を呼び出すように `Dockerfile` の `ENTRYPOINT` を変更しました：

``` dockerfile
ENTRYPOINT ["opentelemetry-instrument", "flask", "run", "-p", "8080", "--host", "0.0.0.0"]
```

最後に、この LangChain アプリケーションから OpenTelemetry で収集されるトレースとメトリクスを強化するために、追加の Splunk 計装パッケージを追加しました：

````
splunk-otel-instrumentation-langchain==0.1.4
splunk-otel-util-genai==0.1.4
````

## LLM アプリケーションのデプロイ

以下のコマンドを使用して、このアプリケーションを OpenShift クラスターにデプロイします：

``` bash
oc apply -f ./llm-app/k8s-manifest.yaml
```

> 注: この Python アプリケーションの Docker イメージをビルドするために、以下のコマンドを実行しました:
> ``` bash
> cd workshop/cisco-ai-pods/llm-app
> docker build --platform linux/amd64 -t ghcr.io/splunk/cisco-ai-pod-workshop-app:1.0 .
> docker push ghcr.io/splunk/cisco-ai-pod-workshop-app:1.0
> ```

## LLM アプリケーションのテスト

アプリケーションが期待通りに動作していることを確認しましょう。

curl コマンドにアクセスできる Pod を起動します：

``` bash
oc run curl --rm -it --image=curlimages/curl:latest \
  --overrides='{
    "spec": {
      "containers": [{
        "name": "curl",
        "image": "curlimages/curl:latest",
        "stdin": true,
        "tty": true,
        "command": ["sh"],
        "resources": {
          "limits": {
            "cpu": "50m",
            "memory": "100Mi"
          },
          "requests": {
            "cpu": "50m",
            "memory": "100Mi"
          }
        }
      }]
    }
  }'
```

次に、以下のコマンドを実行して LLM に質問を送信します：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -X "POST" \
 'http://llm-app:8080/askquestion' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "How much memory does the NVIDIA H200 have?"
  }'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
The NVIDIA H200 has 141GB of HBM3e memory, which is twice the capacity of the NVIDIA H100 Tensor Core GPU with 1.4X more memory bandwidth.
```

{{% /tab %}}
{{< /tabs >}}

## Splunk Observability Cloud でのトレースデータの確認

Splunk Observability Cloud で `APM` に移動し、`Service Map` を選択します。環境名が選択されていることを確認してください（例: `ai-pod-workshop-participant-1`）。以下のようなサービスマップが表示されるはずです：

![Service Map](../../images/ServiceMap.png)

右側のメニューで `Traces` をクリックします。次に、実行時間の長いトレースの1つを選択します。以下の例のように表示されるはずです：

![Trace](../../images/Trace.png)

トレースは、ユーザーの質問（「How much memory does the NVIDIA H200 have?」）に対する回答を返すために、アプリケーションが実行したすべてのやり取りを示しています。

例えば、Weaviate ベクトルデータベースで、当該の質問に関連するドキュメントを検索するために、アプリケーションが類似性検索を実行した箇所を確認できます。

また、ベクトルデータベースから取得したコンテキストを含め、アプリケーションが LLM に送信するプロンプトをどのように作成したかも確認できます：

![Prompt Template](../../images/PromptTemplate.png)

最後に、LLM からのレスポンス、所要時間、使用された入出力トークン数を確認できます：

![LLM Response](../../images/LLMResponse.png)

## メトリクスが Splunk に送信されていることの確認

Splunk Observability Cloud で `Dashboards` に移動し、`Built-in dashboard groups` に含まれている `Cisco AI PODs Dashboard` を検索します。`NIM FOR LLMS` タブに移動し、ダッシュボードが OpenShift クラスター名でフィルタリングされていることを確認します。以下の例のようにチャートが表示されるはずです：

![NIM LLMS Dashboard](../../images/NIMLLM.png)

