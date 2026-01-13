---
title: LLMアプリケーションのデプロイ
linkTitle: 9. LLMアプリケーションのデプロイ
weight: 9
time: 10 minutes
---

ワークショップの最終ステップでは、NVIDIA NIM Operatorを使用して以前デプロイしたinstructモデルとembeddingsモデルを使用するアプリケーションをOpenShiftクラスターにデプロイします。

## アプリケーションの概要

LLMと連携するほとんどのアプリケーションと同様に、私たちのアプリケーションはPythonで書かれています。また、LLMを活用したアプリケーションの開発を簡素化するオープンソースのオーケストレーションフレームワークである[LangChain](https://www.langchain.com/)を使用しています。

アプリケーションは、使用する2つのLLMに接続することから始まります：

* `meta/llama-3.2-1b-instruct`: ユーザープロンプトへの応答に使用
* `nvidia/llama-3.2-nv-embedqa-1b-v2`: embeddingsの計算に使用

``` python
# connect to a LLM NIM at the specified endpoint, specifying a specific model
llm = ChatNVIDIA(base_url=INSTRUCT_MODEL_URL, model="meta/llama-3.2-1b-instruct")

# Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                   base_url=EMBEDDINGS_MODEL_URL)
```

両方のLLMに使用されるURLは`k8s-manifest.yaml`ファイルで定義されています：

``` yaml
    - name: INSTRUCT_MODEL_URL
      value: "http://meta-llama-3-2-1b-instruct.nim-service:8000/v1"
    - name: EMBEDDINGS_MODEL_URL
      value: "http://llama-32-nv-embedqa-1b-v2.nim-service:8000/v1"
```

次に、アプリケーションはLLMとのやり取りで使用されるプロンプトテンプレートを定義します：

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

> LLMに対して、答えがわからない場合は単に「わからない」と言うように明示的に指示していることに注目してください。これはハルシネーションを最小限に抑えるのに役立ちます。また、LLMが質問に答えるために使用できるコンテキストを提供するためのプレースホルダーもあります。

アプリケーションはFlaskを使用し、エンドユーザーからの質問に応答するための`/askquestion`という単一のエンドポイントを定義しています。このエンドポイントを実装するために、アプリケーションはWeaviateベクトルデータベースに接続し、ユーザーの質問を受け取ってembeddingに変換し、ベクトルデータベース内の類似ドキュメントを検索するチェーン（LangChainを使用）を呼び出します。その後、ユーザーの質問と関連ドキュメントをLLMに送信し、LLMの応答を返します。

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

## OpenTelemetryでアプリケーションを計装する

アプリケーションからメトリクス、トレース、ログをキャプチャするために、OpenTelemetryで計装しました。これには、`requirements.txt`ファイルに以下のパッケージを追加する必要がありました（最終的に`pip install`でインストールされます）：

````
splunk-opentelemetry==2.7.0
````

また、追加のOpenTelemetry計装パッケージをインストールするために、このアプリケーションのコンテナイメージをビルドするために使用される`Dockerfile`に以下を追加しました：

``` dockerfile
# Add additional OpenTelemetry instrumentation packages
RUN opentelemetry-bootstrap --action=install
```

次に、アプリケーションを実行するときに`opentelemetry-instrument`を呼び出すように、`Dockerfile`の`ENTRYPOINT`を変更しました：

``` dockerfile
ENTRYPOINT ["opentelemetry-instrument", "flask", "run", "-p", "8080", "--host", "0.0.0.0"]
```

最後に、OpenTelemetryで収集されるトレースとメトリクスを強化するために、[OpenLIT](https://openlit.io/)というパッケージを`requirements.txt`ファイルに追加しました：

````
openlit==1.35.4
````

OpenLITはLangChainをサポートしており、計装時にトレースに追加のコンテキストを追加します。例えば、リクエストを処理するために使用されたトークン数や、プロンプトとレスポンスの内容などです。

OpenLITを初期化するために、アプリケーションコードに以下を追加しました：

``` python
import openlit
...
openlit.init(environment="llm-app")
```

## LLMアプリケーションのデプロイ

以下のコマンドを使用して、このアプリケーションをOpenShiftクラスターにデプロイします：

``` bash
oc apply -f ./llm-app/k8s-manifest.yaml
```

> 注意: このPythonアプリケーション用のDockerイメージをビルドするには、以下のコマンドを実行しました：
>
> ``` bash
> cd workshop/cisco-ai-pods/llm-app
> docker build --platform linux/amd64 -t derekmitchell399/llm-app:1.0 .
> docker push derekmitchell399/llm-app:1.0
> ```

## LLMアプリケーションのテスト

アプリケーションが期待通りに動作していることを確認しましょう。

curlコマンドにアクセスできるPodを起動します：

``` bash
oc run --rm -it -n default curl --image=curlimages/curl:latest -- sh
```

次に、以下のコマンドを実行してLLMに質問を送信します：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -X "POST" \
 'http://llm-app.llm-app.svc.cluster.local:8080/askquestion' \
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

## Splunk Observability Cloudでトレースデータを表示する

Splunk Observability Cloudで、`APM`に移動し、`Service Map`を選択します。`llm-app`環境が選択されていることを確認してください。以下のようなサービスマップが表示されるはずです：

![Service Map](../images/ServiceMap.png)

右側のメニューで`Traces`をクリックします。次に、実行時間の長いトレースの1つを選択します。以下の例のように表示されるはずです：

![Trace](../images/Trace.png)

トレースには、アプリケーションがユーザーの質問（例：「NVIDIA H200のメモリはどのくらいですか？」）に対する回答を返すために実行したすべてのやり取りが表示されます。

例えば、アプリケーションがWeaviateベクトルデータベース内で当該の質問に関連するドキュメントを探すために類似検索を実行した場所を確認できます：

![Document Retrieval](../images/DocumentRetrieval.png)

また、アプリケーションがベクトルデータベースから取得したコンテキストを含め、LLMに送信するプロンプトをどのように作成したかも確認できます：

![Prompt Template](../images/PromptTemplate.png)

最後に、LLMからの応答、所要時間、使用された入力および出力トークンの数を確認できます：

![LLM Response](../images/LLMResponse.png)
