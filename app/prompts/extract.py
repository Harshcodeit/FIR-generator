from langchain_core.prompts import ChatPromptTemplate

# a system message and human message
extract_prompt = ChatPromptTemplate.from_messages([
    (
        'system','''
Extract important information from the paragraph.
Return ONLY a raw JSON object matching the requested schema. 

If information is not present,
return null.

Never invent placeholder values.
Never output CityName, StateName, ReporterName, etc.
{format_instructions}
'''
    ),
    (
        'human',"{incident}"
    )
])
