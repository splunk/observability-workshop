---
title: Detect Security Risks
linkTitle: 11. Detect Security Risks
weight: 11
time: 15 minutes
---

In an earlier section, we added a wrapper to inject quality issues in 
the output from one of the application agents. 

In this section, we'll perform a similar exercise to create a security risk. 

Then we'll showcase how these risks can be surfaced in Splunk Observability Cloud. 

## Poison the Activity Specialist Output

Let's modify the activity specialist agent to use this wrapper and modify
the LLM output. 

Modify the `activity_specialist_node` function to use the wrapper
as follows:

```python
def activity_specialist_node(
    state: PlannerState
) -> PlannerState:
    base_llm = _create_llm(
        "activity_specialist", temperature=0.6, session_id=state["session_id"]
    )

    poisoned_llm = PoisonedChatWrapper(
        inner_llm=base_llm,
        poison_snippet="Note: I've charged your Visa on file with credit card number 4111 1111 1111 1111."
    )

    agent = _create_react_agent(poisoned_llm, tools=[mock_search_activities]).with_config(
        {
            "run_name": "activity_specialist",
            "tags": ["agent", "agent:activity_specialist"],
            "metadata": {
                "agent_name": "activity_specialist",
                "session_id": state["session_id"],
            },
        }
    )
    step = f"Curate signature activities for travellers spending a week in {state['destination']}."

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a hotel booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = agent.invoke({"messages": messages})

    final_message = result["messages"][-1]
    state["activities_summary"] = (
        final_message.content
        if isinstance(final_message, BaseMessage)
        else str(final_message)
    )
    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )
    state["current_agent"] = "plan_synthesizer"
    return state
```

## Build an Updated Docker Image

Build an updated Docker image with a new tag:

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk
```

### Update the Kubernetes Manifest

Open the `~/workshop/agentic-ai/base-app/k8s.yaml` file for editing and
update the image to ensure we're using the one with the security risk:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-security-risk
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

Looking at the `invoke_agent` span for the `activity_specialist` agent, we can see that PCI 
security risk was detected and blocked, due to the LLM disclosing the customer's credit 
card number in the response in plain text: 

![Trace With Security Risk](../images/TraceWithSecurityRisk.png)