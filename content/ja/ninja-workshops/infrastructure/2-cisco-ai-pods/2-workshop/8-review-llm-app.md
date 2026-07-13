---
title: LLMアプリケーションのレビュー
linkTitle: 8. LLMアプリケーションのレビュー
weight: 8
time: 15 minutes
---

ワークショップの最後のステップでは、instructモデルとembeddingsモデルを使用するアプリケーションをOpenShiftクラスターにデプロイします。

## LangChainとは

LLMと対話するほとんどのアプリケーションと同様に、このアプリケーションはPythonで書かれています。また、[LangChain](https://www.langchain.com/)を使用しています。これはLLMを活用したアプリケーションの開発を簡素化するオープンソースのオーケストレーションフレームワークです。

## アプリケーション概要

### LLMへの接続

アプリケーションは、使用する2つのLLMに接続することから始まります。

* `meta/llama-3.2-1b-instruct`: ユーザーのプロンプトへの応答に使用
* `nvidia/llama-3.2-nv-embedqa-1b-v2`: エンベディングの計算に使用

``` python
# connect to a LLM NIM at the specified endpoint, specifying a specific model
llm = ChatNVIDIA(base_url=INSTRUCT_MODEL_URL, model="meta/llama-3.2-1b-instruct")

# Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                   base_url=EMBEDDINGS_MODEL_URL)
```

> なぜ2つのモデルがあるのでしょうか？次のたとえが参考になります。
>
> * Embeddingモデルは「図書館員」（適切な本を見つける役割）
> * Instructモデルは「作家」（本を読んで回答を書く役割）

### プロンプトテンプレートの定義

次に、アプリケーションは `meta/llama-3.2-1b-instruct` LLMとの対話に使用するプロンプトテンプレートを定義します。

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

> LLMに対して、答えがわからない場合は「わからない」と回答するよう明示的に指示している点に注目してください。これはハルシネーションの最小化に役立ちます。また、LLMが質問に回答するために使用できるコンテキストを提供するためのプレースホルダーも含まれています。

### ベクトルデータベースへの接続

次に、アプリケーションはNVIDIAデータシートのドキュメントが事前に格納されたベクトルデータベースに接続します。

``` python
    weaviate_client = weaviate.connect_to_custom(
        http_host=os.getenv('WEAVIATE_HTTP_HOST'),
        http_port=os.getenv('WEAVIATE_HTTP_PORT'),
        http_secure=False,
        grpc_host=os.getenv('WEAVIATE_GRPC_HOST'),
        grpc_port=os.getenv('WEAVIATE_GRPC_PORT'),
        grpc_secure=False
    )
        
    vector_store = WeaviateVectorStore(
        client=weaviate_client,
        embedding=embeddings_model,
        index_name="CustomDocs",
        text_key="page_content"
    )
```

### チェーンの定義

アプリケーションは **LCEL（LangChain Expression Language）** を使用してチェーンを定義します。`|`（パイプ）記号はアセンブリラインのように機能し、あるステップの出力が次のステップの入力になります。

``` python
    chain = (
        {
            "context": vector_store.as_retriever(),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
```

各ステップを順に説明します。

* **ステップ1: 入力マップ {…}**: プロンプトに必要な材料を準備します。
  * context: ベクトルストアをRetrieverに変換します。これはユーザーの質問に基づいて、NVIDIAデータシートから最も関連性の高いスニペットを検索するサーチエンジンのように機能します。
  * question: RunnablePassthrough()を使用して、ユーザーの元の質問がそのままプロンプトに渡されるようにします。
  * **注意**: これらのキー（contextとquestion）は、先ほどプロンプトテンプレートで定義した{context}と{question}のプレースホルダーに直接マッピングされます。
* **ステップ2: prompt**: これは指示書です。コンテキストと質問を受け取り、プロンプトテンプレートを使用してフォーマットします（例:「Answer the question using only the context...」）。
* **ステップ3: llm**: これは「エンジン」（GPT-4のようなもの）です。フォーマットされたプロンプトを読み取り、応答を生成します。
* **ステップ4: StrOutputParser()**: デフォルトでは、AIモデルは複雑なオブジェクトを返します。この「クリーナー」により、シンプルで読みやすいテキスト文字列が返されるようになります。

### チェーンの実行

最後に、アプリケーションはエンドユーザーの質問を入力として渡し、チェーンを実行します。

``` python
    response = chain.invoke(question)
```

これが「スタート」ボタンです。エンドユーザーの質問をパイプラインの先頭に投入すると、Retriever、プロンプト、LLMを経由して、最終的に回答が出力されます。
