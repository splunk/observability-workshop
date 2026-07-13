---
title: 4.3 Orchestration
linkTitle: 4.3 Orchestration
weight: 3
---
### Where execution begins

The main orchestration happens in `plan_travel_internal()`:

```python
def plan_travel_internal(
    origin: str,
    destination: str,
    user_request: str,
    travellers: int,
    ) -> Dict[str, object]:
    session_id = str(uuid4())
    departure, return_date = _compute_dates()

    initial_state: PlannerState = {
        "messages": [HumanMessage(content=user_request)],
        "user_request": user_request,
        "session_id": session_id,
        "origin": origin,
        "destination": destination,
        "departure": departure,
        "return_date": return_date,
        "travellers": travellers,
        "flight_summary": None,
        "hotel_summary": None,
        "activities_summary": None,
        "final_itinerary": None,
        "current_agent": "start",
    }

    workflow = build_workflow()
    compiled_app = workflow.compile()

    for step in compiled_app.stream(initial_state, config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
```

This function implements the following application lifecycle:

* build initial state
* build the graph
* compile it
* stream execution step by step

### Knowledge Check

#### Question 1

Why does the code use `compiled_app.stream(initial_state, config)` instead of
simply calling the graph once and getting the final result?

{{< details summary="Click here to see the answer" >}}
Because streaming executes the workflow **step by step as each node runs**. This lets
the application observe intermediate states, track which node is executing,
and monitor the workflow in real time instead of waiting only for the final output.
{{< /details >}}

#### Question 2

Why do we create an `initial_state` before running the graph?

{{< details summary="Click here to see the answer" >}}
Because LangGraph workflows operate on a shared state object. The `initial_state`
provides the starting data that nodes will read from, update, and pass along as
the workflow progresses.
{{< /details >}}
