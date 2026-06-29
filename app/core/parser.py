from langchain_core.output_parsers import PydanticOutputParser

def load_parser(schema):
    return PydanticOutputParser(
        pydantic_object = schema
    )