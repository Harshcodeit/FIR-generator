from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

# fir_template + report + legal_context -> llm -> FIR
from app.prompts.generate import generate_prompt
from app.utils.loaders import load_pdf

# load model to generate FIR
from app.core.llm import load_llm

# to validate report
from app.schemas.user_report import UserReportSchema

template = load_pdf('format.pdf')[0].page_content

def build_generation_input(data : dict) -> dict :
    report : UserReportSchema = data['report']
    legal_context : AIMessage = data['legal_context']

    return {
        'report' : report.model_dump(),
        'legal_context' : legal_context.content,
        'fir_template' : template
    }

llm = load_llm()

generate_chain = (
    RunnableLambda(build_generation_input) |
    generate_prompt | 
    llm
)

def generate_fir(data : dict) -> AIMessage :
    return generate_chain.invoke(data)


# testing
from rich import print
from app.services.extraction import extract_information
from app.services.questioning import fill_missing_information
from app.services.analysis import get_relevant_data

report = extract_information("""My name is Harshit Singh. I am 24 years old, an Indian national, and I work as a Software Engineer. I live at 14 Akash Deep Enclave, Kolkata, West Bengal. My phone number is 9876543210.

On 30 June 2026 at around 4:00 PM, I parked my black Royal Enfield Classic 350 motorcycle near Akash Deep Enclave, close to City Centre Mall in Kolkata, West Bengal. When I returned after about an hour, the motorcycle was missing. The estimated value of the motorcycle is around ₹1,80,000.

I do not know the identity of the accused, but a nearby shopkeeper mentioned seeing a man wearing a black hoodie and blue jeans loitering around the parking area before the theft.

I could not report the matter immediately because I was searching for the motorcycle in nearby areas and also checking with local security guards. Therefore, I am filing this complaint today.""")


complete_report = fill_missing_information(report)

relevant_data = get_relevant_data(complete_report)

print(generate_fir({
    'report': complete_report,
    'legal_context' : relevant_data
}))