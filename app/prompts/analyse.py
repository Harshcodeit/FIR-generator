from langchain_core.prompts import ChatPromptTemplate

analysis_prompt = ChatPromptTemplate.from_messages([
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
