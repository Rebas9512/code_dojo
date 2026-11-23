def roster(ids: list[int], new_id: int) -> list[list[int]]:
    before = ids.copy()
    ids.append(new_id)
    return [before, ids]
