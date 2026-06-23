"""Healthcare assistant Streamlit app."""
import os
import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from agent import HealthcareAgent
from config import load_config
from rag import get_rag_system
from setup_env import setup_environment

load_dotenv()

if not os.getenv("_ENV_LOADED"):
    setup_environment()
    os.environ["_ENV_LOADED"] = "true"


def escape_dollar_signs(text: str) -> str:
    return text.replace("$", "\\$")


def display_chat_history():
    if not st.session_state.messages:
        return

    for message_data in st.session_state.messages:
        if isinstance(message_data, dict):
            message = message_data.get("message")
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(escape_dollar_signs(message.content))
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(escape_dollar_signs(message.content))

    if st.session_state.get("processing", False):
        with st.chat_message("assistant"):
            st.write("Thinking...")


def show_example_queries(query_1: str, query_2: str):
    st.subheader("💡 Try these examples")
    col1, col2 = st.columns([0.48, 0.48])
    with col1:
        if st.button(query_1, key="query_1", use_container_width=True):
            return query_1
    with col2:
        if st.button(query_2, key="query_2", use_container_width=True):
            return query_2
    return None


def get_user_input(app_title: str, example_query_1: str, example_query_2: str):
    st.title(app_title)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    example_query = show_example_queries(example_query_1, example_query_2)
    display_chat_history()

    user_input = st.chat_input("How can I help you?...")
    if example_query:
        user_input = example_query
    return user_input


def process_input(user_input: str | None):
    if user_input:
        st.session_state.messages.append(
            {"message": HumanMessage(content=user_input), "agent": "user"}
        )
        st.session_state.processing = True
        st.rerun()

    if st.session_state.get("processing", False):
        conversation_messages = []
        for msg_data in st.session_state.messages:
            if isinstance(msg_data, dict) and "message" in msg_data:
                message = msg_data["message"]
                if isinstance(message, HumanMessage):
                    conversation_messages.append({"role": "user", "content": message.content})
                elif isinstance(message, AIMessage):
                    conversation_messages.append({"role": "assistant", "content": message.content})

        response = st.session_state.agent.process_query(conversation_messages)
        st.session_state.messages.append(
            {"message": AIMessage(content=response), "agent": "assistant"}
        )
        st.session_state.processing = False
        st.rerun()


def render_sidebar(app_config: dict) -> str:
    with st.sidebar:
        st.subheader("Model")
        model_config = app_config.get("model", {})
        default_model = model_config.get("default_model", "gpt-4.1-mini")
        additional_models = model_config.get("additional_models", [])
        available_models = [default_model] + [
            m for m in additional_models if m != default_model
        ]

        previous_model = st.session_state.get("active_model", default_model)
        selected_model = st.selectbox(
            "LLM",
            options=available_models,
            index=(
                available_models.index(previous_model)
                if previous_model in available_models
                else 0
            ),
            help="OpenAI model used for chat",
        )

        if previous_model != selected_model and "agent" in st.session_state:
            del st.session_state.agent
        st.session_state.active_model = selected_model

    return selected_model


def main():
    app_config = load_config()
    ui_config = app_config.get("ui", {})
    app_title = ui_config.get("app_title", "Online Healthcare Assistant")
    example_queries = ui_config.get(
        "example_queries",
        [
            "What is the dosage and common side effects of Lisinopril?",
            "Can you look up information for patient P001?",
        ],
    )

    selected_model = render_sidebar(app_config)

    if "rag_initialized" not in st.session_state:
        get_rag_system()
        st.session_state.rag_initialized = True

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "agent" not in st.session_state:
        st.session_state.agent = HealthcareAgent(
            session_id=st.session_state.session_id,
            model_override=selected_model,
        )

    user_input = get_user_input(
        app_title,
        example_queries[0],
        example_queries[1] if len(example_queries) > 1 else "What can you do?",
    )
    process_input(user_input)


if __name__ == "__main__":
    main()
