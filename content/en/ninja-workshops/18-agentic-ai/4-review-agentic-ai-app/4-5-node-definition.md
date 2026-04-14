---
title: 4.5 Defining Nodes
linkTitle: 4.5 Defining Nodes
weight: 5
---

## How a node works

A LangGraph node in this app is just a Python function that accepts state and returns updated state.

For example, the flight specialist:

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )

    step = (
        f"Find an appealing flight from {state['origin']} to {state['destination']} "
        f"departing {state['departure']} for {state['travellers']} travellers."
    )

    messages = [
        SystemMessage(content="You are a flight booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = llm.invoke(messages)
    state["flight_summary"] = result.content
    state["messages"].append(result)
    state["current_agent"] = "hotel_specialist"
    return state
```

This exhibits the common node pattern:

1. create or access an LLM
2. build a prompt from structured state
3. invoke the model
4. save the result into state
5. set the next node

The hotel and activity nodes follow the same structure, which makes the workflow easy to explain.

### Knowledge Check

When creating the LLM for the `flight_specialist` node, we specified 
a temperature of `0.4`. What does this mean? 

<details>
  <summary><b>Click here to see the answer</b></summary>

Temperature controls how random or creative the model’s responses are.

* **Lower temperature (e.g., 0.0–0.3)**: more deterministic and consistent responses
* **Medium (around 0.4–0.7)**: balanced between accuracy and creativity
* **Higher (0.8+)**: more diverse and creative, but less predictable

So setting **temperature=0.4** means the `flight_specialist` agent will produce 
responses that are **mostly consistent and reliable, with a small amount of 
variation**, which useful for tasks that need correctness but not completely rigid answers.

</details>