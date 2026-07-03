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
from langchain_google_genai import ChatGoogleGenerativeAI
from app.utils.helpers import get_message_text

load_dotenv()

@lru_cache(maxsize=1)
def load_llm(model : str = 'gemma-4-31b-it'):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
    )

