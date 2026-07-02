from langchain_core.vectorstores import VectorStoreRetriever

from app.rag.vectorstore import get_vectorstore


def get_retriever(k: int = 5) -> list[VectorStoreRetriever]:
    """Queries both BNS and BNSS collections"""

    bns_retriever = get_vectorstore(collection_name='bns').as_retriever(
        search_type='similarity',
        search_kwargs={'k': k}
    )

    bnss_retriever = get_vectorstore(collection_name='bnss').as_retriever(
        search_type='similarity',
        search_kwargs={'k': max(1, min(2, k // 2))}
    )

    return [bns_retriever, bnss_retriever]