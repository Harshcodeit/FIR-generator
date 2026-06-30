from langchain_core.vectorstores import VectorStoreRetriever

# get vector database
from app.rag.vectorstore import get_vectorstore

_vector_retriever = None

def get_retriever(k : int = 8) -> VectorStoreRetriever :
    global _vector_retriever
    if _vector_retriever is None:
        vectorstore = get_vectorstore()

        _vector_retriever = vectorstore.as_retriever(
            search_type = 'mmr',
            search_kwargs = {'k': k}
        )
    return _vector_retriever

