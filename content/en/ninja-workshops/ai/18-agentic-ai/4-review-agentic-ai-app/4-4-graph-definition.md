---
title: 4.4 Defining the Graph
linkTitle: 4.4 Defining the Graph
weight: 4
---

## How the graph is defined

The graph is built explicitly in `build_workflow()`:

```python
def build_workflow() -> StateGraph:
    graph = StateGraph(PlannerState)
    graph.add_node("coordinator", lambda state: coordinator_node(state))
    graph.add_node("flight_specialist", lambda state: flight_specialist_node(state))
    graph.add_node("hotel_specialist", lambda state: hotel_specialist_node(state))
    graph.add_node("activity_specialist", lambda state: activity_specialist_node(state))
    graph.add_node("plan_synthesizer", lambda state: plan_synthesizer_node(state))
    graph.add_conditional_edges(START, should_continue)
    graph.add_conditional_edges("coordinator", should_continue)
    graph.add_conditional_edges("flight_specialist", should_continue)
    graph.add_conditional_edges("hotel_specialist", should_continue)
    graph.add_conditional_edges("activity_specialist", should_continue)
    graph.add_conditional_edges("plan_synthesizer", should_continue)
    return graph
```

And the routing logic is here:

```python
def should_continue(state: PlannerState) -> str:
    mapping = {
    "start": "coordinator",
    "flight_specialist": "flight_specialist",
    "hotel_specialist": "hotel_specialist",
    "activity_specialist": "activity_specialist",
    "plan_synthesizer": "plan_synthesizer",
    }
    return mapping.get(state["current_agent"], END)
```

Even though this uses conditional edges, the workflow is effectively linear:

* start
* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer
* end

### Knowledge Check

If the workflow is effectively linear, why does the graph still use
`add_conditional_edges` and the `should_continue()` router?

<details>
  <summary><b>Click here to see the answer</b></summary>

Because it makes the workflow **flexible and extensible**. Even though the current flow
is linear, the routing function allows the graph to dynamically decide the next node
based on the state. This makes it easy to add branching, retries, or different
execution paths later without redesigning the graph.

</details>