from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document

# get retriever
from app.rag.retriever import get_retriever

bns_retriever,bnss_retriever = get_retriever()


retrieve_chain = RunnableLambda(
    lambda queries : (
        # bns + bnss docs
        bns_retriever.invoke(queries['query1']) +
        bnss_retriever.invoke(queries['query2'])
    )
)

def retrieve(query1 : str , query2  : str) -> list[Document] : 
    docs = retrieve_chain.invoke({
        'query1' : query1,
        'query2' : query2
    })
    # for doc in docs:
    #     print(doc.metadata["page"])
    #     print(doc.page_content)
    #     print("=" * 80)
    return docs








