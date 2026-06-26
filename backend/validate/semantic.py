def validate_total(subtotal, tax, total):
    subtotal = float(subtotal)
    tax = float(tax)
    total = float(total)

    if abs(subtotal + tax - total) < 0.01:
        return {
            "score": 1.0,
            "reason": "subtotal + tax matches total"
        }

    return {
        "score": 0.0,
        "reason": "total mismatch"
    }