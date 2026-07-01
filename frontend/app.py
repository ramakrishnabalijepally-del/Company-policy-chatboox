import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Company Policy Chatbot",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark-theme CSS ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Overall background */
    .stApp { background-color: #1a1a2e; color: #e0e0e0; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #16213e; }

    /* User message bubble */
    .user-bubble {
        background-color: #0f3460;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        width: fit-content;
        float: right;
        clear: both;
        color: #ffffff;
        font-size: 15px;
    }

    /* Assistant message bubble */
    .assistant-bubble {
        background-color: #1f4068;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
        margin: 8px auto 8px 0;
        max-width: 75%;
        width: fit-content;
        float: left;
        clear: both;
        color: #e0e0e0;
        font-size: 15px;
    }

    /* Source citation box */
    .source-box {
        background-color: #0d2137;
        border-left: 3px solid #4a9eda;
        border-radius: 4px;
        padding: 6px 10px;
        margin: 4px 0 4px 10px;
        font-size: 12px;
        color: #7ab3d3;
        clear: both;
    }

    /* Chat container */
    .chat-container { padding: 10px 0; overflow-y: auto; }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1f2b3e;
        color: #e0e0e0;
        border: 1px solid #3a4a5c;
        border-radius: 8px;
    }

    /* Buttons */
    .stButton > button {
        background-color: #0f3460;
        color: #ffffff;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover { background-color: #1a5276; }

    /* Clear floats */
    .clearfix::after { content: ""; display: table; clear: both; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session state ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "indexed_docs" not in st.session_state:
    st.session_state.indexed_docs = []


def fetch_documents():
    try:
        r = requests.get(f"{BACKEND_URL}/documents", timeout=5)
        if r.status_code == 200:
            st.session_state.indexed_docs = r.json().get("documents", [])
    except Exception:
        st.session_state.indexed_docs = []


def render_chat():
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-bubble">{msg["content"]}</div><div class="clearfix"></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="assistant-bubble">{msg["content"]}</div><div class="clearfix"></div>',
                unsafe_allow_html=True,
            )
            if msg.get("sources"):
                for src in msg["sources"]:
                    st.markdown(
                        f'<div class="source-box">📄 {src["file"]} — Page {src["page"]}</div>',
                        unsafe_allow_html=True,
                    )


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 Policy Manager")
    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload Policy PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF policy documents.",
    )

    if st.button("📥 Ingest Documents", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one PDF file.")
        else:
            progress = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/ingest",
                            files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                            timeout=120,
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"✅ {data['filename']} — {data['chunks_indexed']} chunks indexed")
                        else:
                            st.error(f"❌ Failed: {response.json().get('detail', 'Unknown error')}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to backend. Is it running?")
                progress.progress((i + 1) / len(uploaded_files))
            fetch_documents()

    st.markdown("---")
    st.markdown("### 📚 Indexed Documents")
    fetch_documents()
    if st.session_state.indexed_docs:
        for doc in st.session_state.indexed_docs:
            st.markdown(f"- 📄 {doc}")
    else:
        st.caption("No documents indexed yet.")

    st.markdown("---")
    if st.button("🗑️ Clear Knowledge Base", use_container_width=True):
        try:
            r = requests.delete(f"{BACKEND_URL}/documents", timeout=10)
            if r.status_code == 200:
                st.success("Knowledge base cleared.")
                fetch_documents()
            else:
                st.error("Failed to clear knowledge base.")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend.")


# ── Main chat area ─────────────────────────────────────────────────────────────
col_title, col_btn = st.columns([5, 1])
with col_title:
    st.markdown("## 💬 Company Policy Assistant")
with col_btn:
    if st.button("🔄 New Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("---")

chat_placeholder = st.container()

with chat_placeholder:
    if not st.session_state.chat_history:
        st.markdown(
            """
            <div style='text-align:center; color:#4a6fa5; margin-top:60px;'>
                <h3>👋 Welcome to the Company Policy Assistant</h3>
                <p>Upload policy documents from the sidebar, then ask me anything!</p>
                <p><i>Examples: "What is the annual leave policy?" · "How do I report misconduct?"</i></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        render_chat()

st.markdown("---")

# ── Input row ──────────────────────────────────────────────────────────────────
input_col, send_col = st.columns([9, 1])
with input_col:
    user_input = st.text_input(
        "Ask a question about company policies...",
        key="user_input",
        label_visibility="collapsed",
        placeholder="Ask a question about company policies...",
    )
with send_col:
    send_clicked = st.button("Send", use_container_width=True)

if send_clicked and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

    with st.spinner("Thinking..."):
        try:
            payload = {
                "query": user_input.strip(),
                "chat_history": [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history[:-1]
                ],
            }
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=60,
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data.get("sources", []),
                })
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Error: {response.json().get('detail', 'Unknown error')}",
                    "sources": [],
                })
        except requests.exceptions.ConnectionError:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Cannot connect to backend. Please ensure the backend service is running.",
                "sources": [],
            })

    st.rerun()
