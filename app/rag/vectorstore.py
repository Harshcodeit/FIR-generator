from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.core.embedding_model import load_embeddings
from app.rag.config import VECTOR_DB_PATH


_vectorstore = None

def get_vectorstore() -> Chroma :
    global _vectorstore

    if _vectorstore is None :
        _vectorstore = Chroma(
            embedding_function = load_embeddings(),
            persist_directory = VECTOR_DB_PATH
        )
    return _vectorstore
