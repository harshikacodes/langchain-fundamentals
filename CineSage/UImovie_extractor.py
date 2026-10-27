import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Movie Information Extractor")
st.write("Enter a movie paragraph to extract structured information.")

class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract movie information from the paragraph.
{format_instructions}
"""
    ),
    ("human", "{paragraph}"),
])

para = st.text_area(
    "Movie paragraph",
    placeholder="Paste or type a movie paragraph here...",
    height=200,
)

if st.button("Extract Information", type="primary", use_container_width=True):
    if not para.strip():
        st.warning("Please enter a movie paragraph first.")
    else:
        with st.spinner("Extracting movie information..."):
            model = ChatGroq(model="openai/gpt-oss-20b")
            final_prompt = prompt.invoke({
                "paragraph": para,
                "format_instructions": parser.get_format_instructions(),
            })
            response = model.invoke(final_prompt)
            st.subheader("Extracted Information")
            st.code(response.content, language="json")