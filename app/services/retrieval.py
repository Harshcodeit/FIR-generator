from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document

from rich import print


# get retriever
from app.rag.retriever import get_retriever

retrieve_chain = RunnableLambda(
    lambda query : get_retriever().invoke(query)
)

def retrieve(query : str) -> list[Document] : 
    docs = retrieve_chain.invoke(query)
    for doc in docs:
        print(doc.metadata["page"])
        print(doc.page_content)
        print("=" * 80)
    return docs





