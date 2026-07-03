from app.core.llm import load_llm
from app.core.parser import load_parser
from app.schemas.user_report import UserReportSchema
from app.prompts.extract import extract_prompt
from app.utils.helpers import get_message_text

from langchain_core.runnables import RunnableLambda


llm = load_llm("gemma-4-26b-a4b-it")
parser = load_parser(UserReportSchema)

extract_chain = extract_prompt | llm | RunnableLambda(get_message_text) |parser

def extract_information(incident : str) -> UserReportSchema:
    """It extracts the key information from the user's incident"""
    return extract_chain.invoke({
        'format_instructions' : parser.get_format_instructions(),
        'incident' : incident
    })
