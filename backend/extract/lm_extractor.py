import base64
import ollama

from backend.models import ExtractedField
from backend.extract.json_utils import extract_json


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(
            f.read()
        ).decode()


class VisionExtractor:

    def extract_fields(self, pages):

        prompt = """
Extract invoice fields.

Return ONLY valid JSON.

Schema:

{
"invoice_number":"",
"invoice_date":"",
"vendor_name":"",
"subtotal":"",
"tax":"",
"total":"",
"currency":""
}

Rules:

- Do not guess
- Copy values exactly
- If missing return empty string
"""
        images = []
        for page in pages:
            images.append(
                encode_image(page.path)
            )

        response = ollama.chat(
            model="qwen2.5-vl:7b",
            messages=[
                {
                    "role":"user",
                    "content":prompt,
                    "images":images
                }
            ],
            options={
                "temperature":0
            }
        )
        output = response["message"]["content"]
        data = extract_json(output)

        fields=[]
        for key,value in data.items():
            fields.append(
                ExtractedField(
                    name=key,
                    value=value
                )
            )
        return fields