# take raw data and prepare it for storage
# raw documents -> vector indexed kb

# wrap python functions to convert to runnables
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from langchain_chroma import Chroma

# import loader,chunker,vectorstore
from app.utils.loaders import load_pdf
from app.rag.chunking import split_legal_document
from app.rag.vectorstore import get_vectorstore


# add to vector store
def add_documents(payload : dict) -> Chroma :
    """Receives chunks and collection name,then commits them directly"""
    chunks = payload['chunks']
    collection_name = payload['collection_name']

    # grab right collection
    vectorstore = get_vectorstore(collection_name=collection_name)
    vectorstore.add_documents(chunks)

    return vectorstore

#  raw documents -> langchain documents -> chunks -> vector id documents
ingest_chain = (
    RunnableLambda(lambda payload : {
        'chunks' : split_legal_document(load_pdf(payload['file_name'])),
        'collection_name' : payload['collection_name']
    }) |
    RunnableLambda(add_documents)
)

def ingest_pdf(file_name : str,collection_name : str) -> None :
    ingest_chain.invoke({
        'file_name' : file_name,
        'collection_name' : collection_name
    })


ingest_pdf('BNS.pdf','bns')
ingest_pdf('BNSS.pdf','bnss')
print("Loaded...")