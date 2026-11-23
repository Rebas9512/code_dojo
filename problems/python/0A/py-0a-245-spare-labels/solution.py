def badges(names: list[str], nicknames: dict[str, str]) -> list[str]:
    result = []
    for name in names:
        result.append(nicknames.get(name, name))
    return result
