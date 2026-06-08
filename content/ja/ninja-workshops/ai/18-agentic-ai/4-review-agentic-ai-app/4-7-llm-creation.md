---
title: 4.7 LLM の作成
linkTitle: 4.7 LLM の作成
weight: 7
---

## LLM の作成

LLM 自体はここで作成されます

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

このアプローチにより、モデルの設定がワークフローのロジックから分離されます。
異なるノードは、どの程度決定論的であるべきか、または創造的であるべきかに応じて、異なる temperature を使用できます。

### 知識チェック

Azure OpenAI（OpenAI ではなく）用の LLM を作成するにはどうすればよいですか？

{{< details summary="クリックして回答を表示" >}}
Azure OpenAI 用の LLM を作成するにはいくつかの違いがあります。この関数は `ChatOpenAI` の代わりに `AzureChatOpenAI` オブジェクトを返します。

また、Azure 固有のパラメータ（`azure_deployment`、`openai_api_version`、`Azure endpoint`）も必要になります。以下に例を示します

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

{{< /details >}}
