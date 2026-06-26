from backend.confidence.signals import (
    ocr_signal,
    format_signal,
    extraction_signal
)

from backend.confidence.aggregator import weighted_geometric_mean


def score_field(field, tokens):

    signals = [
        extraction_signal(field),
        ocr_signal(field, tokens),
    ]

    if field.name in [
        "subtotal",
        "tax",
        "total"
    ]:
        signals.append(
            format_signal(field)
        )

    score = weighted_geometric_mean(
        signals
    )

    return {
        "score": score,
        "signals": signals
    }