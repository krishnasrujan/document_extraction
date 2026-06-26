from backend.ingest.loader import load_pages
from backend.models import ExtractionResult

class Pipeline:
    def __init__(self, ocr_engine, lm_extractor):
        self.ocr_engine = ocr_engine
        self.lm_extractor = lm_extractor

    def run(self, file_path, doc_id):

        pages = load_pages(
            file_path,
            "artifacts"
        )

        combined_ocr_tokens = []
        for page in pages:
            combined_ocr_tokens.extend(
                self.ocr_engine.read(page)
            )

        lm_extracted_fields = self.lm_extractor.extract_fields(
            pages
        )

        return ExtractionResult(
            doc_id=doc_id,
            pages=pages,
            tokens=combined_ocr_tokens,
            fields=lm_extracted_fields
        )