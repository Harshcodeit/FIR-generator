# from langchain_core.runnables import RunnableLambda
# from langchain_core.documents import Document

# # get retriever
# from app.rag.retriever import get_retriever

# bns_retriever,bnss_retriever = get_retriever() # embedding model will always be instatiated whenver import is done


# retrieve_chain = RunnableLambda(
#     lambda queries : (
#         # bns + bnss docs
#         bns_retriever.invoke(queries['query1']) +
#         bnss_retriever.invoke(queries['query2'])
#     )
# )

# def retrieve(query1 : str , query2  : str) -> list[Document] : 
#     docs = retrieve_chain.invoke({
#         'query1' : query1,
#         'query2' : query2
#     })
#     for doc in docs:
#         print(doc.metadata["page"])
#         print(doc.page_content)
#         print("=" * 80)
#     return docs

import re
from collections import Counter

from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document

# get retriever
from app.rag.retriever import get_retriever


bns_retriever, bnss_retriever = get_retriever()


STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "by", "from", "is", "are", "was", "were", "be", "been", "being",
    "this", "that", "these", "those", "incident", "reported", "find",
    "section", "sections", "bns", "bnss", "offence", "crime", "criminal",
    "definition", "ingredients", "punishment", "procedure", "relevant",
    "directly", "main", "core", "basic"
}


def _extract_incident_text(query: str) -> str:
    """
    Extracts only the user incident/offence from the retrieval prompt.
    This prevents words like 'definition', 'ingredients', 'punishment'
    from polluting keyword search.
    """

    patterns = [
        r"Reported incident:\s*(.*?)(?:\n\s*\n|$)",
        r"Incident:\s*(.*?)(?:\n\s*\n|$)",
        r"Offence:\s*(.*?)(?:\n\s*\n|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.I | re.S)

        if match:
            return match.group(1).strip()

    return query.strip()


def _tokens(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())

    return [
        word
        for word in words
        if word not in STOPWORDS
    ]


def _extract_section_title(doc: Document) -> str:
    """
    Extracts title from:
    [Section 303]

    303. Theft.—(1) Whoever...
    """

    text = doc.page_content.strip()

    match = re.search(
        r"^\[Section\s+\d+\]\s*\n+\s*\d+\.\s*(.*)",
        text,
        re.I | re.S
    )

    if not match:
        return ""

    rest = match.group(1).strip()

    # Stop title at legal dash / first sentence / newline
    parts = re.split(r"\s*\.\s*—|\s*—|\n", rest, maxsplit=1)

    title = parts[0].strip()

    if len(title) > 180:
        title = title[:180].strip()

    return title


def _keyword_score(query: str, doc: Document) -> int:
    incident = _extract_incident_text(query)

    query_tokens = _tokens(incident)

    if not query_tokens:
        return 0

    query_set = set(query_tokens)

    title = _extract_section_title(doc)
    title_tokens = _tokens(title)
    title_set = set(title_tokens)

    # Only score beginning of section body, not huge table tails
    body_tokens = _tokens(doc.page_content[:3500])
    body_counter = Counter(body_tokens)

    score = 0

    for token in query_set:
        # Strong boost if incident word appears in section title
        if token in title_set:
            score += 25

        # Smaller boost if incident word appears in body
        if token in body_counter:
            score += min(body_counter[token], 8) * 3

    title_lower = title.lower().strip()
    incident_lower = incident.lower().strip()

    # Example:
    # incident = "motorcycle theft"
    # title = "Theft"
    if title_lower and title_lower in incident_lower:
        score += 40

    # Prefer shorter direct offence titles over aggravated long titles
    # Example:
    # "Theft" beats "Theft after preparation..."
    if title_set & query_set:
        score += max(0, 20 - len(title_tokens))

    return score


def _keyword_search_bns(query: str, limit: int = 3) -> list[Document]:
    """
    Keyword/legal-title search over all BNS chunks.
    BNS has limited sections, so this is cheap and reliable.
    """

    result = bns_retriever.vectorstore.get(
        include=["documents", "metadatas"]
    )

    documents = result.get("documents", [])
    metadatas = result.get("metadatas", [])

    scored_docs = []

    for text, metadata in zip(documents, metadatas):
        doc = Document(
            page_content=text,
            metadata=metadata or {}
        )

        score = _keyword_score(query, doc)

        if score > 0:
            scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [
        doc
        for score, doc in scored_docs[:limit]
    ]


def _dedupe_by_section(docs: list[Document], limit: int) -> list[Document]:
    seen = set()
    final_docs = []

    for doc in docs:
        section_number = doc.metadata.get("section_number")
        source = doc.metadata.get("source", "")

        if section_number:
            key = (source, section_number)
        else:
            key = doc.page_content[:200]

        if key in seen:
            continue

        seen.add(key)
        final_docs.append(doc)

        if len(final_docs) >= limit:
            break

    return final_docs


def _retrieve_docs(queries: dict) -> list[Document]:
    bns_query = queries["query1"]
    bnss_query = queries["query2"]

    # 1. Dense semantic search
    bns_semantic_docs = bns_retriever.invoke(bns_query)

    # 2. Keyword/title search
    bns_keyword_docs = _keyword_search_bns(
        query=bns_query,
        limit=3
    )

    # 3. Put keyword docs first so direct offence section enters context
    bns_docs = _dedupe_by_section(
        docs=bns_keyword_docs + bns_semantic_docs,
        limit=5
    )

    # 4. BNSS remains small
    bnss_docs = bnss_retriever.invoke(bnss_query)
    bnss_docs = _dedupe_by_section(
        docs=bnss_docs,
        limit=2
    )

    return bns_docs + bnss_docs


retrieve_chain = RunnableLambda(_retrieve_docs)


def retrieve(query1: str, query2: str) -> list[Document]:
    docs = retrieve_chain.invoke({
        "query1": query1,
        "query2": query2
    })

    # for doc in docs:
        # print(doc.metadata.get("page", "N/A"))
        # print(doc.page_content)
        # print("=" * 80)

    return docs