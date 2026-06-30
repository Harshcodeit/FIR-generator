from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from app.rag.config import DOCS_PATH

def load_pdf(filename : str)  -> list[Document] :
    file_path = DOCS_PATH / filename
    return PyPDFLoader(str(file_path)).load()
