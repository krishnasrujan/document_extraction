import re
from decimal import Decimal

def parse_money(value):
    try:
        value = re.sub(
            r"[^\d.-]",
            "",
            value
        )

        return Decimal(value)

    except Exception:
        return None

def validate_money(value):
    amount = parse_money(value)

    if amount is None:
        return {
            "score": 0.1,
            "reason": "invalid money format"
        }

    return {
        "score": 1.0,
        "reason": "valid money format"
    }