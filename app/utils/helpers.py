def get_missing_fields(report):
    return [
        field
        for field,value in report.model_dump().items()
        if value is None
    ]

from langchain_core.messages import AIMessage
import re


def clean_fir_text(text: str) -> str:
    # Fix section 3 broken labels
    text = re.sub(
        r"3\.\s*\n\s*\(a\)\s*\n+",
        "3. (a) ",
        text
    )

    text = re.sub(
        r"\n\s*\(b\)\s*\n+",
        "\n   (b) ",
        text
    )

    text = re.sub(
        r"\n\s*\(c\)\s*\n+",
        "\n   (c) ",
        text
    )

    # Fix section 6 broken spacing
    text = re.sub(
        r"6\.\s*Complainant\s*/\s*information\s*:\s*\n+",
        "6. Complainant / Informant:\n",
        text,
        flags=re.I
    )

    text = re.sub(r"\n\s*\(a\)\s*\n+", "\n   (a) ", text)
    text = re.sub(r"\n\s*\(b\)\s*\n+", "\n   (b) ", text)
    text = re.sub(r"\n\s*\(c\)\s*\n+", "\n   (c) ", text)
    text = re.sub(r"\n\s*\(d\)\s*\n+", "\n   (d) ", text)
    text = re.sub(r"\n\s*\(e\)\s*\n+", "\n   (e) ", text)
    text = re.sub(r"\n\s*\(f\)\s*\n+", "\n   (f) ", text)
    text = re.sub(r"\n\s*\(g\)\s*\n+", "\n   (g) ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def get_message_text(message: AIMessage | str) -> str:
    content = message.content if hasattr(message, "content") else message

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        return "\n".join(text_parts).strip()

    return str(content)

