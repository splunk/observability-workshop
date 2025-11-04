from models.schemas import GraphState, FulfillmentResult

def fulfill(state: GraphState) -> GraphState:
    # Decide channel: pickup vs delivery based on customer or config.
    result = FulfillmentResult(status="ready_for_pickup", location_id="LOC-SEA-01")
    return {"fulfillment": result, "next": "notify"}