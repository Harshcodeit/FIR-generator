# import re

# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# SECTION_PATTERN = re.compile(r"(?m)^\s*(\d+)\.")


# def split_legal_document(
#     docs: list[Document],
#     chunk_size: int = 3500,
#     chunk_overlap: int = 500,
# ) -> list[Document]:

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         separators=[
#             "\n\n",
#             "\n",
#             ". ",
#             " ",
#             ""
#         ]
#     )

#     # Merge every page into one big text
#     full_text = "\n".join(doc.page_content for doc in docs)

#     matches = list(SECTION_PATTERN.finditer(full_text))

#     sections = []

#     for i, match in enumerate(matches):

#         start = match.start()

#         if i + 1 < len(matches):
#             end = matches[i + 1].start()
#         else:
#             end = len(full_text)

#         section_text = full_text[start:end].strip()

#         sections.append(
#             Document(
#                 page_content=section_text,
#                 metadata=docs[0].metadata.copy()
#             )
#         )

#     final_chunks = []

#     for section in sections:

#         header_match = SECTION_PATTERN.match(section.page_content)

#         if header_match:
#             section_number = header_match.group(1)
#             header = f"[Section {section_number}]"
#         else:
#             header = "[Unknown Section]"

#         if len(section.page_content) <= chunk_size:

#             final_chunks.append(
#                 Document(
#                     page_content=f"{header}\n\n{section.page_content}",
#                     metadata=section.metadata.copy()
#                 )
#             )

#             continue

#         child_chunks = splitter.split_text(section.page_content)

#         for chunk in child_chunks:

#             final_chunks.append(
#                 Document(
#                     page_content=f"{header}\n\n{chunk}",
#                     metadata=section.metadata.copy()
#                 )
#             )

#     return final_chunks

import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Matches legal section starts:
# 303.
# 307.Whoever
# 531. Repeal
#
# Does NOT match:
# 2.5.4.20
SECTION_PATTERN = re.compile(r"(?m)^\s*(\d{1,4})\.(?!\d)")


def _clean_pdf_text(text: str) -> str:
    # Remove long PDF/Gazette divider garbage
    text = re.sub(r"_{10,}", "\n", text)

    # Remove common Gazette headers/footers
    text = re.sub(r"(?im)^.*THE GAZETTE OF INDIA EXTRAORDINARY.*$", "", text)
    text = re.sub(r"(?im)^.*\[Part II.*$", "", text)
    text = re.sub(r"(?im)^Sec\.\s*\d+\].*$", "", text)

    # Remove standalone page numbers
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)

    # Remove digital signature garbage
    text = re.sub(r"(?im)^.*Digitally signed.*$", "", text)
    text = re.sub(r"(?im)^.*Government of India Press.*$", "", text)
    text = re.sub(r"(?im)^.*serialNumber=.*$", "", text)
    text = re.sub(r"(?im)^.*postalCode=.*$", "", text)
    text = re.sub(r"(?im)^.*pseudonym=.*$", "", text)
    text = re.sub(r"(?im)^.*Date:\s*\d{4}\.\d{2}\.\d{2}.*$", "", text)

    # Remove chapter side headings that leak into previous section
    text = re.sub(r"(?m)^\s*Of theft\s*$", "", text)
    text = re.sub(r"(?m)^\s*Of extortion\s*$", "", text)
    text = re.sub(r"(?m)^\s*Of robbery and dacoity\s*$", "", text)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _take_section_opening(text: str, limit: int = 1000) -> str:
    text = text.strip()

    if len(text) <= limit:
        return text

    cut = text.rfind("\n", 0, limit)

    if cut == -1:
        cut = text.rfind(". ", 0, limit)

    if cut == -1:
        cut = limit

    return text[:cut].strip()


def split_legal_document(
    docs: list[Document],
    chunk_size: int = 8000,
    chunk_overlap: int = 500,
) -> list[Document]:

    if not docs:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    # Merge all pages first
    full_text = "\n".join(doc.page_content for doc in docs)
    full_text = _clean_pdf_text(full_text)

    matches = list(SECTION_PATTERN.finditer(full_text))

    # First collect all section candidates
    # Same section may appear multiple times:
    # 303. Theft.             -> title/table entry
    # 303. Theft.—(1) Whoever -> actual full section
    section_map: dict[str, str] = {}

    for i, match in enumerate(matches):
        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(full_text)

        section_text = full_text[start:end].strip()

        if not section_text:
            continue

        header_match = SECTION_PATTERN.match(section_text)

        if not header_match:
            continue

        section_number = header_match.group(1)

        # Keep the longest version of the same section.
        # This removes title-only chunks like:
        # 303. Theft.
        if section_number not in section_map:
            section_map[section_number] = section_text
        else:
            if len(section_text) > len(section_map[section_number]):
                section_map[section_number] = section_text

    final_chunks: list[Document] = []

    # Process sections in numeric order
    for section_number in sorted(section_map.keys(), key=lambda x: int(x)):
        section_text = section_map[section_number].strip()

        if not section_text:
            continue

        header = f"[Section {section_number}]"

        metadata = docs[0].metadata.copy()
        metadata["section_number"] = section_number
        metadata["parent_id"] = f"section_{section_number}"

        # Keep normal legal sections fully intact
        if len(section_text) <= chunk_size:
            final_chunks.append(
                Document(
                    page_content=f"{header}\n\n{section_text}",
                    metadata={
                        **metadata,
                        "chunk_type": "full_section",
                        "chunk_index": 0,
                        "total_chunks": 1,
                    }
                )
            )

            continue

        # Split only very large sections
        section_opening = _take_section_opening(section_text, limit=1000)

        child_chunks = splitter.split_text(section_text)

        for idx, chunk in enumerate(child_chunks):
            chunk_metadata = {
                **metadata,
                "chunk_type": "split_large_section",
                "chunk_index": idx,
                "total_chunks": len(child_chunks),
            }

            if idx == 0:
                page_content = f"""
{header}

{chunk}
""".strip()
            else:
                page_content = f"""
{header}

[Section Opening]
{section_opening}

[Current Text]
{chunk}
""".strip()

            final_chunks.append(
                Document(
                    page_content=page_content,
                    metadata=chunk_metadata
                )
            )

    return final_chunks