# used for local testing
# from langchain_ollama import ChatOllama

# _llm = None

# def load_llm(
#         model_name : str = 'gemma4:26b',
#         temperature : float = 0,
#         num_ctx : int = 8192
# ) :
#     global _llm
#     if _llm is None:
#         _llm = ChatOllama(
#             model = model_name,
#             temperature = temperature,
#             num_ctx = num_ctx
            
#         )

#     return _llm


from functools import lru_cache
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_api_key():
    try:
        return st.secrets["GOOGLE_API_KEY"]   # Streamlit Cloud
    except Exception:
        return os.getenv("GOOGLE_API_KEY")    # Local .env


@lru_cache(maxsize=2)
def load_llm(model : str = 'gemma-4-31b-it'):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=get_api_key(),
        temperature=0.2,
    )

