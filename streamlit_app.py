import os
from uuid import uuid4
from pathlib import Path

import streamlit as st

from app.services.extraction import extract_information
from app.services.analysis import get_relevant_data
from app.services.fir_service import generate_fir
from app.services.pdf_service import generate_pdf
from app.utils.helpers import get_missing_fields,clean_fir_text,get_message_text
from app.schemas.user_report import UserReportSchema
from langchain_core.messages import AIMessage


st.set_page_config(
    page_title="FIR Generator",
    page_icon="📄",
    layout="centered"
)


FIELD_LABELS = {
    "offence_description": "Offence Description",
    "offence_date": "Offence Date",
    "offence_time": "Offence Time",
    "location_name": "Location Name",
    "landmark": "Landmark",
    "city": "City",
    "state": "State",
    "reporter_full_name": "Reporter Full Name",
    "father_or_husband_name": "Father's / Husband's Name",
    "dob": "Date of Birth",
    "nationality": "Nationality",
    "occupation": "Occupation",
    "address": "Address",
    "phone_number": "Phone Number",
    "delay_reason": "Reason for Delay",
    "accused_description": "Accused Description",
    "property_type": "Property Type",
    # "estimated_value": "Estimated Value",
}


def update_report(report: UserReportSchema, updates: dict) -> UserReportSchema:
    data = report.model_dump()
    data.update(updates)
    return UserReportSchema(**data)


st.title("📄 FIR Generator")
st.caption("Generate FIR draft using extraction, legal analysis, FIR generation, and PDF service.")

if "report" not in st.session_state:
    st.session_state.report = None

if "legal_analysis" not in st.session_state:
    st.session_state.legal_analysis = None

if "fir" not in st.session_state:
    st.session_state.fir = None

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None


story = st.text_area(
    "Enter complaint story",
    height=280,
    placeholder="Describe what happened, when, where, property involved, accused details, delay reason, etc."
)

if st.button("Extract Information"):
    if not story.strip():
        st.warning("Please enter the complaint story first.")
    else:
        with st.spinner("Extracting information..."):
            st.session_state.report = extract_information(story)
            st.session_state.legal_analysis = None
            st.session_state.fir = None
            st.session_state.pdf_bytes = None

if st.session_state.report:
    st.subheader("Extracted Report")

    report = st.session_state.report
    st.json(report.model_dump())

    missing_fields = get_missing_fields(report)

    if missing_fields:
        current_field = missing_fields[0]

        label = FIELD_LABELS.get(
            current_field,
            current_field.replace("_", " ").title()
        )

        st.warning(f"Missing information: {label}")

        with st.form("single_missing_field_form"):
            value = st.text_input(label)

            submitted = st.form_submit_button("Save and Continue")

            if submitted:
                if not value.strip():
                    st.warning("Please enter a value before continuing.")
                else:
                    st.session_state.report = update_report(
                        report,
                        {
                            current_field: value.strip()
                        }
                    )
                    st.rerun()
    else:
        st.success("Report is complete.")

        if st.button("Generate Legal Analysis"):
            with st.spinner("Retrieving legal sections and analysing..."):
                st.session_state.legal_analysis = get_relevant_data(st.session_state.report)

        if st.session_state.legal_analysis:
            st.subheader("Legal Analysis")
            st.text(get_message_text(st.session_state.legal_analysis))

            if st.button("Generate FIR Draft"):
                with st.spinner("Generating FIR draft..."):
                    #f
                    fir = generate_fir({
                        "report": st.session_state.report,
                        "legal_context": st.session_state.legal_analysis
                    })
                    fir_text=get_message_text(fir)
                    fir_text=clean_fir_text(fir_text)

                    fir = AIMessage(content = fir_text)
                    st.session_state.fir = fir

        if st.session_state.fir:
            st.subheader("Generated FIR")
            st.text(get_message_text(st.session_state.fir))

            if st.button("Generate PDF"):
                with st.spinner("Generating PDF..."):
                    filename = f"fir_{uuid4().hex}.pdf"

                    pdf_path = generate_pdf(
                        st.session_state.report,
                        st.session_state.legal_analysis,
                        st.session_state.fir,
                        filename
                    )

                    with open(pdf_path, "rb") as file:
                        st.session_state.pdf_bytes = file.read()

                    # temporary file cleanup
                    Path(pdf_path).unlink(missing_ok=True)

        if st.session_state.pdf_bytes:
            st.download_button(
                label="Download FIR PDF",
                data=st.session_state.pdf_bytes,
                file_name="fir.pdf",
                mime="application/pdf"
            )


