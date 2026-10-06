"""Healthcare assistant front-end (Streamlit).

Thin UI only — it holds NO agent / LLM / Agent Control state and never imports
agent.py (see CLAUDE.md §11). After the shared basic-auth (at the ingress), the
user picks an agent stream + target; the embedded orchestrator provisions a
back-end for that (stream, target), and every chat turn is forwarded to it over
in-cluster HTTP.
"""
import html
import uuid

import httpx
import streamlit as st

from config import load_config
from orchestrator import ensure_backend
from targets import DEFAULT_TARGET, TARGETS

QUERY_TIMEOUT_SECONDS = 120
PAGE_ICON = "🩻"

# Short labels for the compact status pill in the chat header.
TARGET_SHORT = {
    "standalone": "Standalone",
    "us-splunk-show": "US Show",
    "eu-splunk-show": "EU Show",
}


def escape_dollar_signs(text: str) -> str:
    return text.replace("$", "\\$")


# --- styling -----------------------------------------------------------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
          :root {
            --accent: #E5326E;      /* Splunk magenta */
            --accent-2: #F99D1C;    /* Splunk orange  */
            --surface: #16181D;
            --surface-2: #1E2128;
            --border: #2A2E37;
            --muted: #9BA3AF;
            --ok: #3DD68C;
          }
          /* Trim default chrome for a cleaner stage look */
          #MainMenu, footer {visibility: hidden;}
          [data-testid="stHeader"] {background: transparent;}
          .block-container {padding-top: 2.2rem; max-width: 820px;}

          /* App header bar (chat view) */
          .app-header {
            display: flex; align-items: center; justify-content: space-between;
            padding: 14px 18px; margin-bottom: 10px;
            background: var(--surface);
            border: 1px solid var(--border); border-radius: 14px;
          }
          .app-header .title {font-size: 1.15rem; font-weight: 700; letter-spacing: .2px;}
          .status-pill {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 6px 12px; border-radius: 999px;
            background: var(--surface-2); border: 1px solid var(--border);
            font-size: .82rem; color: var(--muted);
          }
          .status-pill .dot {
            width: 9px; height: 9px; border-radius: 50%;
            background: var(--ok); box-shadow: 0 0 0 3px rgba(61,214,140,.18);
          }
          .status-pill b {color: #F5F6F8; font-weight: 600;}

          /* Hero (setup view) */
          .hero {text-align: center; padding: 6px 0 2px;}
          .hero .logo {font-size: 2.6rem; line-height: 1;}
          .hero h1 {font-size: 1.9rem; margin: .35rem 0 .15rem; font-weight: 800;}
          .hero p {color: var(--muted); margin: 0;}
          .hero .accent {
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            -webkit-background-clip: text; background-clip: text;
            -webkit-text-fill-color: transparent;
          }

          /* Chat bubbles */
          [data-testid="stChatMessage"] {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 14px; padding: 2px 6px;
          }

          /* Buttons */
          .stButton > button, .stFormSubmitButton > button {
            border-radius: 10px; border: 1px solid var(--border);
            font-weight: 600; transition: all .12s ease-in-out;
          }
          button[kind="primary"], .stFormSubmitButton > button {
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            border: none; color: white;
          }
          button[kind="primary"]:hover, .stFormSubmitButton > button:hover {
            filter: brightness(1.08); transform: translateY(-1px);
          }
          button[kind="secondary"]:hover {border-color: var(--accent);}

          /* Chat input */
          [data-testid="stChatInput"] {
            border-radius: 12px; border: 1px solid var(--border);
          }
          [data-testid="stChatInput"]:focus-within {border-color: var(--accent);}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- back-end HTTP calls -----------------------------------------------------
def backend_query(messages: list[dict], model: str | None) -> str:
    resp = httpx.post(
        f"{st.session_state.backend_url}/query",
        json={
            "session_id": st.session_state.session_id,
            "messages": messages,
            "model": model,
        },
        timeout=QUERY_TIMEOUT_SECONDS,
    )
    resp.raise_for_status()
    return resp.json()["response"]


def backend_log_hallucination() -> bool:
    resp = httpx.post(
        f"{st.session_state.backend_url}/log-hallucination",
        json={"session_id": st.session_state.session_id},
        timeout=60,
    )
    resp.raise_for_status()
    return bool(resp.json().get("success"))


# --- setup screen ------------------------------------------------------------
def render_setup_screen(app_config: dict) -> None:
    title = app_config.get("ui", {}).get("app_title", "Online Healthcare Assistant")
    st.markdown(
        f"""
        <div class="hero">
          <div class="logo">{PAGE_ICON}</div>
          <h1>{html.escape(title)}</h1>
          <p>Start a demo session — your traces and Agent Control settings are
          <span class="accent">isolated to your agent stream</span>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    _, mid, _ = st.columns([1, 6, 1])
    with mid, st.container(border=True):
        with st.form("session_setup"):
            stream = st.text_input(
                "Agent stream name",
                placeholder="e.g. your-name",
                help="Your traces are grouped under this stream; Agent Control binds to it.",
            )
            target_keys = list(TARGETS.keys())
            target = st.selectbox(
                "Target",
                options=target_keys,
                index=target_keys.index(DEFAULT_TARGET),
                format_func=lambda k: TARGETS[k].label,
                help="Where traces are sent. Chosen per session; the back-end is wired to it.",
            )
            submitted = st.form_submit_button(
                "🚀  Launch demo", use_container_width=True, type="primary"
            )

    st.caption("Powered by Splunk Agent Observability")

    if submitted:
        if not stream.strip():
            st.error("Please enter an agent stream name.")
            return
        with st.status("Provisioning your demo environment…", expanded=True) as status:
            st.write(f"Target: **{TARGETS[target].label}**")
            st.write(f"Agent stream: **{stream.strip()}**")
            st.write("Starting a dedicated back-end (first launch can take a minute)…")
            try:
                result = ensure_backend(stream.strip(), target)
            except Exception as e:
                status.update(label="Provisioning failed", state="error")
                st.error(f"Failed to provision back-end: {e}")
                return
            if not result["ready"]:
                status.update(label="Back-end not ready", state="error")
                st.error(
                    f"Back-end did not become ready: {result.get('detail', 'unknown')}.\n\n"
                    "It may still be starting — try launching again in a moment."
                )
                return
            status.update(label="Ready — launching demo", state="complete")
        st.session_state.stream = stream.strip()
        st.session_state.target = target
        st.session_state.backend_url = result["url"]
        st.session_state.messages = []
        st.rerun()


# --- chat screen -------------------------------------------------------------
def render_header() -> None:
    stream = html.escape(st.session_state.stream)
    target_short = html.escape(TARGET_SHORT.get(st.session_state.target, st.session_state.target))
    st.markdown(
        f"""
        <div class="app-header">
          <div class="title">{PAGE_ICON}&nbsp; Healthcare Assistant</div>
          <div class="status-pill"><span class="dot"></span>
            <b>{stream}</b>&nbsp;·&nbsp;{target_short}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_chat_history() -> None:
    for entry in st.session_state.messages:
        avatar = "🧑" if entry["role"] == "user" else PAGE_ICON
        with st.chat_message(entry["role"], avatar=avatar):
            st.write(escape_dollar_signs(entry["content"]))
    if st.session_state.get("processing"):
        with st.chat_message("assistant", avatar=PAGE_ICON):
            st.write("Thinking…")


def render_sidebar(app_config: dict) -> None:
    with st.sidebar:
        st.markdown("#### Session")
        with st.container(border=True):
            st.markdown(
                f"**Stream:** `{st.session_state.stream}`  \n"
                f"**Target:** {TARGETS[st.session_state.target].label}"
            )
        if st.button("← Switch stream", use_container_width=True):
            for key in ("stream", "target", "backend_url", "messages"):
                st.session_state.pop(key, None)
            st.rerun()
        st.caption("Detaches this browser. The back-end keeps running and is "
                   "auto-reaped when idle.")

        if app_config.get("demo_hallucinations"):
            st.divider()
            st.markdown("#### Hallucination Demo")
            st.caption("Log an intentional hallucination to Splunk Agent Observability.")
            if st.button("Log Hallucination", key="log_hallucination",
                         use_container_width=True):
                with st.spinner("Logging hallucination…"):
                    try:
                        ok = backend_log_hallucination()
                    except Exception as e:
                        ok = False
                        st.error(f"Failed to log hallucination: {e}")
                if ok:
                    _append_hallucination_to_chat(app_config)
                    st.rerun()


def _append_hallucination_to_chat(app_config: dict, index: int = 0) -> None:
    hallucinations = app_config.get("demo_hallucinations", [])
    if not hallucinations:
        return
    h = hallucinations[index if index < len(hallucinations) else 0]
    q, a = h.get("question", ""), h.get("hallucinated_answer", "")
    if q and a:
        st.session_state.messages.append({"role": "user", "content": q})
        st.session_state.messages.append({"role": "assistant", "content": a})


def show_example_queries(q1: str, q2: str) -> str | None:
    st.caption("💡 Try an example")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(q1, key="query_1", use_container_width=True, type="secondary"):
            return q1
    with col2:
        if st.button(q2, key="query_2", use_container_width=True, type="secondary"):
            return q2
    return None


def render_chat_screen(app_config: dict) -> None:
    ui = app_config.get("ui", {})
    render_sidebar(app_config)
    model = app_config.get("model", {}).get("default_model", "gpt-4.1-mini")
    render_header()

    examples = ui.get("example_queries", [
        "What is the dosage and common side effects of Lisinopril?",
        "Can you look up information for patient P001?",
    ])
    if not st.session_state.messages:
        example = show_example_queries(
            examples[0], examples[1] if len(examples) > 1 else "What can you do?"
        )
    else:
        example = None
    display_chat_history()

    user_input = st.chat_input("How can I help you?...") or example
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.processing = True
        st.rerun()

    if st.session_state.get("processing"):
        try:
            response = backend_query(st.session_state.messages, model)
        except Exception as e:
            response = f"Error contacting the agent back-end: {e}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.processing = False
        st.rerun()


# --- entrypoint --------------------------------------------------------------
def main() -> None:
    app_config = load_config()
    st.set_page_config(
        page_title="Healthcare Assistant",
        page_icon=PAGE_ICON,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    inject_css()

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.get("backend_url"):
        render_setup_screen(app_config)
    else:
        render_chat_screen(app_config)


if __name__ == "__main__":
    main()
