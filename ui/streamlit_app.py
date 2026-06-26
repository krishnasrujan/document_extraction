import streamlit as st

from backend.pipeline import Pipeline
from backend.ocr.tesseract import TesseractEngine
from backend.extract.lm_extractor import OpenAIVisionExtractor

from backend.confidence.document import score_document
from backend.confidence.router import route


st.set_page_config(
    page_title="Document Confidence Scoring",
    layout="wide"
)

st.title(
    "Invoice Extraction Confidence Scoring"
)


uploaded_file = st.file_uploader(
    "Upload invoice",
    type=[
        "pdf",
        "png",
        "jpg"
    ]
)


if uploaded_file:

    path = f"artifacts/{uploaded_file.name}"

    with open(path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )


    pipeline = Pipeline(
        ocr_engine=TesseractEngine(),
        llm_extractor=OpenAIVisionExtractor()
    )


    result = pipeline.run(
        file_path=path,
        doc_id=uploaded_file.name
    )


    confidence = score_document(
        result
    )


    decision = route(
        confidence
    )


    st.subheader(
        "Extracted Fields"
    )

    for field in result.fields:

        st.write(
            field.name,
            field.value
        )


    st.subheader(
        "Confidence"
    )

    st.metric(
        "Document Score",
        round(confidence, 3)
    )


    st.subheader(
        "Decision"
    )

    st.write(
        decision.action.value
    )