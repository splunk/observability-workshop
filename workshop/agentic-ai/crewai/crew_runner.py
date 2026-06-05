from __future__ import annotations
import os
import yaml
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Dict, Any, Tuple

from crewai import Agent, Task, Crew, Process
from tools import mock_search_flights, mock_search_hotels, mock_search_activities

def _compute_dates() -> Tuple[str, str]:
    start = datetime.now() + timedelta(days=30)
    end = start + timedelta(days=7)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def _load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _openai_model_name() -> str:
    deployment = os.getenv("OPENAI_MODEL_NAME")
    if not deployment:
        raise RuntimeError("Missing OPENAI_MODEL_NAME")
    return deployment


def _validate_openai_env() -> None:
    required = [
        "OPENAI_BASE_URL",
        "OPENAI_MODEL_NAME",
        "OPENAI_API_KEY",
    ]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing OpenAI env vars: {', '.join(missing)}")


def build_crew() -> Crew:
    _validate_openai_env()
    agents_cfg = _load_yaml("config/agents.yaml")
    tasks_cfg = _load_yaml("config/tasks.yaml")
    model = _openai_model_name()

    coordinator = Agent(
        config=agents_cfg["coordinator"],
        llm=model,
    )
    flight_specialist = Agent(
        config=agents_cfg["flight_specialist"],
        llm=model,
        tools=[mock_search_flights],
    )
    hotel_specialist = Agent(
        config=agents_cfg["hotel_specialist"],
        llm=model,
        tools=[mock_search_hotels],
    )
    activity_specialist = Agent(
        config=agents_cfg["activity_specialist"],
        llm=model,
        tools=[mock_search_activities],
    )
    plan_synthesizer = Agent(
        config=agents_cfg["plan_synthesizer"],
        llm=model,
    )

    t1 = Task(config=tasks_cfg["coordinate_trip"], agent=coordinator)
    t2 = Task(config=tasks_cfg["find_flights"], agent=flight_specialist)
    t3 = Task(config=tasks_cfg["find_hotel"], agent=hotel_specialist)
    t4 = Task(config=tasks_cfg["find_activities"], agent=activity_specialist)
    t5 = Task(config=tasks_cfg["synthesize_itinerary"], agent=plan_synthesizer)

    return Crew(
        agents=[coordinator, flight_specialist, hotel_specialist, activity_specialist, plan_synthesizer],
        tasks=[t1, t2, t3, t4, t5],
        process=Process.sequential,
        verbose=True,
    )

def plan_travel_internal(origin: str, destination: str, user_request: str, travellers: int) -> Dict[str, Any]:
    session_id = str(uuid4())
    departure, return_date = _compute_dates()

    inputs = {
        "session_id": session_id,
        "origin": origin,
        "destination": destination,
        "user_request": user_request,
        "travellers": travellers,
        "departure": departure,
        "return_date": return_date,
    }

    crew = build_crew()
    result = crew.kickoff(inputs=inputs)
    final_text = str(result)

    return {
        "session_id": session_id,
        "origin": origin,
        "destination": destination,
        "departure": departure,
        "return_date": return_date,
        "travellers": travellers,
        "flight_summary": None,
        "hotel_summary": None,
        "activities_summary": None,
        "final_itinerary": final_text,
        "agent_steps": [
            {"agent": "coordinator", "status": "completed"},
            {"agent": "flight_specialist", "status": "completed"},
            {"agent": "hotel_specialist", "status": "completed"},
            {"agent": "activity_specialist", "status": "completed"},
            {"agent": "plan_synthesizer", "status": "completed"},
        ],
    }