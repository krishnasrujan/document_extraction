import base64

import ollama

from backend.models import ExtractedField
from backend.extract.json_utils import extract_json
from backend.extract.flatten import flatten_entities


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


class VisionExtractor:
    def extract_fields(self, pages):
        prompt = """
You are a document understanding system.

Analyze the given document image.

Identify:

1. Document type
2. All important entities

Return ONLY valid JSON.

Format:

{
 "document_type": "",
 "entities": {
    "field": "value"
 }
}

Rules:

- Do not guess values
- Extract only visible information
- Preserve exact text
- Do not normalize values
- If missing, do not include
"""

        images = [
            encode_image(page.path)
            for page in pages
        ]

        response = ollama.chat(
            model="qwen2.5vl:7b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": images
                }
            ],
            options={
                "temperature": 0
            }
        )

        output = response["message"]["content"]

        data = extract_json(output)

        entities = data.get("entities", {})

        flattened = flatten_entities(entities)

        return [
            ExtractedField(
                name=field["name"],
                value=field["value"]
            )
            for field in flattened
        ]