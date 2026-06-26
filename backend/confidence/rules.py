import re


def validate_invoice_number(value):
    if not value:
        return 0

    pattern = r"^[A-Z0-9-]+$"

    return 1 if re.match(pattern, value) else 0.3


def validate_currency(value):
    allowed = [
        "USD",
        "INR",
        "EUR"
    ]

    return 1 if value in allowed else 0.5


def validate_total(value):
    if not value:
        return 0

    try:
        float(
            value.replace(",", "")
        )
        return 1
    except:
        return 0.3


def validate_field(field):
    if field.name == "invoice_number":
        return validate_invoice_number(
            field.value
        )

    if field.name == "currency":
        return validate_currency(
            field.value
        )

    if field.name == "total":
        return validate_total(
            field.value
        )

    return 0.8 if field.value else 0