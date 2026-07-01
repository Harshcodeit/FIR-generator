from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.core.embedding_model import load_embeddings
from app.rag.config import VECTOR_DB_PATH



def get_vectorstore(collection_name : str) -> Chroma :
    """Returns a chroma instance tied to a specific collection(e.g. 'bns' or 'bnss') """

    return Chroma(
            collection_name = collection_name,
            embedding_function = load_embeddings(),
            persist_directory = VECTOR_DB_PATH
        )
    
