"""
Hallucination Demo Helpers

Log intentional hallucinations to Splunk Agent Observability for demos.
Examples are defined in config.yaml under `demo_hallucinations`.
"""
import logging
import os
import uuid
from typing import Any, List, Optional, Union

from galileo_core.schemas.logging.span import LlmMetrics, RetrieverSpan
from galileo_core.schemas.logging.step import Metrics
from galileo_core.schemas.shared.document import Document
from langchain_core.messages import AIMessage, HumanMessage
from splunk_ao import SplunkAOLogger
from splunk_ao.deployment import DeploymentMode, resolve_deployment
from splunk_ao.schema.logged import LoggedLlmSpan, LoggedTrace, LoggedWorkflowSpan
from splunk_ao.schema.trace import TracesIngestRequest

logger = logging.getLogger(__name__)


def _documents_from_context(context_docs: List[str]) -> List[Document]:
    return [
        Document(content=doc, metadata={"source": "demo_hallucination"})
        for doc in context_docs
    ]


def _build_hallucination_trace(
    question: str,
    context_docs: List[str],
    hallucinated_answer: str,
    model: str,
) -> LoggedTrace:
    """Build a workflow trace with retriever + LLM spans for the hallucination demo."""
    context_text = "\n\n".join(context_docs)
    llm_input = f"""Human: You are a helpful assistant. Given the context below, please answer the following question:

{context_text}

Question: {question}"""

    retriever_span = RetrieverSpan(
        input=question,
        output=_documents_from_context(context_docs),
        name="RAG Retrieval",
        metrics=Metrics(duration_ns=int(1.3e8)),
        status_code=200,
        id=uuid.uuid4(),
    )
    llm_span = LoggedLlmSpan(
        input=llm_input,
        output=hallucinated_answer,
        model=model,
        name="LLM Response",
        metrics=LlmMetrics(
            duration_ns=int(1.2e8),
            num_input_tokens=len(llm_input.split()) * 2,
            num_output_tokens=len(hallucinated_answer.split()) * 2,
            num_total_tokens=len(llm_input.split()) * 2 + len(hallucinated_answer.split()) * 2,
            time_to_first_token_ns=500000,
        ),
        user_metadata={"temperature": "0.1", "demo_type": "hallucination"},
        temperature=0.1,
        status_code=200,
        id=uuid.uuid4(),
    )
    workflow_span = LoggedWorkflowSpan(
        input=question,
        output=hallucinated_answer,
        name="Hallucination Demo",
        metrics=Metrics(duration_ns=int(2.5e8)),
        status_code=200,
        id=uuid.uuid4(),
    )
    workflow_span.add_child_span(retriever_span)
    workflow_span.add_child_span(llm_span)

    trace = LoggedTrace(
        input=question,
        output=hallucinated_answer,
        name="Hallucination Demo",
        metrics=Metrics(duration_ns=int(2.5e8)),
        status_code=200,
        id=uuid.uuid4(),
    )
    trace.add_child_span(workflow_span)
    return trace


def _ensure_session(
    splunk_ao_logger: SplunkAOLogger,
    session_name: str,
    external_session_id: Optional[str],
) -> None:
    if splunk_ao_logger.session_id is not None:
        return

    if resolve_deployment() == DeploymentMode.STANDALONE:
        splunk_ao_logger.start_session(
            name=session_name,
            external_id=external_session_id or str(uuid.uuid4()),
        )
    elif external_session_id:
        splunk_ao_logger.set_session(external_session_id)


def _resolve_ingest_session_id(
    splunk_ao_logger: SplunkAOLogger,
    existing_logger: Optional[Union[SplunkAOLogger, Any]],
    external_session_id: Optional[str],
):
    """Return the backend session ID used by OTLP chat traces on this thread."""
    if splunk_ao_logger.session_id is not None:
        return splunk_ao_logger.session_id

    if not external_session_id:
        return None

    # Standalone maps Streamlit's external UUID to a backend session via CRUD.
    if resolve_deployment() == DeploymentMode.STANDALONE and existing_logger is not None:
        backend_session_id = existing_logger.start_session(external_id=external_session_id)
        existing_logger.set_session(backend_session_id)
        return backend_session_id

    splunk_ao_logger.set_session(external_session_id)
    return external_session_id


def log_hallucination(
    project_name: str,
    agent_stream: str,
    question: str,
    context_docs: List[str],
    hallucinated_answer: str,
    model: str = "gpt-4o",
    session_name: str = "Hallucination Demo",
    external_session_id: Optional[str] = None,
    backend_session_id: Optional[str] = None,
    existing_logger: Optional[Union[SplunkAOLogger, Any]] = None,
) -> bool:
    """
    Log a hallucination trace to Splunk AO for demonstration purposes.

    Creates a trace with a retriever span (real context) and an LLM span (wrong answer).
    Uses the CRUD ingest API so retriever documents stay typed; standalone OTLP export
    JSON-stringifies retriever output and the receiver rejects the batch.
    """
    try:
        logger.info(
            "Logging hallucination to project: %s, agent stream: %s",
            project_name,
            agent_stream,
        )

        if existing_logger:
            logger.info("Using existing Splunk AO session for hallucination demo")
            if hasattr(existing_logger, "get_logger_instance"):
                splunk_ao_logger = existing_logger.get_logger_instance()
            else:
                splunk_ao_logger = existing_logger
        else:
            logger.info("Creating new Splunk AO session for hallucination demo")
            splunk_ao_logger = SplunkAOLogger(project=project_name, agent_stream=agent_stream)
            _ensure_session(splunk_ao_logger, session_name, external_session_id)

        trace = _build_hallucination_trace(
            question=question,
            context_docs=context_docs,
            hallucinated_answer=hallucinated_answer,
            model=model,
        )
        ingest_session_id = backend_session_id or _resolve_ingest_session_id(
            splunk_ao_logger,
            existing_logger,
            external_session_id,
        )
        logger.info("Ingesting hallucination trace into session %s", ingest_session_id)
        splunk_ao_logger.ingest_traces(
            TracesIngestRequest(
                traces=[trace],
                session_id=ingest_session_id,
                log_stream_id=splunk_ao_logger.agent_stream_id,
            )
        )

        logger.info("Successfully logged hallucination to project: %s", project_name)
        return True

    except Exception as e:
        logger.error("Failed to log hallucination: %s", e)
        return False


def log_demo_hallucination(
    config: dict,
    hallucination_index: int = 0,
    existing_logger: Optional[Union[SplunkAOLogger, Any]] = None,
    session_id: Optional[str] = None,
    backend_session_id: Optional[str] = None,
) -> bool:
    """Log a demo hallucination from config.yaml to Splunk AO."""
    project_name = os.getenv("SPLUNK_AO_PROJECT", "healthcare-assistant")
    agent_stream = os.getenv("SPLUNK_AO_AGENT_STREAM", "default")

    hallucinations = config.get("demo_hallucinations", [])
    if not hallucinations:
        logger.warning("No hallucination examples defined in config")
        return False

    if hallucination_index >= len(hallucinations):
        hallucination_index = 0

    hallucination = hallucinations[hallucination_index]
    question = hallucination.get("question", "")
    hallucinated_answer = hallucination.get("hallucinated_answer", "")
    context_docs = hallucination.get("context", [])

    if not question or not hallucinated_answer:
        logger.error("Invalid hallucination config: missing question or answer")
        return False

    if not context_docs:
        context_docs = ["[No context available]"]

    model_config = config.get("model", {})
    model = model_config.get("default_model", "gpt-4o")

    return log_hallucination(
        project_name=project_name,
        agent_stream=agent_stream,
        question=question,
        context_docs=context_docs,
        hallucinated_answer=hallucinated_answer,
        model=model,
        session_name="Healthcare Hallucination Demo",
        external_session_id=session_id,
        backend_session_id=backend_session_id,
        existing_logger=existing_logger,
    )


def add_hallucination_interaction_to_chat(
    config: dict,
    hallucination_index: int = 0,
) -> None:
    """Append the demo hallucination Q&A pair to the Streamlit chat history."""
    import streamlit as st

    hallucinations = config.get("demo_hallucinations", [])
    if not hallucinations:
        return

    if hallucination_index >= len(hallucinations):
        hallucination_index = 0

    hallucination = hallucinations[hallucination_index]
    question = hallucination.get("question", "")
    answer = hallucination.get("hallucinated_answer", "")

    if not question or not answer:
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.messages.append(
        {"message": HumanMessage(content=question), "agent": "user"}
    )
    st.session_state.messages.append(
        {"message": AIMessage(content=answer), "agent": "assistant"}
    )
