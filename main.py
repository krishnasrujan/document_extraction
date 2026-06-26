import argparse

from backend.pipeline import Pipeline
from backend.ocr.tesseract import TesseractEngine
from backend.extract.vlm_extractor import VisionExtractor
from backend.confidence.scorer import ConfidenceScorer
from backend.confidence.router import route


def main():

    parser = argparse.ArgumentParser(
        description="Document extraction pipeline"
    )

    parser.add_argument(
        "file",
        help="path to document"
    )

    parser.add_argument(
        "--doc-id",
        default="document_001",
        help="document identifier"
    )

    args = parser.parse_args()


    pipeline = Pipeline(

        ocr_engine=TesseractEngine(),

        vlm_extractor=VisionExtractor(),

        confidence_engine=ConfidenceScorer()

    )


    result = pipeline.run(

        file_path=args.file,

        doc_id=args.doc_id

    )

    score = (
        pipeline.confidence_engine.document_score(
            result.fields
        )
    )


    decision = route(
        score
    )

    print("\nExtracted Fields:")

    for field in result.fields:

        print(
            {
                "name": field.name,
                "value": field.value,
                "confidence": (
                    field.confidence.raw
                    if field.confidence
                    else None
                )
            }
        )


    print("\nDocument Confidence:")
    print(score)


    print("\nDecision:")
    print(decision)


if __name__ == "__main__":

    main()