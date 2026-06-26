import json

def extract_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == 0:
        raise ValueError(
            "No JSON found"
        )

    return json.loads(
        text[start:end]
    )