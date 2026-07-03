from pathlib import Path
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

# fir_template + report + legal_context -> llm -> FIR
from app.prompts.generate import generate_prompt
from app.utils.loaders import load_pdf
from app.utils.helpers import get_message_text
# load model to generate FIR
from app.core.llm import load_llm
# to validate report
from app.schemas.user_report import UserReportSchema

BASE_DIR = Path(__file__).resolve().parents[2]
FORMAT_PDF_PATH = BASE_DIR / "documents" / "format.pdf"


template = load_pdf(FORMAT_PDF_PATH)[0].page_content

def build_generation_input(data : dict) -> dict :
    report : UserReportSchema = data['report']
    legal_context : AIMessage = data['legal_context']

    return {
        'report' : report.model_dump(),
        'legal_context' : get_message_text(legal_context),
        'fir_template' : template 
    }

llm = load_llm()

generate_chain = (
    RunnableLambda(build_generation_input) |
    generate_prompt | 
    llm
)

def generate_fir(data : dict) -> AIMessage :
    response = generate_chain.invoke(data)
    return AIMessage(content = get_message_text(response))








