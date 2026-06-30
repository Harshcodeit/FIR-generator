import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_legal_document(
    docs: list[Document], 
    chunk_size: int = 800, 
    chunk_overlap: int = 150
) -> list[Document]:
    """Splits legal text by structural anchors before applying size bounds."""
    
    # 1. Define hard logical boundaries
    legal_pattern = re.compile(
        r'(?=\n(?:ARTICLE|SECTION|Section|§|Clause)\s+\d+)'  # Section headers
        r'|(?=\n[A-Z\s]{4,}(?:,|:))'                        # WHEREAS, DEFINITIONS
        r'|(?=\n\s*(?:\([a-z]\)|\d+\.))'                    # Sub-clauses: (a), 1.
        r'|(?=\n\n)'                                         # Paragraphs
    )
    
    # 2. Define standard fallback boundary rules
    fallback_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    
    final_chunks = []
    for doc in docs :
        initial_sections = legal_pattern.split(doc.page_content)

        for section in initial_sections :
            section = section.strip()
            if not section:
                continue

            # if section size is lesser than chunk size
            if len(section) <= chunk_size:
                final_chunks.append(
                    Document(
                        page_content=section,
                        metadata = doc.metadata.copy()
                    )
                )

            # if larger , use the fallback splitter
            else:
                for chunk in fallback_splitter.split_text(section):
                    final_chunks.append(
                        Document(
                            page_content=chunk,
                            metadata = doc.metadata.copy()
                        )
                    )
            
    return final_chunks



