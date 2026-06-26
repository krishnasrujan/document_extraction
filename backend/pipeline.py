from backend.ingest.loader import load_pages
from backend.ocr.tesseract import TesseractEngine
from backend.extract.openai_vlm import OpenAIVisionExtractor
from backend.models import ExtractionResult

class Pipeline:
    def __init__(self, ocr_engine, extractor):
        self.ocr_engine = ocr_engine
        self.extractor = extractor

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

        fields = self.extractor.extract(
            pages
        )

        return ExtractionResult(
            doc_id=doc_id,
            pages=pages,
            tokens=tokens,
            fields=fields
        )