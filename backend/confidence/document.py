from backend.confidence.scorer import score_field


def score_document(result):

    scores = []

    # a field is the entity extracted by an LM. We need to score the extraction
    # we use all the
    for field in result.fields:
        output = score_field(
            field,
            result.tokens
        )

        field.confidence = output

        scores.append(
            output["score"]
        )

    if not scores:
        return 0.0

    return sum(scores) / len(scores)