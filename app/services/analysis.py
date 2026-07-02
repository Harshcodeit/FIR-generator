import json

from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage

# get user schema
from app.schemas.user_report import UserReportSchema

# send reasoning prompt and queries
from app.prompts.analyse import analysis_prompt
from app.prompts.retrieve import BNS_QUERY, BNSS_QUERY

# use retriever to get retrieved context
from app.services.retrieval import retrieve

# use llm to get sections that actually apply
from app.core.llm import load_llm




llm = load_llm()


def _format_report(report: UserReportSchema) -> str:
    data = report.model_dump()

    offence_description = data.get("offence_description", "")

    return f"""
Offence Description:
{offence_description}

Full Report Data:
{json.dumps(data, indent=2, ensure_ascii=False)}
""".strip()


def _format_retrieved_docs(docs) -> str:
    formatted_docs = []

    for idx, doc in enumerate(docs, start=1):
        section_number = doc.metadata.get("section_number", "unknown")
        source = doc.metadata.get("source", "")
        act = doc.metadata.get("act", "")

        formatted_docs.append(
            f"""
================ CANDIDATE {idx} ================
Metadata:
Section Number: {section_number}
Source: {source}
Act: {act}

Content:
{doc.page_content}
""".strip()
        )

    return "\n\n".join(formatted_docs)


def build_reasoning_input(report: UserReportSchema) -> dict:
    bns_query = BNS_QUERY.format(
        offence=report.offence_description
    )

    bnss_query = BNSS_QUERY.format(
        offence=report.offence_description
    )

    docs = retrieve(bns_query, bnss_query)

    context = _format_retrieved_docs(docs)

    return {
        "report": _format_report(report),
        "retrieved_docs": context
    }


analyse_chain = (
    RunnableLambda(build_reasoning_input)
    | analysis_prompt
    | llm
)


def get_relevant_data(report: UserReportSchema) -> AIMessage:
    return analyse_chain.invoke(report)