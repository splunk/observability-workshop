"""Back-end agent service for the Healthcare Assistant demo.

One back-end process is bound to exactly ONE (agent_stream, target) for its
whole life — see CLAUDE.md §2/§11. agent_control.init() runs once per process
(lazily, on the first query, guarded by agent_control_helpers). The front-end
never runs agent logic; it calls this service over in-cluster HTTP.

Run with:  uvicorn server:app --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import logging
import os
import threading
import time
from typing import List, Optional

from dotenv import load_dotenv

# Load .env before importing the agent so Agent Control SDK settings see local URLs
# (mirrors app.py's original ordering).
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

from config import load_config
from setup_env import setup_environment

logger = logging.getLogger("healthcare.server")
logging.basicConfig(level=logging.INFO)

# --- identity of this back-end (injected by the orchestrator) ----------------
AGENT_STREAM = os.getenv("SPLUNK_AO_AGENT_STREAM", "default")
PROJECT = os.getenv("SPLUNK_AO_PROJECT", "Healthcare Assistant Demo")
# Idle self-termination: delete own Deployment+Service and exit after this many
# seconds with no /query. 0 disables (handy for local `uvicorn` dev).
IDLE_TTL_SECONDS = int(os.getenv("BACKEND_IDLE_TTL_SECONDS", "7200"))

# Wall-clock epoch (not monotonic): the orchestrator reads it off a Deployment
# annotation to compare last-used across pods, so it must be comparable across
# processes.
_last_activity = time.time()
_activity_lock = threading.Lock()
LAST_USED_ANNOTATION = "demo.splunk/last-used"


def _touch() -> None:
    global _last_activity
    with _activity_lock:
        _last_activity = time.time()


# --- request/response models -------------------------------------------------
class Message(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    session_id: str
    messages: List[Message]
    model: Optional[str] = None


class QueryResponse(BaseModel):
    response: str


class HallucinationRequest(BaseModel):
    session_id: Optional[str] = None


# --- app ---------------------------------------------------------------------
app = FastAPI(title="Healthcare Assistant Back-end", docs_url="/docs")

# Per-(session_id, model) agent cache. LangGraph here has no persistent
# checkpointer, so an agent is effectively stateless between turns (the front-end
# sends full history); the session_id is what groups traces into a Splunk AO
# session, so we keep one agent per session to preserve that grouping.
_agents: dict[tuple[str, Optional[str]], "object"] = {}
_agents_lock = threading.Lock()
_ready = False


def _get_agent(session_id: str, model: Optional[str]):
    from agent import HealthcareAgent  # imported lazily so startup can warm first

    key = (session_id, model)
    with _agents_lock:
        agent = _agents.get(key)
        if agent is None:
            agent = HealthcareAgent(session_id=session_id, model_override=model)
            _agents[key] = agent
        return agent


@app.on_event("startup")
def _startup() -> None:
    global _ready
    setup_environment()
    logger.info(
        "Back-end starting: project=%r agent_stream=%r idle_ttl=%ss",
        PROJECT, AGENT_STREAM, IDLE_TTL_SECONDS,
    )
    # Warm the RAG system (pgvector connection + embeddings) so the first real
    # query doesn't pay for it. agent_control.init() happens on the first /query
    # (it needs a started Splunk AO session to resolve the agent_stream_id).
    # Skippable so the service can boot without Postgres (e.g. CI smoke tests).
    if os.getenv("BACKEND_SKIP_RAG_WARM", "").strip().lower() in ("1", "true", "yes", "on"):
        logger.info("BACKEND_SKIP_RAG_WARM set — skipping RAG warmup")
    else:
        try:
            from rag import get_rag_system
            get_rag_system()
            logger.info("RAG system warmed")
        except Exception as e:  # pragma: no cover - warmup is best-effort
            logger.warning("RAG warmup failed (will retry lazily): %s", e)
    _ready = True
    if IDLE_TTL_SECONDS > 0:
        threading.Thread(target=_idle_watcher, name="idle-watcher", daemon=True).start()


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "agent_stream": AGENT_STREAM}


@app.get("/ready")
def ready() -> dict:
    return {"ready": _ready, "agent_stream": AGENT_STREAM}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    _touch()
    agent = _get_agent(req.session_id, req.model)
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    response = agent.process_query(messages)
    return QueryResponse(response=response)


@app.post("/log-hallucination")
def log_hallucination(req: HallucinationRequest) -> dict:
    """Log an intentional hallucination trace to this back-end's stream/target."""
    _touch()
    from helpers.hallucination_helpers import log_demo_hallucination

    ok = log_demo_hallucination(config=load_config(), session_id=req.session_id)
    return {"success": bool(ok)}


def _idle_watcher() -> None:
    """Refresh the last-used annotation and self-terminate once idle past the TTL.

    Each tick stamps demo.splunk/last-used on our own Deployment so the
    orchestrator can pick the least-recently-used back-end for eviction. Once
    idle past the TTL we delete our own Service + Deployment and exit — removing
    the Deployment (not just the Pod) is what prevents a restart (CLAUDE.md §12).
    Requires the back-end ServiceAccount to have patch + delete rights on
    deployments/services in its namespace.
    """
    while True:
        time.sleep(60)
        with _activity_lock:
            last = _last_activity
        _update_last_used_annotation(last)
        idle = time.time() - last
        if idle < IDLE_TTL_SECONDS:
            continue
        logger.info("Idle for %.0fs (TTL %ss) — self-terminating", idle, IDLE_TTL_SECONDS)
        try:
            _self_delete()
        except Exception as e:
            logger.warning("Self-delete failed (%s); exiting process anyway", e)
        os._exit(0)


_apps_api = None


def _get_apps_api():
    global _apps_api
    if _apps_api is None:
        from kubernetes import client, config as k8s_config

        try:
            k8s_config.load_incluster_config()
        except Exception:
            k8s_config.load_kube_config()
        _apps_api = client.AppsV1Api()
    return _apps_api


def _update_last_used_annotation(last_used: float) -> None:
    name = os.getenv("BACKEND_NAME")
    namespace = os.getenv("POD_NAMESPACE", "default")
    if not name:
        return
    body = {"metadata": {"annotations": {LAST_USED_ANNOTATION: str(int(last_used))}}}
    try:
        _get_apps_api().patch_namespaced_deployment(name, namespace, body)
    except Exception as e:  # best-effort; eviction falls back to creationTimestamp
        logger.debug("last-used annotation update failed: %s", e)


def _self_delete() -> None:
    name = os.getenv("BACKEND_NAME")
    namespace = os.getenv("POD_NAMESPACE", "default")
    if not name:
        logger.info("BACKEND_NAME not set; skipping k8s self-delete")
        return
    from kubernetes import client, config as k8s_config

    try:
        k8s_config.load_incluster_config()
    except Exception:
        k8s_config.load_kube_config()
    core = client.CoreV1Api()
    apps = client.AppsV1Api()
    for delete, kind in (
        (lambda: core.delete_namespaced_service(name, namespace), "service"),
        (lambda: apps.delete_namespaced_deployment(name, namespace), "deployment"),
    ):
        try:
            delete()
            logger.info("Deleted %s/%s", kind, name)
        except Exception as e:
            logger.warning("Could not delete %s/%s: %s", kind, name, e)
