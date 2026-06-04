---
title: 4.2 Shared State
linkTitle: 4.2 Shared State
weight: 2
---

## Shared State in LangGraph

The most important LangGraph concept in this app is the shared state object:

```python
class PlannerState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_request: str
    session_id: str
    origin: str
    destination: str
    departure: str
    return_date: str
    travellers: int
    flight_summary: Optional[str]
    hotel_summary: Optional[str]
    activities_summary: Optional[str]
    final_itinerary: Optional[str]
    current_agent: str
```

This state moves through the graph from node to node.

Each node:

* reads values from state
* does some work
* writes new values back to state
* sets current_agent to control what happens next

This is a key LangGraph mental model: **stateful workflow orchestration**.

### Knowledge Check

How would you explain the syntax used for the `messages` field?

```python
messages: Annotated[List[AnyMessage], add_messages]
```

<details>
  <summary><b>Click here to see the answer</b></summary>

`messages: Annotated[List[AnyMessage], add_messages]` does two things.

* `List[AnyMessage]` defines the **type** of the field: it’s a list of LangChain message objects (system, human, or AI messages).
* `Annotated[..., add_messages]` adds **LangGraph behavior** that tells the graph **how updates to this field should be handled**.

Specifically, `add_messages` means that when a node writes new messages, LangGraph will **append them to the existing list instead of overwriting it**.
So the conversation history grows as each node adds messages.

</details>
