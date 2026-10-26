import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #10131a;
        color: #f1f5f9;
    }
    [data-testid="stHeader"] {
        background: rgba(16, 19, 26, 0);
    }
    .main .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    .app-subtitle {
        color: #aab4c5;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
    }
    div[data-testid="stTextArea"] textarea {
        background: #1b2230;
        color: #f1f5f9;
        border: 1px solid #354156;
        border-radius: 10px;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 1px #60a5fa;
    }
    div.stButton > button {
        width: 100%;
        min-height: 2.8rem;
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: #2563eb;
        color: white;
        border: none;
    }
    .result-box {
        background: #1b2230;
        border: 1px solid #354156;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        color: #e5eaf2;
        white-space: pre-wrap;
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie Information Extractor")
st.markdown(
    '<p class="app-subtitle">Extract structured movie details from a paragraph.</p>',
    unsafe_allow_html=True,
)

para = st.text_area(
    "Movie paragraph",
    placeholder="Paste a movie paragraph here...",
    height=200,
)

if st.button("Extract Information", type="primary"):
    if not para.strip():
        st.warning("Please enter a movie paragraph first.")
    else:
        try:
            with st.spinner("Extracting movie information..."):
                model = ChatGroq(model="openai/gpt-oss-20b")

                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        """
You are a professional Movie Information Extraction Assistant.

Your task:
Extract useful structured information from a movie paragraph and present it in a clean readable format.

Rules:
- Do NOT add explanations
- Do NOT add extra commentary
- Follow the exact format
- If information is missing -> write NULL
- Keep summary short (2-3 lines max)
- Do NOT guess unknown facts

Output Format:

Movie Title:
Release Year:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:
"""
                    ),
                    (
                        "human",
                        """
Extract information from this paragraph:

{paragraph}
"""
                    ),
                ])

                final_prompt = prompt.invoke({"paragraph": para})
                response = model.invoke(final_prompt)

            st.subheader("Extracted Information")
            st.markdown(
                '<div class="result-box">' + 
                response.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") +
                '</div>',
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"Could not extract information. Check your Groq API key and connection. Details: {e}")