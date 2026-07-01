from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage

# get user schema
from app.schemas.user_report import UserReportSchema

# send reasoning prompt and queries
from app.prompts.analyse import analysis_prompt
from app.prompts.retrieve import BNS_QUERY,BNSS_QUERY

# use retriever to get retrieved context
from app.services.retrieval import retrieve

# use llm to get sections that actually apply
from app.core.llm import load_llm


print("loaded analysis service ===============")


llm = load_llm()


def build_reasoning_input(report : UserReportSchema) -> dict :
    query = f"""
    Offence: {report.offence_description}
    
    Identify:
    - Relevant Bharatiya Nyaya Sanhita (BNS) sections.
    - Definition of the offence.
    - Punishment prescribed.
    - Ingredients required to constitute the offence.
    """

    bns_query = BNS_QUERY.format(offence = report.offence_description)
    bnss_query =BNSS_QUERY.format(offence = report.offence_description)

    docs = retrieve(bns_query,bnss_query)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return  {
        'report' : report.model_dump(),
        'retrieved_docs' : context
    }

analyse_chain = (
    RunnableLambda(build_reasoning_input) |
    analysis_prompt |
    llm 
)

def get_relevant_data(report : UserReportSchema) -> AIMessage :
    return analyse_chain.invoke(report)


