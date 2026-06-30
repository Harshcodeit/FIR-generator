from app.core.llm import load_llm
from app.core.parser import load_parser
from app.schemas.user_report import UserReportSchema
from app.prompts.extract import extract_prompt
from rich import print

llm = load_llm()
parser = load_parser(UserReportSchema)

extract_chain = extract_prompt | llm | parser

def extract_information(incident : str) -> UserReportSchema:
    """It extracts the key information from the user's incident"""
    return extract_chain.invoke({
        'format_instructions' : parser.get_format_instructions(),
        'incident' : incident
    })
