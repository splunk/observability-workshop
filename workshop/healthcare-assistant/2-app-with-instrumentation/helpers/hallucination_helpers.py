"""
Hallucination Demo Helpers

Log intentional hallucinations to Splunk Agent Observability for demos.
Examples are defined in config.yaml under `demo_hallucinations`.

The demo trace is sent through the SAME backend logger and session the chat
turns use (via the REST `ingest_traces` API), so it groups into the active
session alongside the real conversation.
"""
import logging
import uuid
from typing import List, Optional

from langchain_core.messages import AIMessage, HumanMessage
from galileo_core.schemas.logging.span import LlmMetrics, RetrieverSpan
from galileo_core.schemas.logging.step import Metrics
from galileo_core.schemas.shared.document import Document
from splunk_ao import SplunkAOLogger
from splunk_ao.schema.logged import LoggedLlmSpan, LoggedTrace
from splunk_ao.schema.trace import TracesIngestRequest

logger = logging.getLogger(__name__)


def _build_hallucination_trace(
    question: str,
    context_docs: List[str],
    hallucinated_answer: str,
    model: str,
) -> LoggedTrace:
    """Build a trace with a retriever span (real context) and an LLM span (wrong answer)."""
    context_text = "\n\n".join(context_docs)
    llm_input = f"""Human: You are a helpful assistant. Given the context below, please answer the following question:

{context_text}

Question: {question}"""

    retriever_span = RetrieverSpan(
        input=question,
        output=[
            Document(content=doc, metadata={"source": "demo_hallucination"})
            for doc in context_docs
        ],
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
    trace = LoggedTrace(
        input=question,
        output=hallucinated_answer,
        name="Hallucination Demo",
        metrics=Metrics(duration_ns=int(2.5e8)),
        status_code=200,
        id=uuid.uuid4(),
    )
    trace.add_child_span(retriever_span)
    trace.add_child_span(llm_span)
    return trace


def log_hallucination(
    ingest_logger: SplunkAOLogger,
    session_id: Optional[str],
    question: str,
    context_docs: List[str],
    hallucinated_answer: str,
    model: str = "gpt-4o",
) -> bool:
    """
    Log a hallucination trace to Splunk AO for demonstration purposes.

    Uses the REST ingest API so the retriever documents stay typed and the trace
    groups under the supplied (chat) session.
    """
    try:
        trace = _build_hallucination_trace(
            question=question,
            context_docs=context_docs,
            hallucinated_answer=hallucinated_answer,
            model=model,
        )
        ingest_logger.ingest_traces(
            TracesIngestRequest(
                traces=[trace],
                session_id=session_id,
                log_stream_id=ingest_logger.agent_stream_id,
            )
        )
        logger.info("Successfully logged hallucination to session %s", session_id)
        return True

    except Exception as e:
        logger.error("Failed to log hallucination: %s", e)
        return False


def log_demo_hallucination(
    config: dict,
    ingest_logger: SplunkAOLogger,
    session_id: Optional[str],
    hallucination_index: int = 0,
) -> bool:
    """Log a demo hallucination from config.yaml to Splunk AO."""
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
        ingest_logger=ingest_logger,
        session_id=session_id,
        question=question,
        context_docs=context_docs,
        hallucinated_answer=hallucinated_answer,
        model=model,
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
