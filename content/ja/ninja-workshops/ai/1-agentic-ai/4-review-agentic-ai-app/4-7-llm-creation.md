---
title: 4.7 LLMの作成
linkTitle: 4.7 LLMの作成
weight: 7
---

## LLMの作成

LLM自体はここで作成されます

```python
def _create_llm(agent_name: str, *, temperature: float, session_id: str) -> AzureChatOpenAI:
    azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    return AzureChatOpenAI(
        azure_deployment=azure_deployment_name,
        openai_api_version=azure_openai_api_version,
        temperature=temperature,
        model_name = azure_deployment_name,
        # AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables will be used to connect to the LLM
    )
```

このアプローチでは、モデルの設定をワークフローロジックから分離しています。
各ノードは、どの程度決定論的または創造的であるべきかに応じて、異なるtemperatureを使用できます。

### 理解度チェック

OpenAI（Azure OpenAIではなく）用のLLMをどのように作成しますか？

<details>
  <summary><b>クリックして回答を表示</b></summary>

OpenAI用のLLMの作成にはいくつかの違いがあります。関数は `AzureChatOpenAI` の代わりに `ChatOpenAI` オブジェクトを返します。

OpenAIを直接使用する場合、Azure固有のパラメータ（`azure_deployment`、`openai_api_version`、`Azure endpoint`）は使用しません。代わりに、モデル名を指定し、標準の `OPENAI_API_KEY` 環境変数を使用します。

以下は例です

```python
def _create_llm(agent_name: str, *, temperature: float, session_id: str) -> ChatOpenAI:
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        # Uses OPENAI_API_KEY automatically from environment
    )
```

</details>
