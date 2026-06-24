import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama

load_dotenv()

st.set_page_config(page_title="AI FIR Generator")

st.title("AI FIR Generator")

# ---------------- Models ----------------

@st.cache_resource
def load_resources():

    llm = ChatOllama(
        model="mistral:7b",
        temperature=0
    )

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4}
    )

    fir_format = PyPDFLoader(
        "./Documents/format.pdf"
    ).load()

    return llm, retriever, fir_format


llm, retriever, fir_format = load_resources()

# ---------------- UI ----------------

offence_description = st.text_input(
"Offence Description",
placeholder="Bike stolen near mall"
)

approximate_date = st.text_input("Date")
approximate_time = st.text_input("Time")

location_name = st.text_input("Location")
city = st.text_input("City")
state = st.text_input("State")

reporter_full_name = st.text_input("Full Name")
reporter_occupation = st.text_input("Occupation")

# ---------------- Prompts ----------------

prompt_analysis = ChatPromptTemplate.from_messages([
(
"system",
"""
You are a legal analyst.

Determine which sections actually apply.

Do not list sections that merely might apply.

A section is applicable only when its required elements are explicitly supported by the facts.

If evidence is missing, reject the section.

Return:
Applicable Sections
Rejected Sections
Reasoning
"""
),
(
"human",
"""
Facts:
{report}

Candidate Sections:
{retrieved_docs}
"""
)
])

prompt_generate = ChatPromptTemplate.from_messages([
(
"system",
"""
You are an Indian police officer.

Generate a formal FIR.

Use ONLY the legal sections provided.

If information is unavailable write Not Available.

Never use placeholders.
"""
),
(
"human",
"""
Facts:
{report}

Legal Context:
{legal_context}

FIR Template:
{fir_template}

Generate the FIR.
"""
)
])

# ---------------- Generate ----------------

if st.button("Generate FIR"):


    report = {
        "offence_description": offence_description,
        "approximate_date": approximate_date,
        "approximate_time": approximate_time,
        "location_name": location_name,
        "city": city,
        "state": state,
        "reporter_full_name": reporter_full_name,
        "reporter_occupation": reporter_occupation
    }

    query = f"""


    Description of offence:
    {offence_description}

    What are the relevant BNS sections and punishment?
    """


    retrieved_docs = retriever.invoke(query)

    retrieved_context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    fir_template = "\n\n".join(
        page.page_content
        for page in fir_format
    )

    with st.spinner("Analyzing law..."):

        analysis_prompt = prompt_analysis.invoke({
            "report": report,
            "retrieved_docs": retrieved_context
        })

        legal_context = llm.invoke(
            analysis_prompt
        ).content

    with st.spinner("Generating FIR..."):

        fir_prompt = prompt_generate.invoke({
            "report": report,
            "legal_context": legal_context,
            "fir_template": fir_template
        })

        fir_text = llm.invoke(
            fir_prompt
        ).content

    st.subheader("Legal Analysis")
    st.text(legal_context)

    st.subheader("Generated FIR")

    st.text_area(
        "",
        value=fir_text,
        height=600
    )

