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

from functools import lru_cache

@lru_cache(maxsize=1)
def get_fir_template() -> str:
    return load_pdf("format.pdf")[0].page_content


def build_generation_input(data : dict) -> dict :
    report : UserReportSchema = data['report']
    legal_context : AIMessage = data['legal_context']

    return {
        'report' : report.model_dump(),
        'legal_context' : get_message_text(legal_context),
        'fir_template' : get_fir_template()
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








