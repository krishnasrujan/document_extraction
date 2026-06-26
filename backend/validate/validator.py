from backend.validate.format import validate_money
from backend.validate.semantic import validate_total

def validate_fields(fields):
    results = []

    field_map = {
        field.name: field.value
        for field in fields
    }

    for name, value in field_map.items():

        if name in [
            "subtotal",
            "tax",
            "total"
        ]:
            results.append(
                validate_money(value)
            )

    if all(
        key in field_map
        for key in [
            "subtotal",
            "tax",
            "total"
        ]
    ):
        results.append(
            validate_total(
                field_map["subtotal"],
                field_map["tax"],
                field_map["total"]
            )
        )

    return results