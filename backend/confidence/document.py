from backend.confidence.scorer import score_field


def score_document(result):

    scores = []

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