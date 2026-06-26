from backend.ingest.loader import load_pages
from backend.models import ExtractionResult


class Pipeline:

    def __init__(
        self,
        ocr_engine,
        lm_extractor,
        confidence_engine
    ):
        self.ocr_engine = ocr_engine
        self.lm_extractor = lm_extractor
        self.confidence_engine = confidence_engine


    def run(self, file_path, doc_id):

        pages = load_pages(
            file_path,
            "artifacts"
        )

        tokens = []

        for page in pages:
            tokens.extend(
                self.ocr_engine.read(page)
            )

        fields = self.lm_extractor.extract_fields(
            pages
        )

        for field in fields:
            field.confidence = (
                self.confidence_engine.calculate(
                    field,
                    tokens
                )
            )

        return ExtractionResult(
            doc_id=doc_id,
            pages=pages,
            tokens=tokens,
            fields=fields
        )