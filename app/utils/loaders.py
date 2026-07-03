from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from app.rag.config import DOCS_PATH

def load_pdf(filename: str | Path) -> list[Document]:
    file_path = Path(filename)

    if not file_path.is_absolute():
        file_path = DOCS_PATH / file_path

    if not file_path.exists():
        raise FileNotFoundError(f"PDF not found at: {file_path}")

    return PyPDFLoader(str(file_path)).load()