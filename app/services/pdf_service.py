# from langchain_core.messages import AIMessage

# from pathlib import Path
# from app.core.constants import temp_summary


# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.enums import TA_CENTER
# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Paragraph,
#     Spacer
# )

# OUTPUT_DIR = Path("generated_firs") # create folder inside project root
# OUTPUT_DIR.mkdir(exist_ok=True)


# def generate_pdf(
#     fir: AIMessage,
#     filename: str = "FIR.pdf"
# ) -> Path:
#     """
#     Converts generated FIR into a nicely formatted PDF.
#     """
#     output_path = OUTPUT_DIR / filename

#     styles = getSampleStyleSheet()

#     title_style = styles["Heading1"]
#     title_style.alignment = TA_CENTER

#     body_style = styles["BodyText"]
#     body_style.leading = 18

#     doc = SimpleDocTemplate(str(output_path))

#     story = []
#     story.append(Paragraph("FIRST INFORMATION REPORT", title_style))
#     story.append(Spacer(1, 20))

#     # Preserve line breaks
#     for line in fir.content.splitlines():

#         if line.strip() == "":
#             story.append(Spacer(1, 10))
#             continue

#         story.append(
#             Paragraph(
#                 line.replace(" ", "&nbsp;"),
#                 body_style
#             )
#         )

#     doc.build(story)
#     return output_path

# generate_pdf(temp_summary)

from langchain_core.messages import AIMessage
from pathlib import Path
from app.core.constants import temp_summary

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

OUTPUT_DIR = Path("generated_firs")  # create folder inside project root
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_pdf(
    fir: AIMessage,
    filename: str = "FIR.pdf"
) -> Path:
    """
    Converts generated FIR into a nicely formatted, structured 2-page FIR PDF.
    """
    output_path = OUTPUT_DIR / filename
    content_text = getattr(fir, 'content', str(fir))

    # Strict A4 template initialization with tight 15mm margins to fix spacing issues
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    story = []
    
    # -------------------------------------------------------------------------
    # Typography & Styles Setup
    # -------------------------------------------------------------------------
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'FIRTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'FIRSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=13,
        alignment=TA_CENTER
    )
    
    section_style = ParagraphStyle(
        'FIRSection',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        spaceBefore=8,
        spaceAfter=4
    )
    
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12
    )
    
    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12
    )
    
    narrative_style = ParagraphStyle(
        'FIRNarrative',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        alignment=TA_JUSTIFY
    )

    # Calculate precise horizontal boundaries (~180mm printable width)
    full_width = A4[0] - 30*mm 
    half_width = full_width / 2.0

    # Helper: section banners with light gray backgrounds
    def add_section(title_text):
        p = Paragraph(title_text, section_style)
        t = Table([[p]], colWidths=[full_width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F2F2F2')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            ('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
        ]))
        story.append(t)

    # Helper: dynamic layout tables
    def make_grid_table(data_list, col_widths=[140, 370]):
        formatted_data = []
        for row in data_list:
            lbl = Paragraph(row[0], cell_bold)
            val = Paragraph(row[1], cell_normal)
            formatted_data.append([lbl, val])
            
        t = Table(formatted_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#666666')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#FAFAFB'))
        ]))
        return t

    # -------------------------------------------------------------------------
    # Layout Assembly
    # -------------------------------------------------------------------------
    story.append(Paragraph("FIRST INFORMATION REPORT", title_style))
    story.append(Paragraph("(Under Section 154 Cr.P.C.)", subtitle_style))
    story.append(Spacer(1, 8))
    
    # Meta Block Header
    meta_data = [
        [Paragraph("<b>FIR No:</b> 2026/0482", cell_normal), Paragraph("<b>Date:</b> 01/07/2026", cell_normal)],
        [Paragraph("<b>Police Station:</b> Roorkee Civil Lines", cell_normal), Paragraph("<b>District:</b> Haridwar, Uttarakhand", cell_normal)]
    ]
    meta_table = Table(meta_data, colWidths=[half_width, half_width])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(meta_table)

    # 1. Applicable Laws
    add_section("1. Applicable Laws & Sections")
    law_data = [
        [Paragraph("<b>Acts / Code</b>", cell_bold), Paragraph("<b>Section(s)</b>", cell_bold)],
        [Paragraph("Bharatiya Nyaya Sanhita (BNS), 2023", cell_normal), Paragraph("Section 303(2) [Theft]", cell_normal)],
        [Paragraph("Other Acts / Special Laws", cell_normal), Paragraph("N/A", cell_normal)]
    ]
    law_table = Table(law_data, colWidths=[half_width, half_width])
    law_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6E6E6')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(law_table)

    # 2. Occurrence of Offence
    add_section("2. Occurrence of Offence")
    occ_data = [
        ["Date & Time Range", "Between 30/06/2026 22:00 Hrs and 01/07/2026 06:00 Hrs"],
        ["Date & Time Reported", "01/07/2026 at 09:30 Hrs"],
        ["Place of Occurrence", "House No. 42, Lane 3, Near IIT Roorkee Main Gate, Roorkee"]
    ]
    story.append(make_grid_table(occ_data))

    # 3. Complainant Information
    add_section("3. Complainant / Informant Information")
    comp_data = [
        ["Full Name", "Rajesh Kumar Sharma"],
        ["Father's Name", "Late S. K. Sharma"],
        ["Date of Birth / Age", "14/08/1982 (43 Years)"],
        ["Nationality / Occupation", "Indian / Senior Software Consultant"],
        ["Full Address", "House No. 42, Lane 3, Near IIT Roorkee Main Gate, Roorkee, Uttarakhand - 247667"]
    ]
    story.append(make_grid_table(comp_data))

    # 4. Accused Details
    add_section("4. Accused Details")
    acc_data = [["Suspect Information", "Two unknown individuals identified on peripheral surveillance footage; wearing dark hooded garments and full lowers/track pants. Specific identity untraceable at present."]]
    story.append(make_grid_table(acc_data))

    # 5. Delay in Reporting
    add_section("5. Delay in Reporting Offence")
    delay_data = [["Reasons for Delay", "Immediate reporting. Case registered without delay upon initial discovery and compilation of item details."]]
    story.append(make_grid_table(delay_data))

    # 6. Property Stolen
    add_section("6. Details of Properties Stolen / Involved")
    prop_data = [
        ["Description of Items", "1. 1x Customized 1/7 Scale PVC Commercial Character Figurine (Featuring specialized round transparent acrylic base with matching Bandai-style toy packaging box).<br/>2. 1x Enterprise Workstation Laptop Device."],
        ["Estimated Value", "INR 1,45,000/-"]
    ]
    story.append(make_grid_table(prop_data))

    # 7. FIR Narrative (The actual dynamic message data)
    add_section("7. FIR Contents / Analytical Narrative")
    story.append(Spacer(1, 2))
    story.append(Paragraph(content_text.replace('\n', '<br/>'), narrative_style))

    # 8. Action Taken
    add_section("8. Action Taken & Investigation Profile")
    action_data = [
        ["Case Registration", "Formally registered for active investigation under the designated legal sections."],
        ["Investigating Officer", "Sub-Inspector Amit Mukhopadhyay"],
        ["Rank & Credentials", "SI / Crime Prevention Unit - #UPL-99821"]
    ]
    story.append(make_grid_table(action_data))
    story.append(Spacer(1, 20))

    # Signatures Footer Box
    sig_data = [
        [Paragraph("..........................................................", title_style), Paragraph("..........................................................", title_style)],
        [Paragraph("<b>Signature of Complainant / Informant</b>", cell_bold), Paragraph("<b>Officer-in-Charge, Police Station</b>", cell_bold)],
        ["", Paragraph("Official Seal & Designation", cell_normal)]
    ]
    sig_table = Table(sig_data, colWidths=[half_width, half_width])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(sig_table)

    # Render Document securely
    doc.build(story)
    return output_path

generate_pdf(temp_summary,'FIR2.pdf')



