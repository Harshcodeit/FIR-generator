from langchain_ollama import ChatOllama

_llm = None

def load_llm(
        model_name : str = 'gemma4:26b',
        temperature : float = 0,
        num_ctx : int = 8192
) :
    global _llm
    if _llm is None:
        _llm = ChatOllama(
            model = model_name,
            temperature = temperature,
            num_ctx = num_ctx
            
        )

    return _llm


