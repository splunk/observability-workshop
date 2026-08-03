"""
Hallucination Demo Helpers

Log intentional hallucinations to Galileo for Splunk Agent Observability demos.
Examples are defined in config.yaml under `demo_hallucinations`.
"""
import logging
import os
import uuid
from typing import Any, List, Optional, Union

from galileo import GalileoLogger
from langchain_core.messages import AIMessage, HumanMessage

logger = logging.getLogger(__name__)


def log_hallucination(
    project_name: str,
    log_stream: str,
    question: str,
    context_docs: List[str],
    hallucinated_answer: str,
    model: str = "gpt-4o",
    session_name: str = "Hallucination Demo",
    external_session_id: Optional[str] = None,
    existing_logger: Optional[Union[GalileoLogger, Any]] = None,
) -> bool:
    """
    Log a hallucination trace to Galileo for demonstration purposes.

    Creates a trace with a retriever span (real context) and an LLM span (wrong answer).
    """
    try:
        logger.info(
            "Logging hallucination to project: %s, log stream: %s",
            project_name,
            log_stream,
        )

        if existing_logger:
            logger.info("Using existing Galileo session for hallucination demo")
            if hasattr(existing_logger, "get_logger_instance"):
                galileo_logger = existing_logger.get_logger_instance()
            else:
                galileo_logger = existing_logger
        else:
            logger.info("Creating new Galileo session for hallucination demo")
            galileo_logger = GalileoLogger(project=project_name, log_stream=log_stream)
            galileo_logger.start_session(
                name=session_name,
                external_id=external_session_id or str(uuid.uuid4()),
            )

        galileo_logger.start_trace(
            input=question,
            name="Hallucination Demo",
        )

        galileo_logger.add_retriever_span(
            input=question,
            output=context_docs,
            name="RAG Retrieval",
            duration_ns=int(1.3e8),
            status_code=200,
        )

        context_text = "\n\n".join(context_docs)
        llm_input = f"""Human: You are a helpful assistant. Given the context below, please answer the following question:

{context_text}

Question: {question}"""

        galileo_logger.add_llm_span(
            input=llm_input,
            output=hallucinated_answer,
            model=model,
            name="LLM Response",
            num_input_tokens=len(llm_input.split()) * 2,
            num_output_tokens=len(hallucinated_answer.split()) * 2,
            total_tokens=len(llm_input.split()) * 2 + len(hallucinated_answer.split()) * 2,
            duration_ns=int(1.2e8),
            metadata={"temperature": "0.1", "demo_type": "hallucination"},
            temperature=0.1,
            status_code=200,
            time_to_first_token_ns=500000,
        )

        galileo_logger.conclude(
            output=hallucinated_answer,
            duration_ns=int(2.5e8),
            status_code=200,
        )

        galileo_logger.flush()

        logger.info("Successfully logged hallucination to project: %s", project_name)
        return True

    except Exception as e:
        logger.error("Failed to log hallucination: %s", e)
        return False


def log_demo_hallucination(
    config: dict,
    hallucination_index: int = 0,
    existing_logger: Optional[Union[GalileoLogger, Any]] = None,
    session_id: Optional[str] = None,
) -> bool:
    """Log a demo hallucination from config.yaml to Galileo."""
    project_name = os.getenv("GALILEO_PROJECT", "healthcare-assistant")
    log_stream = os.getenv("GALILEO_LOG_STREAM", "default")

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
        log_stream=log_stream,
        question=question,
        context_docs=context_docs,
        hallucinated_answer=hallucinated_answer,
        model=model,
        session_name="Healthcare Hallucination Demo",
        external_session_id=session_id,
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
