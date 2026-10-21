import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage,
)

load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="Funny AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# UI styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #111827;
    }

    h1 {
        text-align: center;
        color: #F9FAFB;
    }

    .subtitle {
        text-align: center;
        color: #9CA3AF;
        margin-bottom: 30px;
    }

    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 12px;
    }

    [data-testid="stChatInput"] {
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 Funny AI Chatbot")
st.markdown(
    '<p class="subtitle">Your funny AI assistant is ready to chat!</p>',
    unsafe_allow_html=True,
)

# Initialize the model and conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="you are a funny Ai agent")
    ]

if "model" not in st.session_state:
    st.session_state.model = ChatGroq(
        model="openai/gpt-oss-20b"
    )

# Display previous conversation
for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        continue

    role = "user" if isinstance(message, HumanMessage) else "assistant"

    with st.chat_message(role):
        st.markdown(message.content)

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:
    # Keep the original exit behavior
    if prompt == "0":
        st.info("Goodbye! 👋")
        st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.model.invoke(
                st.session_state.messages
            )

            st.markdown(response.content)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )
