import logging

from backend.ingest.loader import load_pages
from backend.models import ExtractionResult


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(
        self,
        ocr_engine,
        vlm_extractor,
        confidence_engine
    ):
        self.ocr_engine = ocr_engine
        self.vlm_extractor = vlm_extractor
        self.confidence_engine = confidence_engine

    def run(self, file_path, doc_id):
        logger.info(f"Processing document: {doc_id}")

        pages = load_pages(
            file_path,
            "artifacts"
        )

        logger.info(f"Total pages: {len(pages)}")

        tokens = []

        for page in pages:
            logger.info(f"Running OCR for page {page.index}")

            page_tokens = self.ocr_engine.read(page)

            logger.info(
                f"OCR tokens extracted: {len(page_tokens)}"
            )

            print(f"\nOCR OUTPUT - PAGE {page.index}")
            print("----------------------")

            for token in page_tokens:
                print(token.text)

            tokens.extend(page_tokens)

        logger.info("Running VLM extraction")

        fields = self.vlm_extractor.extract_fields(pages)

        print("\nVLM OUTPUT")
        print("----------------------")

        for field in fields:
            print(f"{field.name}: {field.value}")

        logger.info(
            f"VLM fields extracted: {len(fields)}"
        )

        logger.info("Calculating confidence")

        for field in fields:
            confidence = self.confidence_engine.calculate(
                field,
                tokens
            )

            field.confidence = confidence

            print("\nCONFIDENCE")
            print("----------------------")
            print(f"Field: {field.name}")
            print(f"Value: {field.value}")
            print(f"Score: {confidence.raw}")

            for signal in confidence.signals:
                print(
                    f"""
                    Signal: {signal.name}
                    Score: {signal.score}
                    Reason: {signal.reason}
                    """
                )

        return ExtractionResult(
            doc_id=doc_id,
            pages=pages,
            tokens=tokens,
            fields=fields
        )