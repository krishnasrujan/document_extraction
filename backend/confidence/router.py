from backend.models import RoutingAction, RoutingDecision


def route(document_score):

    if document_score >= 0.85:
        return RoutingDecision(
            action=RoutingAction.AUTO_APPROVE,
            doc_score=document_score,
            reasons=[
                "high confidence"
            ]
        )

    if document_score < 0.50:
        return RoutingDecision(
            action=RoutingAction.REJECT,
            doc_score=document_score,
            reasons=[
                "low confidence"
            ]
        )

    return RoutingDecision(
        action=RoutingAction.REVIEW,
        doc_score=document_score,
        reasons=[
            "manual review required"
        ]
    )