---
title: Review the Agentic AI Application
linkTitle: 4. Review the Agentic AI Application
weight: 4
time: 20 minutes
---

## Goals of this Section

This workshop utilizes an **Agentic AI** application. Before we instrument the application with **OpenTelemetry**, 
we want workshop attendees to understand how the application works.

This walkthrough explains the core concepts the application uses:

* **LangChain** message abstractions
* **LangGraph** state and workflow orchestration
* **Multi-agent** decomposition
* **LLM invocation** patterns
* The r**equest lifecycle** from API to final response

By the end of this section, attendees should be able to explain how a request moves through the 
application and identify the major boundaries we may later instrument.

## Application Overview 

At a high level, the application accepts a travel-planning request and sends it through a sequence
of AI specialists. One agent coordinates, then other agents focus on flights, hotels, and 
activities, and finally one agent synthesizes everything into a final itinerary.

So the mental model I want you to have is:

1. a request comes in,
2. the workflow builds state,
3. a graph executes several nodes,
4. each node updates the state,
5. and the app returns the final itinerary.

That architecture will matter a lot once we start asking observability questions like:

* Which node is currently running?
* How long did each step take?
* Which LLM call failed?
* What information was passed from one step to the next?

### Request Lifecycle 

Let’s start from the outside and work inward.

The application exposes a Flask endpoint at `/travel/plan`.

A client sends a POST request with fields like:

* origin
* destination
* user_request
* travellers

The Flask route parses the incoming JSON, sets defaults if needed, and then calls the 
internal orchestration function: `plan_travel_internal()`.

That function is really the runtime entry point for the AI workflow. Inside this function, the application:

1. generates a session_id
2. computes trip dates
3. constructs the initial PlannerState
4. builds the LangGraph workflow
5. compiles it
6. executes it step by step
7. collects the final result and returns JSON

This gives us an important separation of concerns:

* Flask handles HTTP
* LangGraph handles orchestration
* LangChain handles model-facing abstractions

That separation is worth calling out early because it gives us clean mental boundaries for the rest of the code review.

### Shared State Model 

The most important concept in this application is the shared state object: `PlannerState`.

This is a `TypedDict` that defines the data moving through the graph.

It includes things like:

* user_request
* origin
* destination
* departure
* return_date
* travellers
* flight_summary
* hotel_summary
* activities_summary
* final_itinerary
* current_agent
* messages

If you only remember one LangGraph concept from this review, remember this:

**LangGraph workflows are fundamentally state-driven.**

Each node reads from shared state, does some work, writes updates back into shared state, and then the graph decides what happens next.

This is different from a simple prompt chain where one string is passed into the next model call. Here we have a structured memory object that persists across the workflow.

One especially interesting field is `messages`.

It is defined with:

````
Annotated[List[AnyMessage], add_messages]
````

That tells LangGraph that when messages are updated, they should be appended rather than overwritten.

This matters because the app is preserving conversational context as it moves through the workflow.

So if attendees ask, “Where is the memory in this app?” the answer is:

* partly in the explicit structured fields like `origin` and `flight_summary`
* and partly in the messages list that records the conversational history

### Workflow Graph 

Now let’s look at how the workflow is organized.

The graph is built in `build_workflow()`.

This function:
1. creates a StateGraph using PlannerState 
2. adds named nodes 
3. adds conditional edges 
4. compiles later into an executable workflow

The node sequence is:

* coordinator
* flight_specialist
* hotel_specialist
* activity_specialist
* plan_synthesizer

Even though the graph uses conditional routing, the current implementation is effectively linear.

The should_continue() function checks the current_agent field in state and maps it to the next node.

So the execution path is essentially:

* START
* coordinator
* flight specialist
* hotel specialist
* activity specialist
* plan synthesizer
* END

