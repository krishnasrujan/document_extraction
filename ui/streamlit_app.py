import streamlit as st

from backend.pipeline import Pipeline
from backend.ocr.tesseract import TesseractEngine
from backend.extract.vlm_extractor import VisionExtractor
from backend.confidence.scorer import ConfidenceScorer
from backend.confidence.router import route


st.set_page_config(page_title="Document Confidence Scoring", layout="wide")

st.title("Document Extraction Confidence Scoring")

uploaded_file = st.file_uploader(
    "Upload document",
    type=["pdf", "png", "jpg", "jpeg"]
)


if uploaded_file:
    path = f"artifacts/{uploaded_file.name}"

    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    pipeline = Pipeline(
        ocr_engine=TesseractEngine(),
        vlm_extractor=VisionExtractor(),
        confidence_engine=ConfidenceScorer()
    )

    result = pipeline.run(
        file_path=path,
        doc_id=uploaded_file.name
    )

    document_score = pipeline.confidence_engine.document_score(
        result.fields
    )

    decision = route(document_score)

    st.subheader("Extracted Fields")

    for field in result.fields:
        confidence = field.confidence.raw if field.confidence else 0

        with st.expander(field.name):
            if isinstance(field.value, dict):
                st.json(field.value)
            elif isinstance(field.value, list):
                st.write(field.value)
            else:
                st.write(field.value)

            st.metric("Confidence", round(confidence, 3))

            if field.confidence:
                st.write("Signals")

                for signal in field.confidence.signals:
                    st.write({
                        "name": signal.name,
                        "score": signal.score,
                        "weight": signal.weight,
                        "reason": signal.reason
                    })

    st.subheader("Document Confidence")
    confidence_col, decision_col = st.columns(2)
    with confidence_col:
        st.metric(
            "Overall Score",
            f"{document_score:.2f}"
        )
    with decision_col:
        st.metric(
            "Routing Decision",
            decision.action.value.title()
        )
    st.divider()
    st.subheader("Decision Details")
    st.info(
        decision.reasons[0]
    )