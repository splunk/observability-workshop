"""
Multi-agent travel planner driven by LangGraph.

The example coordinates a set of LangChain agents that collaborate to build a
week-long city break itinerary.

[User Request] --> [Pre-Parse: origin/dest/dates] --> START
                    |
                    v
              [LangGraph Workflow]
    ┌──────────┼──────────┼──────────┼──────────┐
    |          |          |          |          |
[Coord] --> [Flight] --> [Hotel] --> [Act.] --> [Synth] --> END
    |          |          |          |          |
    └──────────┼──────────┼──────────┼──────────┘
               |          |          |
          (OTEL Spans/Metrics)
"""

from __future__ import annotations

import json
import httpx
import os
import random
import sys
from datetime import datetime, timedelta
from typing import Annotated, Dict, List, Optional, TypedDict
from uuid import uuid4
from pprint import pprint
from typing import Union

from flask import Flask, request, jsonify
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages

from langchain_core.messages import convert_to_messages

# Begin: Add Import Statements

# End: Add Import Statements

import logging

logging.basicConfig(level=logging.INFO)


DESTINATIONS = {
    "paris": {
        "country": "France",
        "currency": "EUR",
        "airport": "CDG",
        "highlights": [
            "Eiffel Tower at sunset",
            "Seine dinner cruise",
            "Day trip to Versailles",
        ],
    },
    "tokyo": {
        "country": "Japan",
        "currency": "JPY",
        "airport": "HND",
        "highlights": [
            "Tsukiji market food tour",
            "Ghibli Museum visit",
            "Day trip to Hakone hot springs",
        ],
    },
    "rome": {
        "country": "Italy",
        "currency": "EUR",
        "airport": "FCO",
        "highlights": [
            "Colosseum underground tour",
            "Private pasta masterclass",
            "Sunset walk through Trastevere",
        ],
    },
}

def _compute_dates() -> tuple[str, str]:
    start = datetime.now() + timedelta(days=30)
    end = start + timedelta(days=7)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

# Begin: Tool Definitions

# End: Tool Definitions


# ---------------------------------------------------------------------------
# LangGraph state & helpers
# ---------------------------------------------------------------------------


class PlannerState(TypedDict):
    """Shared state that moves through the LangGraph workflow."""

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

def _create_llm(agent_name: str, *, temperature: float, session_id: str) -> AzureChatOpenAI:
    """Create an AzureChatOpenAI instance."""

    azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    # Azure OpenAI Configuration
    return AzureChatOpenAI(
        azure_deployment = azure_deployment_name,
        openai_api_version = azure_openai_api_version,
        temperature = temperature,
        model_name = azure_deployment_name,
        # AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables will be used to connect to the LLM
    )


# ---------------------------------------------------------------------------
# Pretty Printing Utilities
# ---------------------------------------------------------------------------


def pretty_print_message(message, indent=False):
    """Pretty print a single langchain message."""
    try:
        pretty_message = message.pretty_repr(html=False)
        if not indent:
            logging.info(pretty_message)
            return

        indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
        logging.info(indented)
    except Exception:
        # Fallback if pretty_repr fails
        logging.error(f"Message: {message}")


def pretty_print_messages(update, last_message=False):
    """Pretty print messages from a workflow update."""
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        logging.info(f"\n🔹 Update from subgraph {graph_id}:")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"📍 Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        logging.info(f"\n{update_label}")

        # Check if node_update has messages
        if "messages" in node_update:
            try:
                messages = convert_to_messages(node_update["messages"])
                if last_message:
                    messages = messages[-1:]

                for m in messages:
                    pretty_print_message(m, indent=is_subgraph)
            except Exception as e:
                logging.error(
                    f"  (Could not pretty print messages: {e})"
                )

# ---------------------------------------------------------------------------
# LangGraph nodes
# ---------------------------------------------------------------------------


def coordinator_node(state: PlannerState) -> PlannerState:
    llm = _create_llm("coordinator", temperature=0.2, session_id=state["session_id"])

    system_message = SystemMessage(
        content=(
            "You are the lead travel coordinator. Extract the key details from the "
            "traveller's request and describe the plan for the specialist agents."
        )
    )

    result = llm.invoke([system_message] + list(state["messages"]))
    final_message = result
    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )
    state["current_agent"] = "flight_specialist"
    return state


def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
        "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )

    step = (
        f"Find an appealing flight from {state['origin']} to {state['destination']} "
        f"departing {state['departure']} for {state['travellers']} travellers."
    )

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a flight booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = llm.invoke(messages)
    final_message = result
    state["flight_summary"] = final_message.content if isinstance(final_message, BaseMessage) else str(final_message)
    state["messages"].append(final_message if isinstance(final_message, BaseMessage) else AIMessage(content=str(final_message)))
    state["current_agent"] = "hotel_specialist"
    return state


def hotel_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
        "hotel_specialist", temperature=0.5, session_id=state["session_id"]
    )

    step = (
        f"Recommend a boutique hotel in {state['destination']} between {state['departure']} "
        f"and {state['return_date']} for {state['travellers']} travellers."
    )

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a hotel booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = llm.invoke(messages)

    final_message = result
    state["hotel_summary"] = (
        final_message.content
        if isinstance(final_message, BaseMessage)
        else str(final_message)
    )
    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )
    state["current_agent"] = "activity_specialist"
    return state


def activity_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
        "activity_specialist", temperature=0.6, session_id=state["session_id"]
    )

    step = f"Curate signature activities for travellers spending a week in {state['destination']}."

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a hotel booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = llm.invoke(messages)

    final_message = result
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


def plan_synthesizer_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
        "plan_synthesizer", temperature=0.3, session_id=state["session_id"]
    )
    system_content = (
        "You are the travel plan synthesiser. Combine the specialist insights into a "
        "concise, structured itinerary covering flights, accommodation and activities."
    )

    system_prompt = SystemMessage(content=system_content)
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
            system_prompt,
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


def should_continue(state: PlannerState) -> str:
    mapping = {
        "start": "coordinator",
        "flight_specialist": "flight_specialist",
        "hotel_specialist": "hotel_specialist",
        "activity_specialist": "activity_specialist",
        "plan_synthesizer": "plan_synthesizer",
    }
    return mapping.get(state["current_agent"], END)


def build_workflow() -> StateGraph:
    graph = StateGraph(PlannerState)
    graph.add_node("coordinator", lambda state: coordinator_node(state))
    graph.add_node("flight_specialist",lambda state: flight_specialist_node(state))
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


# ---------------------------------------------------------------------------
# FastMCP Server Implementation
# ---------------------------------------------------------------------------

# Initialize Flask app
app = Flask(__name__)

def plan_travel_internal(
    origin: str,
    destination: str,
    user_request: str,
    travellers: int,
) -> Dict[str, object]:
    """Internal function to execute travel planning workflow."""
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

    root_input = [
        {
            "role": "user",
            "parts": [
                {
                    "type": "text",
                    "content": user_request,
                }
            ],
        }
    ]

    config = {
        "configurable": {"thread_id": session_id},
        "recursion_limit": 10,
    }

    final_state: Optional[PlannerState] = None
    agent_steps = []

    for step in compiled_app.stream(initial_state, config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
        agent_steps.append({"agent": node_name, "status": "completed"})

    if not final_state:
        final_plan = ""
    else:
        final_plan = final_state.get("final_itinerary") or ""

    if final_plan:
        preview = final_plan[:500] + ("..." if len(final_plan) > 500 else "")

    return {
        "session_id": session_id,
        "origin": origin,
        "destination": destination,
        "departure": departure,
        "return_date": return_date,
        "travellers": travellers,
        "flight_summary": final_state.get("flight_summary") if final_state else None,
        "hotel_summary": final_state.get("hotel_summary") if final_state else None,
        "activities_summary": final_state.get("activities_summary")
        if final_state
        else None,
        "final_itinerary": final_plan,
        "agent_steps": agent_steps,
    }


@app.route("/travel/plan", methods=["POST"])
def plan():
    """Handle travel planning requests via HTTP POST."""
    try:
        data = request.get_json()

        origin = data.get("origin", "Seattle")
        destination = data.get("destination", "Paris")
        user_request = data.get(
            "user_request",
            f"Planning a week-long trip from {origin} to {destination}. "
            "Looking for boutique hotel, flights and unique experiences.",
        )
        travellers = int(data.get("travellers", 2))

        logging.info(
            f"[SERVER] Processing travel plan: {origin} -> {destination}"
        )

        result = plan_travel_internal(
            origin=origin,
            destination=destination,
            user_request=user_request,
            travellers=travellers
        )

        logging.info(
            "[SERVER] Travel plan completed successfully"
        )
        logging.info("TRAVEL PLAN RESULT:")
        logging.info(result)

        return jsonify(result), 200

    except Exception as e:
        logging.error(
            f"[SERVER] Error processing travel plan: {e}"
        )
        import traceback

        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for k8s."""
    return jsonify({"status": "healthy", "service": "travel-planner-flask"}), 200


if __name__ == "__main__":
    logging.info(
        "[INFO] Starting Flask server on http://0.0.0.0:8080"
    )
    app.run(host="0.0.0.0", port=8080, debug=False)
