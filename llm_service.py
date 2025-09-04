import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

@st.cache_resource
def get_llm():
    """Initialize and cache the LLM with OpenAI API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set OPENAI_API_KEY in your .env file")
        st.stop()
    return ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini",
        openai_api_key=api_key
    )

llm = get_llm()

def extract_with_llm(field_name, text):
    """Generic extractor using LLM."""
    prompt = PromptTemplate.from_template(
        "Extract only the {field} from: '{text}'. Return just the value, no extra words. If not found, return 'NONE'."
    )
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"field": field_name, "text": text})
    return result.strip() if result and result.upper() != "NONE" else None
