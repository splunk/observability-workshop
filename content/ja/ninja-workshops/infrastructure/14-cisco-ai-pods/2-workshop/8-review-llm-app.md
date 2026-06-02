---
title: LLM アプリケーションの確認
linkTitle: 8. LLM アプリケーションの確認
weight: 8
time: 15 minutes
---

ワークショップの最後のステップでは、instruct モデルと embeddings モデルを使用するアプリケーションを OpenShift クラスターにデプロイします。

## LangChain とは

LLM とやり取りするほとんどのアプリケーションと同様に、このアプリケーションも Python で書かれています。また、[LangChain](https://www.langchain.com/) を使用しています。LangChain は、LLM を活用したアプリケーションの開発を簡素化するオープンソースのオーケストレーションフレームワークです。

## アプリケーションの概要

### LLM への接続

アプリケーションはまず、使用する 2 つの LLM に接続します。

* `meta/llama-3.2-1b-instruct`: ユーザープロンプトへの応答に使用
* `nvidia/llama-3.2-nv-embedqa-1b-v2`: embeddings の計算に使用

``` python
# connect to a LLM NIM at the specified endpoint, specifying a specific model
llm = ChatNVIDIA(base_url=INSTRUCT_MODEL_URL, model="meta/llama-3.2-1b-instruct")

# Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                   base_url=EMBEDDINGS_MODEL_URL)
```

> なぜ 2 つのモデルがあるのでしょうか？ わかりやすい例えを紹介します。
>
> * Embedding モデルは「司書」のような役割です（適切な本を見つける手助けをします）。
> * Instruct モデルは「執筆者」のような役割です（本を読んで回答を書きます）。

### プロンプトテンプレートの定義

次に、アプリケーションは `meta/llama-3.2-1b-instruct` LLM とのやり取りで使用するプロンプトテンプレートを定義します。

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

> LLM に対して、答えを知らない場合は知らないと明示的に答えるように指示している点に注目してください。これによりハルシネーションを最小限に抑えることができます。また、LLM が質問に答える際に使用できるコンテキストを提供するためのプレースホルダーも用意されています。

### ベクトルデータベースへの接続

次に、アプリケーションは NVIDIA データシートのドキュメントが事前に格納されたベクトルデータベースに接続します。

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

### Chain の定義

アプリケーションは **LCEL (LangChain Expression Language)** を使用して chain を定義します。`|` (パイプ) 記号は組み立てラインのように動作し、あるステップの出力が次のステップの入力になります。

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

これをステップごとに見ていきましょう。

* **ステップ 1: 入力マップ {…}**: プロンプトのための材料を準備します。
  * context: ベクトルストアを retriever に変換します。これは検索エンジンのように動作し、ユーザーの質問に基づいて NVIDIA データシートから最も関連性の高い箇所を見つけます。
  * question: `RunnablePassthrough()` を使用して、ユーザーの元の質問がプロンプトに直接渡されるようにします。
  * **注意**: これらのキー (context と question) は、先ほどプロンプトテンプレートで定義した `{context}` と `{question}` のプレースホルダーに直接対応しています。
* **ステップ 2: prompt**: これは指示書です。コンテキストと質問を受け取り、プロンプトテンプレートを使用してフォーマットします (例: "Answer the question using only the context...")。
* **ステップ 3: llm**: これは「エンジン」です (GPT-4 のようなもの)。フォーマットされたプロンプトを読み取り、応答を生成します。
* **ステップ 4: StrOutputParser()**: デフォルトでは、AI モデルは複雑なオブジェクトを返します。この「クリーナー」により、シンプルで読みやすいテキスト文字列を取得できます。

### Chain の呼び出し

最後に、アプリケーションはエンドユーザーの質問を入力として渡すことで chain を呼び出します。

``` python
    response = chain.invoke(question)
```

これは「スタート」ボタンです。エンドユーザーの質問をパイプラインの最初に投入すると、retriever、prompt、LLM を経由して、最終的に答えが反対側から出てきます。
