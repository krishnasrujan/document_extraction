import re

from rapidfuzz import fuzz


def normalize(value):
    if value is None:
        return ""

    return re.sub(
        r"[^a-z0-9]",
        "",
        str(value).lower()
    )


def align_value(field, tokens):
    value = normalize(field.value)
    label = normalize(field.name)

    if not value:
        return None

    best_score = 0
    best = None

    for start in range(len(tokens)):
        text = ""
        bbox = None
        confidences = []

        for end in range(start, min(start + 5, len(tokens))):
            token = tokens[end]

            text += token.text
            confidences.append(token.conf)

            bbox = (
                token.bbox
                if bbox is None
                else bbox.union(token.bbox)
            )

            ocr_text = normalize(text)

            value_score = fuzz.partial_ratio(
                value,
                ocr_text
            ) / 100

            label_score = fuzz.partial_ratio(
                label,
                ocr_text
            ) / 100

            score = (
                0.7 * value_score
                +
                0.3 * label_score
            )

            if score > best_score:
                best_score = score

                best = {
                    "bbox": bbox,
                    "ocr_conf": sum(confidences) / len(confidences),
                    "match_ratio": score,
                    "text": text
                }

    if best is None:
        return None

    return best