---
title: 4.1 Request Lifecycle
linkTitle: 4.1 Request Lifecycle
weight: 1
---

## What the application does

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

### Knowledge Check

Where does the LangGraph workflow actually start executing in this API flow?

{{< details summary="Click here to see the answer" >}}
It starts inside `plan_travel_internal()`. The Flask route only receives
the request and extracts parameters. `plan_travel_internal()` initializes
the workflow state and invokes the LangGraph graph, which then runs the nodes
(coordinator, specialists, synthesizer) that update the state until
the final itinerary is produced.
{{< /details >}}