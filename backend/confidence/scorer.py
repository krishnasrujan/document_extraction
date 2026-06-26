from backend.models import FieldConfidence, SignalScore
from backend.confidence.signals import (
    ocr_signal,
    format_signal,
    extraction_signal
)


class ConfidenceScorer:

    def calculate(
        self,
        field,
        tokens
    ):

        signals = [
            ocr_signal(
                field,
                tokens
            ),
            extraction_signal(
                field
            ),
            format_signal(
                field
            )
        ]

        score = sum(
            signal["score"] *
            signal["weight"]
            for signal in signals
        )

        return FieldConfidence(
            raw=round(
                score,
                2
            ),
            signals=[
                SignalScore(
                    name=s["name"],
                    score=s["score"],
                    weight=s["weight"],
                    reason=s["reason"]
                )
                for s in signals
            ]
        )


    def document_score(
        self,
        fields
    ):

        scores = []

        for field in fields:

            if field.confidence:
                scores.append(
                    field.confidence.raw
                )

        if not scores:
            return 0

        return round(
            sum(scores) / len(scores),
            2
        )