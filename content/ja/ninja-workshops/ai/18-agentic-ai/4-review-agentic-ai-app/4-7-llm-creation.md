---
title: 4.7 LLM Creation
linkTitle: 4.7 LLM Creation
weight: 7
---

## LLM の作成

LLM 自体は次の場所で作成されます。

```python
def _create_llm(agent_name: str, *, temperature: float, session_id: str) -> ChatOpenAI:
    """Create an ChatOpenAI instance."""

    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1-mini")

    return ChatOpenAI(
        model = model_name,
        temperature = temperature,
        # Uses OPENAI_API_KEY automatically from environment
    )
```

このアプローチでは、モデルの設定をワークフローのロジックから分離しています。各ノードがどの程度決定論的であるべきか、あるいはどの程度創造的であるべきかに応じて、異なる temperature を使用できます。

### 知識の確認

OpenAI ではなく Azure OpenAI 用の LLM を作成するには、どうすればよいでしょうか？

<details>
  <summary><b>クリックして回答を表示</b></summary>

Azure OpenAI 用の LLM を作成する場合、いくつか違いがあります。関数は `ChatOpenAI` ではなく `AzureChatOpenAI` オブジェクトを返します。

また、Azure 固有のパラメーター（`azure_deployment`、`openai_api_version`、`Azure endpoint`）も必要になります。以下に例を示します。

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

</details>
