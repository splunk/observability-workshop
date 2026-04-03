---
title: Agentic AI Application Architecture
linkTitle: 4. Agentic AI Application Architecture
weight: 4
time: 20 minutes
---

## Application Overview

This workshop utilizes an **Agentic AI** application for booking travel. 
Before we instrument the application with **OpenTelemetry**, it helps to 
understand how the application works.

The application is a **Flask API** that accepts a travel planning request and runs it through 
a **LangGraph** workflow made up of several LangChain-powered LLM nodes. Each node plays a specific 
role, updates shared state, and hands off to the next step.

In this part of the workshop, we will review:

* the request lifecycle 
* the shared state model 
* how LangGraph nodes work 
* the LangChain abstractions used in the code 
* where observability will matter later

### What the application does

At a high level, the application accepts a request and turns it into a multi-step workflow:

* coordinator
* flight specialist 
* hotel specialist 
* activity specialist 
* synthesizer

The main flow looks like this:

```python
@app.route("/travel/plan", methods=["POST"])
def plan():
    data = request.get_json()

    origin = data.get("origin", "Seattle")
    destination = data.get("destination", "Paris")
    user_request = data.get(
        "user_request",
        f"Planning a week-long trip from {origin} to {destination}. "
        "Looking for boutique hotel, flights and unique experiences.",
    )
    travellers = int(data.get("travellers", 2))

    result = plan_travel_internal(
        origin=origin,
        destination=destination,
        user_request=user_request,
        travellers=travellers
    )

    return jsonify(result), 200
```

A helpful way to explain this is:

1. Flask receives the request 
2. `plan_travel_internal()` builds the workflow state 
3. LangGraph executes the nodes 
4. each node updates the state 
5. the final itinerary is returned as JSON

### Shared State in LangGraph

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

It is also worth highlighting this field:

```python
messages: Annotated[List[AnyMessage], add_messages]
```

This tells LangGraph to append new messages rather than overwrite the list. That is how 
the application preserves conversation history across steps.

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

### How the graph is defined

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

### How a node works

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

### LangChain concepts used in the nodes

The application uses LangChain message abstractions rather than one long prompt string.

``` python
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
```

This is important because each node can separate:

* system role
* user task
* model response

For example:

```python
messages = [
    SystemMessage(content="You are a flight booking specialist. Provide concise options."),
    HumanMessage(content=step),
]
result = llm.invoke(messages)
```

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

