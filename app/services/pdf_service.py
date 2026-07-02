
"""
FIR PDF generation service.

Builds a compact, government-style First Information Report (FIR) PDF
from structured report metadata, an LLM legal-analysis message, and an
LLM-generated FIR narrative.

Design goals:
- Single source of truth for metadata is `UserReportSchema` (never parsed
  from the narrative text).
- Only the "Applicable Sections" portion of the legal analysis is shown.
- Consistent typography between table cells and body paragraphs.
- Fits comfortably within 1-2 pages with no large dead space.
"""

from datetime import datetime
from pathlib import Path

from langchain_core.messages import AIMessage

from app.schemas.user_report import UserReportSchema

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    SimpleDocTemplate,
    KeepTogether,
)

# --------------------------------------------------------------------------- #
# Output location
# --------------------------------------------------------------------------- #

OUTPUT_DIR = Path("generated_firs")
OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------------------------------------------------------- #
# Layout constants
# --------------------------------------------------------------------------- #

PAGE_SIZE = A4
MARGIN = 1.5 * cm

# A single font size drives both table cells and body paragraphs so the
# document reads as one consistent typeface, not a mix of debug-table text
# and prose.
BASE_FONT_SIZE = 9.5
LEADING = BASE_FONT_SIZE + 3.5

LABEL_COL_WIDTH = 4.2 * cm
VALUE_COL_WIDTH = PAGE_SIZE[0] - 2 * MARGIN - LABEL_COL_WIDTH

# --------------------------------------------------------------------------- #
# Unicode font registration (needed to render "₹" and other non-Latin-1
# glyphs). Falls back to the built-in Helvetica family if no system Unicode
# font is found -- no new package dependency is introduced either way.
# --------------------------------------------------------------------------- #

_UNICODE_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def _register_unicode_font() -> None:
    """
    Try to register DejaVu Sans (commonly preinstalled on Linux) so that
    currency symbols such as ₹ render correctly. If unavailable, the base
    Helvetica fonts are kept and callers should rely on `safe_text()` to
    avoid glyphs Helvetica cannot render.
    """
    global FONT_REGULAR, FONT_BOLD

    regular_path = Path(_UNICODE_FONT_CANDIDATES[0])
    bold_path = Path(_UNICODE_FONT_CANDIDATES[1])

    if regular_path.exists():
        pdfmetrics.registerFont(TTFont("DejaVuSans", str(regular_path)))
        FONT_REGULAR = "DejaVuSans"

        if bold_path.exists():
            pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(bold_path)))
            FONT_BOLD = "DejaVuSans-Bold"
        else:
            FONT_BOLD = "DejaVuSans"


_register_unicode_font()


def safe_text(value: str) -> str:
    """
    Guard against characters the active font cannot render. Only kicks in
    when we ended up on the Helvetica fallback (no Unicode font found).
    """
    if FONT_REGULAR != "Helvetica":
        return value
    return value.replace("₹", "Rs. ")


# --------------------------------------------------------------------------- #
# Styles
# --------------------------------------------------------------------------- #

_stylesheet = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "FIRTitle",
    parent=_stylesheet["Heading1"],
    fontName=FONT_BOLD,
    fontSize=15,
    alignment=TA_CENTER,
    spaceAfter=2,
)

SUBTITLE_STYLE = ParagraphStyle(
    "FIRSubtitle",
    parent=_stylesheet["BodyText"],
    fontName=FONT_REGULAR,
    fontSize=9,
    textColor=colors.grey,
    alignment=TA_CENTER,
    spaceAfter=10,
)

SECTION_HEADING_STYLE = ParagraphStyle(
    "SectionHeading",
    parent=_stylesheet["Heading2"],
    fontName=FONT_BOLD,
    fontSize=11,
    spaceBefore=8,
    spaceAfter=4,
    textColor=colors.HexColor("#1a1a1a"),
)

BODY_STYLE = ParagraphStyle(
    "FIRBody",
    parent=_stylesheet["BodyText"],
    fontName=FONT_REGULAR,
    fontSize=BASE_FONT_SIZE,
    leading=LEADING,
    spaceAfter=4,
)

TABLE_LABEL_STYLE = ParagraphStyle(
    "TableLabel",
    parent=BODY_STYLE,
    fontName=FONT_BOLD,
    fontSize=BASE_FONT_SIZE,
    leading=LEADING,
)

TABLE_VALUE_STYLE = ParagraphStyle(
    "TableValue",
    parent=BODY_STYLE,
    fontName=FONT_REGULAR,
    fontSize=BASE_FONT_SIZE,
    leading=LEADING,
)

FOOTER_LABEL_STYLE = ParagraphStyle(
    "FooterLabel",
    parent=BODY_STYLE,
    alignment=TA_CENTER,
    fontSize=8.5,
)


# --------------------------------------------------------------------------- #
# Small reusable helpers
# --------------------------------------------------------------------------- #

def section_heading(text: str):
    """A styled section heading, e.g. 'Complainant Details'."""
    return Paragraph(text, SECTION_HEADING_STYLE)


def body_paragraph(text: str):
    """A styled body paragraph with consistent font size/leading."""
    return Paragraph(safe_text(text), BODY_STYLE)


def field_table(rows: list[tuple[str, str]]) -> Table:
    """
    Build a compact two-column label/value table. Every row is passed
    through Paragraph so long values wrap instead of overflowing, and the
    font matches body text exactly.

    `rows` is a list of (label, value) tuples. Empty values are rendered
    as an em dash so blank fields don't look like a rendering bug.
    """
    data = []
    for label, value in rows:
        display_value = value.strip() if value else "—"
        data.append(
            [
                Paragraph(label, TABLE_LABEL_STYLE),
                Paragraph(safe_text(display_value), TABLE_VALUE_STYLE),
            ]
        )

    table = Table(data, colWidths=[LABEL_COL_WIDTH, VALUE_COL_WIDTH])
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bfbfbf")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f2f2f2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def extract_section(text: str, start_marker: str, end_markers: list[str]) -> str:
    """
    Extract the text between `start_marker` and the first occurring
    `end_marker` (case-insensitive). If `start_marker` is missing, returns
    an empty string. If no end marker is found, returns everything after
    the start marker.

    This keeps the legal-analysis parsing generic and reusable, rather than
    hardcoding a single "Applicable Sections" extraction.
    """
    lower_text = text.lower()
    start_idx = lower_text.find(start_marker.lower())
    if start_idx == -1:
        return ""

    start_idx += len(start_marker)

    end_idx = len(text)
    for marker in end_markers:
        idx = lower_text.find(marker.lower(), start_idx)
        if idx != -1:
            end_idx = min(end_idx, idx)

    return text[start_idx:end_idx].strip()


# --------------------------------------------------------------------------- #
# Story builders (each appends to the shared `story` list)
# --------------------------------------------------------------------------- #

def build_header(story: list) -> None:
    """Document title block."""
    story.append(Paragraph("FIRST INFORMATION REPORT", TITLE_STYLE))
    story.append(Paragraph("Prepared under Section 154 Cr.P.C.", SUBTITLE_STYLE))

    generated_on = datetime.now().strftime("%d %b %Y, %I:%M %p")
    story.append(
        field_table(
            [
                ("Status", "Draft — Generated by AI FIR Assistant"),
                ("Generated On", generated_on),
            ]
        )
    )
    story.append(Spacer(1, 0.3 * cm))


def build_complainant_details(story: list, report: UserReportSchema) -> None:
    """Complainant identity block."""
    story.append(section_heading("Complainant Details"))
    story.append(
        field_table(
            [
                ("Full Name", report.reporter_full_name),
                ("Father / Husband's Name", report.father_or_husband_name),
                ("Date of Birth", report.dob),
                ("Occupation", report.occupation),
                ("Nationality", report.nationality),
                ("Phone Number", report.phone_number),
                ("Address", report.address),
            ]
        )
    )


def build_incident_details(story: list, report: UserReportSchema) -> None:
    """Offence, date/time, and location block."""
    story.append(section_heading("Incident Details"))
    story.append(
        field_table(
            [
                ("Offence", report.offence_description),
                ("Date", report.offence_date),
                ("Time", report.offence_time),
            ]
        )
    )
    story.append(Spacer(1, 0.15 * cm))
    story.append(
        field_table(
            [
                ("Location", report.location_name),
                ("Landmark", report.landmark),
                ("City", report.city),
                ("State", report.state),
            ]
        )
    )


def build_property_and_accused(story: list, report: UserReportSchema) -> None:
    """Accused description and property/value block."""
    story.append(section_heading("Property & Accused"))
    story.append(
        field_table(
            [
                ("Accused Description", report.accused_description),
                ("Property Involved", report.property_type),
                ("Estimated Value", report.estimated_value),
                ("Reason for Delay", report.delay_reason),
            ]
        )
    )


def build_applicable_sections(story: list, legal_analysis: AIMessage) -> None:
    """
    Renders only applicable BNS sections and procedurally relevant BNSS sections.
    Rejected sections and reasoning are intentionally omitted.
    """
    story.append(section_heading("Applicable Sections"))

    bns_text = extract_section(
        legal_analysis.content,
        start_marker="Applicable BNS Sections:",
        end_markers=[
            "Procedurally Relevant BNSS Sections:",
            "Rejected Sections:",
            "Reasoning:",
        ],
    )

    bnss_text = extract_section(
        legal_analysis.content,
        start_marker="Procedurally Relevant BNSS Sections:",
        end_markers=[
            "Rejected Sections:",
            "Reasoning:",
        ],
    )

    if bns_text:
        story.append(body_paragraph("BNS Sections:"))
        for line in bns_text.splitlines():
            line = line.strip(" -•\t")
            if line:
                story.append(body_paragraph(f"• {line}"))

    if bnss_text:
        story.append(body_paragraph("BNSS Sections:"))
        for line in bnss_text.splitlines():
            line = line.strip(" -•\t")
            if line:
                story.append(body_paragraph(f"• {line}"))

    if not bns_text and not bnss_text:
        story.append(body_paragraph("No applicable sections were identified."))

def build_fir_narrative(story: list, fir: AIMessage) -> None:
    """
    Renders the FIR narrative as clean, separated paragraphs (blank lines
    in the source become paragraph breaks rather than a single wall of
    text with manual <br/> tags).
    """
    story.append(section_heading("Generated FIR Narrative"))

    paragraphs = [p.strip() for p in fir.content.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [fir.content.strip()]

    for para in paragraphs:
        # Collapse single newlines within a paragraph into spaces so text
        # wraps naturally instead of breaking mid-sentence.
        cleaned = " ".join(line.strip() for line in para.splitlines() if line.strip())
        story.append(body_paragraph(cleaned))


def build_footer(story: list) -> None:
    """Signature block."""
    story.append(Spacer(1, 0.8 * cm))

    signature_table = Table(
        [
            ["________________________", "________________________"],
            [
                Paragraph("Complainant Signature", FOOTER_LABEL_STYLE),
                Paragraph("Investigating Officer", FOOTER_LABEL_STYLE),
            ],
        ],
        colWidths=[VALUE_COL_WIDTH / 2 + LABEL_COL_WIDTH / 2] * 2,
    )
    signature_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 1), (-1, 1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ]
        )
    )
    story.append(KeepTogether(signature_table))


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def generate_pdf(
    report: UserReportSchema,
    legal_analysis: AIMessage,
    fir: AIMessage,
    filename: str = "FIR.pdf",
) -> Path:
    """
    Generate a compact, government-style FIR PDF.

    Metadata is always sourced from `report` (never parsed from the FIR
    narrative). `legal_analysis` is filtered down to only its "Applicable
    Sections" portion. `fir` supplies the final narrative text.
    """
    output_path = OUTPUT_DIR / filename

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=PAGE_SIZE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="First Information Report",
    )

    story: list = []

    build_header(story)
    build_complainant_details(story, report)
    story.append(Spacer(1, 0.2 * cm))
    build_incident_details(story, report)
    story.append(Spacer(1, 0.2 * cm))
    build_property_and_accused(story, report)
    story.append(Spacer(1, 0.2 * cm))
    build_applicable_sections(story, legal_analysis)
    story.append(Spacer(1, 0.2 * cm))
    build_fir_narrative(story, fir)
    build_footer(story)

    doc.build(story)

    return output_path


# --------------------------------------------------------------------------- #
# Manual smoke test (run this file directly to generate a sample FIR.pdf)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
from app.core.constants import report, legal_analysis, fir

generate_pdf(report, legal_analysis, fir)