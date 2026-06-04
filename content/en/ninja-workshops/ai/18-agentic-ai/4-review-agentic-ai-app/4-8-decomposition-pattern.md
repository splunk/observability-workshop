---
title: 4.8 Decomposition Pattern
linkTitle: 4.8 Decomposition Pattern
weight: 8
---

### The synthesizer shows the decomposition pattern

The final node combines the specialist outputs into one answer.

```python
def plan_synthesizer_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "plan_synthesizer", temperature=0.3, session_id=state["session_id"]
    )

    content = json.dumps(
        {
            "flight": state["flight_summary"],
            "hotel": state["hotel_summary"],
            "activities": state["activities_summary"],
        },
        indent=2,
    )

    response = llm.invoke(
        [
            SystemMessage(
                content="You are the travel plan synthesiser. Combine the specialist insights into a concise, structured itinerary."
            ),
            HumanMessage(
                content=(
                    f"Traveller request: {state['user_request']}\n\n"
                    f"Origin: {state['origin']} | Destination: {state['destination']}\n"
                    f"Dates: {state['departure']} to {state['return_date']}\n\n"
                    f"Specialist summaries:\n{content}"
                )
            ),
        ]
    )
    state["final_itinerary"] = response.content
    state["messages"].append(response)
    state["current_agent"] = "completed"
    return state
```

This is a classic pattern for agentic apps:

* decompose work into specialists
* collect intermediate outputs
* synthesize into a final response

That is one of the main architectural ideas you should take away from this overview.

### Knowledge Check

Why does the app use a separate `plan_synthesizer` node instead of letting
one agent generate the entire travel plan?

<details>
  <summary><b>Click here to see the answer</b></summary>

Because the system breaks the problem into **specialized tasks** first (flights, hotels, activities).
Each specialist produces a focused summary, and the `plan_synthesizer` node then **combines those
outputs into one coherent itinerary**.

This pattern improves **modularity, reliability, and observability**, since each agent
handles a smaller problem and the final node integrates the results.

</details>