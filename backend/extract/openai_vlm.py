import base64
from openai import OpenAI

from backend.config import settings
from backend.models import ExtractedField
from backend.extract.base import Extractor
from backend.extract.json_utils import extract_json

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(
            f.read()
        ).decode()

class OpenAIVisionExtractor(Extractor):

    def extract(self, pages):

        prompt = """
Extract invoice fields.

Return JSON only:

{
"invoice_number":"",
"invoice_date":"",
"vendor_name":"",
"subtotal":"",
"tax":"",
"total":"",
"currency":""
}

Do not guess.
Copy exactly.
"""

        content = [
            {
                "type": "text",
                "text": prompt
            }
        ]

        for page in pages:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image(page.path)}"
                    }
                }
            )

        response = client.chat.completions.create(
            model=settings.VISION_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        data = extract_json(
            response.choices[0].message.content
        )

        fields = []

        for key, value in data.items():
            fields.append(
                ExtractedField(
                    name=key,
                    value=value
                )
            )

        return fields