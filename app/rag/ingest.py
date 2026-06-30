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
def add_documents(chunks : list[Document]) -> Chroma :
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    return vectorstore

#  raw documents -> langchain documents -> chunks -> vector id documents
ingest_chain = (
    RunnableLambda(load_pdf) |
    RunnableLambda(split_legal_document) |
    RunnableLambda(add_documents)
)

def ingest_pdf(file_path : str) -> None :
    ingest_chain.invoke(file_path)

