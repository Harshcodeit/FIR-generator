from langchain_ollama import ChatOllama

_llm = None

def load_llm(
        model_name : str = 'gemma4:26b',
        temperature : float = 0
) :
    global _llm
    if _llm is None:
        _llm = ChatOllama(
            model = model_name,
            temperature = temperature
        )

    return _llm

