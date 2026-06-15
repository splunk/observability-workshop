---
title: LLM アプリケーションのレビュー
linkTitle: 8. LLM アプリケーションのレビュー
weight: 8
time: 15 minutes
---

ワークショップの最後のステップでは、instruct モデルと embeddings モデルを使用するアプリケーションを OpenShift クラスターにデプロイします。

## LangChain とは？

LLM と対話するほとんどのアプリケーションと同様に、このアプリケーションは Python で書かれています。また、[LangChain](https://www.langchain.com/) を使用しています。LangChain は、LLM を活用したアプリケーションの開発を簡素化するオープンソースのオーケストレーションフレームワークです。

## アプリケーション概要

### LLM への接続

アプリケーションは、使用する2つの LLM に接続することから始まります

* `meta/llama-3.2-1b-instruct`: ユーザープロンプトへの応答に使用します
* `nvidia/llama-3.2-nv-embedqa-1b-v2`: エンベディングの計算に使用します

``` python
# connect to a LLM NIM at the specified endpoint, specifying a specific model
llm = ChatNVIDIA(base_url=INSTRUCT_MODEL_URL, model="meta/llama-3.2-1b-instruct")

# Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                   base_url=EMBEDDINGS_MODEL_URL)
```

> なぜ2つのモデルがあるのでしょうか？以下のアナロジーが参考になります
>
> * Embedding モデルは「図書館司書」です（適切な本を見つける手助けをします）
> * Instruct モデルは「作家」です（本を読んで回答を書きます）

### プロンプトテンプレートの定義

次に、アプリケーションは `meta/llama-3.2-1b-instruct` LLM とのやり取りで使用するプロンプトテンプレートを定義します

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

> LLM に対して、答えがわからない場合は「わからない」と明示的に言うよう指示していることに注目してください。これはハルシネーションを最小限に抑えるのに役立ちます。また、LLM が質問に回答するために使用できるコンテキストを提供するためのプレースホルダーもあります。

### ベクトルデータベースへの接続

次に、アプリケーションは NVIDIA データシートドキュメントが事前に登録されたベクトルデータベースに接続します

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

アプリケーションは **LCEL (LangChain Expression Language)** を使用してチェーンを定義します。`|`（パイプ）記号は組み立てラインのように機能し、あるステップの出力が次のステップの入力になります。

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

各ステップを詳しく見ていきましょう

* **ステップ 1: 入力マップ {…}**: プロンプトの材料を準備します。
  * context: ベクトルストアをリトリーバーに変換します。これはユーザーの質問に基づいて NVIDIA データシートから最も関連性の高いスニペットを検索する検索エンジンとして機能します。
  * question: RunnablePassthrough() を使用して、ユーザーの元の質問がそのままプロンプトに渡されるようにします。
  * **注意**: これらのキー（context と question）は、先ほどプロンプトテンプレートで定義した {context} と {question} のプレースホルダーに直接マッピングされます。
* **ステップ 2: prompt**: これは指示書です。context と question を受け取り、プロンプトテンプレートを使用してフォーマットします（例：「コンテキストのみを使用して質問に回答してください...」）。
* **ステップ 3: llm**: これは「エンジン」です（GPT-4 のようなもの）。フォーマットされたプロンプトを読み取り、応答を生成します。
* **ステップ 4: StrOutputParser()**: デフォルトでは、AI モデルは複雑なオブジェクトを返します。この「クリーナー」により、シンプルで読みやすいテキスト文字列が返されるようになります。

### チェーンの呼び出し

最後に、アプリケーションはエンドユーザーの質問を入力として渡してチェーンを呼び出します

``` python
    response = chain.invoke(question)
```

これは「スタート」ボタンです。エンドユーザーの質問をパイプラインの先頭に投入すると、リトリーバー、プロンプト、LLM を順に通過して、最終的に回答が出力されます。
