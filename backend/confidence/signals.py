from backend.align.aligner import align_value
from backend.validate.format import validate_money

def ocr_signal(field, tokens):
    aligned = align_value(
        field.value,
        tokens
    )

    if aligned is None:
        return {
            "name": "ocr_alignment",
            "score": 0.0,
            "weight": 0.4,
            "reason": "no OCR match"
        }

    return {
        "name": "ocr_alignment",
        "score": aligned["match_ratio"] * aligned["ocr_conf"],
        "weight": 0.4,
        "reason": "OCR value aligned"
    }


def format_signal(field):
    result = validate_money(
        field.value
    )

    return {
        "name": "format",
        "score": result["score"],
        "weight": 0.2,
        "reason": result["reason"]
    }


def extraction_signal(field):
    if field.value:
        return {
            "name": "extraction",
            "score": 1.0,
            "weight": 0.4,
            "reason": "value extracted"
        }

    return {
        "name": "extraction",
        "score": 0.0,
        "weight": 0.4,
        "reason": "missing value"
    }