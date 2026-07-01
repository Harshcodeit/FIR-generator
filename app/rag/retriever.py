from langchain_core.vectorstores import VectorStoreRetriever

# get vector database
from app.rag.vectorstore import get_vectorstore


def get_retriever(k : int = 4) -> list[VectorStoreRetriever] :
    """Queries both BNS and BNSS collections"""

    bns_retriever = get_vectorstore(collection_name='bns').as_retriever(
        search_type = 'mmr',
        search_kwargs={'k' : k}
    )
    bnss_retriever = get_vectorstore(collection_name='bnss').as_retriever(
        search_type = 'mmr',
        search_kwargs={'k' : k}
    )

    return [bns_retriever,bnss_retriever]




