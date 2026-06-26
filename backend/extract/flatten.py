def flatten_entities(data, parent=""):
    fields = []

    for key, value in data.items():
        field_name = f"{parent}.{key}" if parent else key

        if isinstance(value, dict):
            fields.extend(flatten_entities(value, field_name))

        elif isinstance(value, list):
            for index, item in enumerate(value):
                item_name = f"{field_name}[{index}]"

                if isinstance(item, dict):
                    fields.extend(flatten_entities(item, item_name))
                else:
                    fields.append({
                        "name": item_name,
                        "value": item
                    })

        else:
            fields.append({
                "name": field_name,
                "value": value
            })

    return fields