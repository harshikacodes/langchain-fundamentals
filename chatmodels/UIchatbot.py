import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="MoodBot AI", page_icon="🤖")

# Simple color styling
st.markdown("""
<style>
.stApp { background-color: #101827; color: white; }
h1, h2, h3, p, label { color: #F8FAFC !important; }
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #CBD5E1 !important;
}
.stButton button {
    background: #4F46E5;
    color: white !important;
    border: 1px solid #818CF8;
    border-radius: 10px;
}
.stButton button p { color: white !important; }
[data-testid="stChatMessage"] {
    background: #1E293B;
    border: 1px solid #475569;
    border-radius: 12px;
}
[data-testid="stChatMessage"] p { color: #F8FAFC !important; }
[data-testid="stChatInput"] {
    background: #1E293B;
    border: 1px solid #818CF8;
}
[data-testid="stChatInput"] textarea {
    color: white !important;
    -webkit-text-fill-color: black !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
}
</style>
""", unsafe_allow_html=True)

# AI personalities
MODES = {
    "😡 Angry": "You are an angry AI agent. You respond aggressively and impatiently.",
    "😂 Funny": "You are a very funny AI agent. You respond with humor and jokes.",
    "😢 Sad": "You are a sad AI agent. You respond with disappointment.",
}

if "mode" not in st.session_state:
    st.session_state.mode = "😂 Funny"
    st.session_state.messages = [
        SystemMessage(content=MODES["😂 Funny"])
    ]

if "model" not in st.session_state:
    st.session_state.model = ChatGroq(model="openai/gpt-oss-20b")

# Header
st.title("🤖 MoodBot AI")
st.caption("One AI. Three personalities. Choose your vibe.")

# Mode selection
st.subheader("Choose your personality")
cols = st.columns(3)

for col, mode in zip(cols, MODES):
    with col:
        if st.button(mode, use_container_width=True):
            if st.session_state.mode != mode:
                st.session_state.mode = mode
                st.session_state.messages = [
                    SystemMessage(content=MODES[mode])
                ]
                st.rerun()

st.info(f"Current mode: {st.session_state.mode}")

# Show conversation
for msg in st.session_state.messages:
    if isinstance(msg, SystemMessage):
        continue
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Chat input
prompt = st.chat_input("Type a message... (0 to exit)")

if prompt:
    if prompt.strip() == "0":
        st.session_state.messages = [
            SystemMessage(content=MODES[st.session_state.mode])
        ]
        st.rerun()

    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.model.invoke(
                    st.session_state.messages
                )
                st.markdown(response.content)
                st.session_state.messages.append(
                    AIMessage(content=response.content)
                )
            except Exception:
                st.error("Something went wrong. Check your API key.")