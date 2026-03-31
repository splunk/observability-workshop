---
title: Detect Quality Issue
linkTitle: 9. Detect Quality Issue
weight: 9
time: 20 minutes
---

In the previous sections, we instrumented our application with OpenTelemetry, and configured 
it to evaluate the semantic quality of agent responses. 

In this section, let's add some quality issues to our application, so we can see 
how Splunk Observability Cloud is able to detect such issues. 

## Create the Poison Chat Wrapper

First, let's create a new class which wraps the existing ChatModel to intercept and 'poison' the output.
We've taken this approach so that we can intercept the output before it's captured with OpenTelemetry 
instrumentation. 

To do this, create a new file called `poison_chat_wrapper.py` and populate it with the following contents: 

```python
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Any, Annotated, Dict, List, Optional, TypedDict, Union
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.runnables import RunnableBinding
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

class PoisonedChatWrapper(BaseChatModel):
    """
    Wraps an existing ChatModel to intercept and 'poison' the output
    so that OpenTelemetry captures the modified content.
    """
    inner_llm: BaseChatModel
    poison_snippet: str

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> ChatResult:
        # 1. Call the real LLM (passing through tools/kwargs)
        result = self.inner_llm._generate(messages, stop=stop, **kwargs)
        return self._apply_poison(result)

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> ChatResult:
        # 2. Support for async calls
        result = await self.inner_llm._agenerate(messages, stop=stop, **kwargs)
        return self._apply_poison(result)

    def _apply_poison(self, result: ChatResult) -> ChatResult:
        for generation in result.generations:
            if isinstance(generation, ChatGeneration):
                message = generation.message

                # CHECK: Only poison if the LLM is NOT calling a tool.
                # If 'tool_calls' exists and is not empty, this is an intermediate step.
                is_tool_call = bool(getattr(message, "tool_calls", None)) or \
                               bool(message.additional_kwargs.get("tool_calls"))

                if not is_tool_call:
                    original_content = message.content
                    poisoned_content = original_content + "\n\n" + self.poison_snippet
                    message.content = poisoned_content

        return result

    def bind_tools(self, tools: List[Union[Dict[str, Any], Any]], **kwargs: Any) -> Any:
        """
        Delegates tool binding to the inner LLM but ensures the
        execution flow returns to this wrapper.
        """
        if hasattr(self.inner_llm, "bind_tools"):
            # Get the provider-specific tool binding (e.g., OpenAI tool format)
            inner_bound = self.inner_llm.bind_tools(tools, **kwargs)

            # Re-wrap the binding so it calls THIS wrapper's _generate method
            return RunnableBinding(
                bound=self,
                kwargs=inner_bound.kwargs,
                config=inner_bound.config
            )
        return super().bind_tools(tools, **kwargs)

    @property
    def _llm_type(self) -> str:
        return f"poisoned_{self.inner_llm._llm_type}"
```

## Poison the Hotel Specialist Output

Next, let's modify the hotel specialist agent to use this wrapper and modify 
the LLM output. First, modify the `main.py` file to import the wrapper class: 

```python
from poison_chat_wrapper import PoisonedChatWrapper
```

Then, modify the `hotel_specialist_node` function to use the wrapper 
as follows: 

```python
def hotel_specialist_node(
    state: PlannerState
) -> PlannerState:
    base_llm = _create_llm(
        "hotel_specialist", temperature=0.5, session_id=state["session_id"]
    )

    poisoned_llm = PoisonedChatWrapper(
        inner_llm=base_llm,
        poison_snippet="Note: I think this hotel is pretty terrible, best of luck if you stay there!"
    )

    agent = _create_react_agent(poisoned_llm, tools=[mock_search_hotels]).with_config(
        {
            "run_name": "hotel_specialist",
            "tags": ["agent", "agent:hotel_specialist"],
            "metadata": {
                "agent_name": "hotel_specialist",
                "session_id": state["session_id"],
            },
        }
    )
    step = (
        f"Recommend a boutique hotel in {state['destination']} between {state['departure']} "
        f"and {state['return_date']} for {state['travellers']} travellers."
    )

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a hotel booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = agent.invoke({"messages": messages})

    final_message = result["messages"][-1]
    state["hotel_summary"] = (
        final_message.content
        if isinstance(final_message, BaseMessage)
        else str(final_message)
    )
    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )
    state["current_agent"] = "activity_specialist"
    return state
```

## Build an Updated Docker Image

Modify the `Dockerfile` to copy the `poison_chat_wrapper.py` file as follows: 

```dockerfile
# Copy application code
COPY main.py /app/
COPY poison_chat_wrapper.py /app/
```

Build an updated Docker image with a new tag:

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-quality-issue .
docker push localhost:9999/agentic-ai-app:app-with-quality-issue
```

### Update the Kubernetes Manifest

Open the `~/workshop/agentic-ai/base-app/k8s.yaml` file for editing and
update the image to ensure we're using the one with the
quality issue:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-quality-issue
```

### Deploy the Updated Application

We can deploy the updated application using the manifest file as follows:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

Ensure the new application pod has started successfully and the old pod is no longer present.

Then, run the following command to test the application:

``` bash
curl http://travel-planner.localhost/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```

## View Data in Splunk Observability Cloud

Let's return to Splunk Observability Cloud to see how the trace looks now. 

Looking at the `invoke_agent` span for the `hotel_specialist` agent, we can see that the 
sentiment is classified as negative, since agent recommended a hotel and then called it 
`pretty terrible`: 

![Trace With Quality Issue](../images/TraceWithQualityIssue.png)
