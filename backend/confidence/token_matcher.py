import re
from difflib import SequenceMatcher


def normalize(value):

    if value is None:
        return ""

    if not isinstance(value,str):
        value=str(value)

    return re.sub(
        r"\s+",
        "",
        value.lower()
    )


def is_near(field_bbox, token_bbox):
    if not field_bbox:
        return True

    distance = abs(
        field_bbox.y - token_bbox.y
    )

    return distance < 100


def find_matching_tokens(field, tokens):
    matches = []

    if not field.value:
        return matches

    target = normalize(
        field.value
    )

    for token in tokens:

        if field.page is not None:
            if token.bbox.page != field.page:
                continue

        if not is_near(
            field.bbox,
            token.bbox
        ):
            continue

        score = SequenceMatcher(
            None,
            target,
            normalize(token.text)
        ).ratio()

        if score >= 0.8:
            matches.append(token)

    return matches