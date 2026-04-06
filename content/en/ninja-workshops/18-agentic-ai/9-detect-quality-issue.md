---
title: Detect Quality Issue
linkTitle: 9. Detect Quality Issue
weight: 9
time: 15 minutes
---

In the previous sections, we instrumented our application with OpenTelemetry, and configured 
it to evaluate the semantic quality of agent responses. 

In this section, let's add some quality issues to our application, so we can see 
how Splunk Observability Cloud is able to detect such issues. 

## About the Poisoned Chat Wrapper

In this section, we'll use a class named `PoisonedChatWrapper` which wraps the existing 
ChatModel to intercept and 'poison' the output. We've taken this approach so that we 
can intercept the output before it's captured with OpenTelemetry instrumentation. 

If you're curious to understand this is done, please review the `poison_chat_wrapper.py` file. 

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
