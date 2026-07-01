# import re
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document


# def split_legal_document(
#     docs: list[Document], 
#     chunk_size: int = 1000, 
#     chunk_overlap: int = 200
# ) -> list[Document]:
#     """Splits plain legal text cleanly by trapping section transitions"""
    
    

#     legal_pattern = re.compile(
#     r"(?m)^\s*(\d+)\.\s"
#     )
    
#     # 2. Define standard fallback boundary rules
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         separators=["\n\n", "\n", " ", ""]
#     )

    
#     final_chunks = []
#     for doc in docs :
#         initial_sections = legal_pattern.split(doc.page_content)

#         for section in initial_sections :
#             section = section.strip()
#             if not section or len(section) < 40:
#                 continue

#             header_match = re.match(r'^(\d+\s*\.\s*)', section)
#             section_prefix = f"[Section {header_match.group(1).strip()}] " if header_match else ""


#             # if section size is lesser than chunk size
#             if len(section) <= chunk_size:
#                 doc_content = section if section.startswith(section_prefix) else section_prefix + section
#                 final_chunks.append(
#                     Document(
#                         page_content=doc_content,
#                         metadata = doc.metadata.copy()
#                     )
#                 )

#             # if larger , use the fallback splitter
#             else:
#                 for chunk in fallback_splitter.split_text(section):
#                     content = chunk if chunk.startswith(section_prefix) else section_prefix + chunk
#                     final_chunks.append(
#                         Document(
#                             page_content=content,
#                             metadata = doc.metadata.copy()
#                         )
#                     )
            
#     return final_chunks




# import re

# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# SECTION_PATTERN = re.compile(
#     r"(?m)^\s*(\d+)\.\s"
# )


# def split_legal_document(
#     docs: list[Document],
#     chunk_size: int = 1000,
#     chunk_overlap: int = 200
# ) -> list[Document]:

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )

#     # --------- Build complete sections ---------

#     sections = []

#     current_text = ""
#     current_metadata = None

#     for doc in docs:

#         text = doc.page_content.strip()

#         if not text:
#             continue

#         if SECTION_PATTERN.search(text):

#             if current_text:
#                 sections.append(
#                     Document(
#                         page_content=current_text,
#                         metadata=current_metadata.copy()
#                     )
#                 )

#             current_text = text
#             current_metadata = doc.metadata

#         else:

#             if current_text:
#                 current_text += "\n\n" + text

#             else:
#                 current_text = text
#                 current_metadata = doc.metadata

#     if current_text:
#         sections.append(
#             Document(
#                 page_content=current_text,
#                 metadata=current_metadata.copy()
#             )
#         )

#     # --------- Split oversized sections ---------

#     final_chunks = []

#     for section in sections:

#         if len(section.page_content) <= chunk_size:

#             final_chunks.append(section)

#         else:

#             header = section.page_content.split("\n", 1)[0]

#             child_chunks = splitter.split_text(section.page_content)

#             for chunk in child_chunks:

#                 final_chunks.append(
#                     Document(
#                         page_content=f"{header}\n\n{chunk}",
#                         metadata=section.metadata.copy()
#                     )
#                 )

#     return final_chunks


import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Matches:
# 261.
# 262.
# 303.
SECTION_PATTERN = re.compile(r"(?m)^\s*\d+\.")


def split_legal_document(
    docs: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    sections: list[Document] = []

    current_section = ""
    current_metadata = None

    for doc in docs:

        text = doc.page_content.strip()

        if not text:
            continue

        matches = list(SECTION_PATTERN.finditer(text))

        # No new section on this page → continuation
        if not matches:
            if current_section:
                current_section += "\n\n" + text
            else:
                current_section = text
                current_metadata = doc.metadata
            continue

        # Process every section found on this page
        for i, match in enumerate(matches):

            start = match.start()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(text)

            section_text = text[start:end].strip()

            # First section may be continuation of previous page
            if i == 0 and current_section:

                current_section += "\n\n" + section_text

                sections.append(
                    Document(
                        page_content=current_section,
                        metadata=current_metadata.copy(),
                    )
                )

                current_section = ""
                current_metadata = None

            else:

                sections.append(
                    Document(
                        page_content=section_text,
                        metadata=doc.metadata.copy(),
                    )
                )

    # Leftover section
    if current_section:
        sections.append(
            Document(
                page_content=current_section,
                metadata=current_metadata.copy(),
            )
        )

    final_chunks: list[Document] = []

    for section in sections:

        if len(section.page_content) <= chunk_size:
            final_chunks.append(section)
            continue

        header = section.page_content.split("\n", 1)[0]

        for chunk in splitter.split_text(section.page_content):

            final_chunks.append(
                Document(
                    page_content=f"{header}\n\n{chunk}",
                    metadata=section.metadata.copy(),
                )
            )

    return final_chunks