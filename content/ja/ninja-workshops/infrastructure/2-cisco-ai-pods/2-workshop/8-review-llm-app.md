---
title: LLM アプリケーションの確認
linkTitle: 8. LLM アプリケーションの確認
weight: 8
time: 15 minutes
---

ワークショップの最後のステップでは、instruct モデルと embeddings モデルを使用するアプリケーションを OpenShift クラスターにデプロイします。

## LangChain とは？

LLM とやり取りするほとんどのアプリケーションと同様に、このアプリケーションは Python で書かれています。また、LLM を活用したアプリケーションの開発を簡素化するオープンソースのオーケストレーションフレームワークである [LangChain](https://www.langchain.com/) を使用しています。

## アプリケーション概要

### LLM への接続

アプリケーションはまず、使用する2つの LLM に接続します：

* `meta/llama-3.2-1b-instruct`：ユーザーのプロンプトへの応答に使用
* `nvidia/llama-3.2-nv-embedqa-1b-v2`：埋め込みの計算に使用

``` python
# connect to a LLM NIM at the specified endpoint, specifying a specific model
llm = ChatNVIDIA(base_url=INSTRUCT_MODEL_URL, model="meta/llama-3.2-1b-instruct")

# Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                   base_url=EMBEDDINGS_MODEL_URL)
```
> なぜ2つのモデルがあるのでしょうか？以下のたとえが参考になります：
> * Embedding モデルは「図書館員」です（適切な本を見つける手助けをします）
> * Instruct モデルは「作家」です（本を読み、答えを書きます）

### プロンプトテンプレートの定義

アプリケーションは次に、`meta/llama-3.2-1b-instruct` LLM とのやり取りで使用するプロンプトテンプレートを定義します：

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

> LLM に対して、答えがわからない場合はわからないと言うように明示的に指示していることに注目してください。これはハルシネーションを最小限に抑えるのに役立ちます。また、LLM が質問に答えるために使用できるコンテキストを提供するためのプレースホルダーもあります。

### ベクターデータベースへの接続

アプリケーションは次に、NVIDIA のデータシートドキュメントが事前に格納されたベクターデータベースに接続します：

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

これをステップごとに分解してみましょう：

* **ステップ1：入力マップ {…}**：プロンプトの材料を準備しています。
  * context：ベクターストアをリトリーバーに変換します。これはユーザーの質問に基づいて、NVIDIA データシートから最も関連性の高いスニペットを見つける検索エンジンのように機能します。
  * question：RunnablePassthrough() を使用して、ユーザーの元の質問がそのままプロンプトに渡されるようにします。
  * **注意**：これらのキー（context と question）は、先ほど定義したプロンプトテンプレートの {context} と {question} プレースホルダーに直接対応しています。
* **ステップ2：prompt**：これは指示書です。context と question を受け取り、プロンプトテンプレートを使用してフォーマットします（例：「コンテキストのみを使用して質問に答えてください...」）。
* **ステップ3：llm**：これは「エンジン」です（GPT-4 のようなもの）。フォーマットされたプロンプトを読み取り、レスポンスを生成します。
* **ステップ4：StrOutputParser()**：デフォルトでは、AI モデルは複雑なオブジェクトを返します。この「クリーナー」により、シンプルで読みやすいテキスト文字列が返されるようになります。

### チェーンの実行

最後に、アプリケーションはエンドユーザーの質問を入力として渡してチェーンを実行します：

``` python
    response = chain.invoke(question)
```

これが「スタート」ボタンです。エンドユーザーの質問をパイプラインの最初に投入すると、リトリーバー、プロンプト、LLM を経由して、最終的に答えが出力されます。
