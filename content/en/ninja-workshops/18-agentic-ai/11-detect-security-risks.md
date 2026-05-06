---
title: Detect Security Risks
linkTitle: 11. Detect Security Risks
weight: 11
time: 15 minutes
---

> Note: this section of the workshop requires changes to multiple files.
> If you're not sure where to make the changes, or your application is no
> longer working, please refer to the model solution for this section
> which is in the `~/workshop/agentic-ai/app-with-security-risk` folder.

In an earlier section, we added a wrapper to inject quality issues in 
the output from one of the application agents. 

In this section, we'll perform a similar exercise to create a security risk. 

Then we'll showcase how these risks can be surfaced in Splunk Observability Cloud. 

## Poison the Activity Specialist Output

Let's modify the activity specialist agent to use this wrapper and modify
the LLM output. 

Open the `~/workshop/agentic-ai/base-app/main.py` file for editing.

Replace the definition of the `activity_specialist_node` function with the version included below. 
This effectively simulates a scenario where the LLM has 
included the user's credit card number as part of the response, which is 
a clear security risk and PCI violation. 

> Tip: to delete a large number of lines in bulk using the `vi` editor, press `Shift` + `v` to ensure `Visual 
> Line` mode, then use the down arrow to select all the lines you want to delete, then press `d`
> to delete the selected lines.

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

> Hint: run the following command to compare your changes with the model solution:
>
> `diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-security-risk/main.py`

## Build an Updated Docker Image

Build an updated Docker image with a new tag:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk
```

> Tip: if the image is taking too long to build, consider using the pre-built
> image instead. To do so, update the image name in
> the `~/workshop/agentic-ai/base-app/k8s.yaml` file to `ghcr.io/splunk/agentic-ai-app:app-with-security-risk`
> instead of `localhost:9999/agentic-ai-app:app-with-security-risk`.

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

Ensure the new application pod has started successfully and the old pod is no longer present:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
````

{{% /tab %}}
{{< /tabs >}}

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

## View Events in Cisco AI Defense

Workshop attendees won’t be able to log in to the AI Defense application directly. 
However, if we were able to view the AI Defense dashboard, we would see that an 
event was logged for this request and that the credit card number included in the 
prompt was automatically redacted.

![AI Defense Events](../images/AIDefenseEvents.png)

Note that policies can be configured AI Defense to specify whether we want to monitor
or block specific types of security issues. In this case, we've chosen to just monitor
PCI-related issues.

## View Data in Splunk Observability Cloud

Let's return to Splunk Observability Cloud to see how the trace looks now.

Navigate to `APM` and then select `AI agents`. Ensure your environment name
is selected (e.g. `agentic-ai-$INSTANCE`). You'll notice that the page
includes security risks now!

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

> You should also see the security risks on the `AI overview` page, as well as the 
> `AI agent` page for the `plan_synthesizer` agent. 

Navigate to `APM -> AI trace data` and load the most recent trace.

In the agent flow, we can see that a security risk was detected: 

![Agent Flow With Security Risk](../images/AgentFlowWithSecurityRisk.png)

Looking at the `invoke_agent` span for the `activity_specialist` agent, we can see that PCI
security risk was detected and blocked, due to the LLM disclosing the customer's credit
card number in the response in plain text:

![Trace With Security Risk](../images/TraceWithSecurityRisk.png)

Clicking on the security risk provides additional details, along with a link 
to view the event in Cisco AI Defense: 

![Security Risk Details](../images/SecurityRiskDetails.png)

And if we view the `Span details` for this span, we can see that the 
`gen_ai.security.event_id` attribute is included with this span: 

![Security Event Span Attribute](../images/SecurityEventSpanAttribute.png)

This attribute allows us to correlate the span in Splunk Observability Cloud 
with the corresponding event in Cisco AI Defense. 
