import argparse

from backend.pipeline import Pipeline
from backend.ocr.tesseract import TesseractEngine
from backend.extract.openai_vlm import OpenAIVisionExtractor
from backend.confidence.document import score_document
from backend.confidence.router import route


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file",
        help="path to invoice document"
    )

    args = parser.parse_args()

    pipeline = Pipeline(
        ocr_engine=TesseractEngine(),
        extractor=OpenAIVisionExtractor()
    )

    result = pipeline.run(
        file_path=args.file,
        doc_id="document_001"
    )

    score = score_document(
        result
    )

    decision = route(
        score
    )

    print(
        decision
    )


if __name__ == "__main__":
    main()