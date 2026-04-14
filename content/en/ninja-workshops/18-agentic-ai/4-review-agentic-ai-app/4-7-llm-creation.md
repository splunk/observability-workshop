---
title: 4.7 LLM Creation
linkTitle: 4.7 LLM Creation
weight: 7
---

## LLM Creation 

The LLM itself is created here:

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

This approach separates model configuration from workflow logic.
Different nodes can use different temperatures depending on how deterministic or
creative they should be.

### Knowledge Check

How would you create an LLM for OpenAI (rather than Azure OpenAI?)

<details>
  <summary><b>Click here to see the answer</b></summary>

Creating an LLM for OpenAI has a few differences. The function would return a `ChatOpenAI` 
object instead of `AzureChatOpenAI`. 

With OpenAI directly, you don’t use the Azure-specific parameters (`azure_deployment`, 
`openai_api_version`, `Azure endpoint`). Instead, you specify the model name and rely 
on the standard `OPENAI_API_KEY` environment variable.

Here's an example: 

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