def flatten(items: list):
    for item in items:
        if isinstance(item, list):
            ____
        else:
            yield item


def run_case(items: list, limit: int) -> list[int]:
    stream = flatten(items)
    values = []
    for _ in range(limit):
        value = next(stream, None)
        if value is None:
            break
        values.append(value)
    return values
