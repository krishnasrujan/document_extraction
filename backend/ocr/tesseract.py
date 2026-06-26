import pytesseract
from pytesseract import Output
from PIL import Image

from backend.models import Token, BBox
from backend.ocr.base import OCREngine

class TesseractEngine(OCREngine):

    def read(self, page):
        image = Image.open(page.path)

        data = pytesseract.image_to_data(
            image,
            output_type=Output.DICT
        )

        tokens = []

        for i, text in enumerate(data["text"]):
            text = text.strip()
            conf = float(data["conf"][i])

            if not text or conf < 0:
                continue

            tokens.append(
                Token(
                    text=text,
                    conf=conf / 100,
                    bbox=BBox(
                        x=data["left"][i],
                        y=data["top"][i],
                        w=data["width"][i],
                        h=data["height"][i],
                        page=page.index
                    )
                )
            )

        return tokens