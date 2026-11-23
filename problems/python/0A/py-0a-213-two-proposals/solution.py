def proposals(songs: list[str], a: str, b: str) -> list[list[str]]:
    first = songs.copy()
    second = songs.copy()
    first.append(a)
    second.append(b)
    return [songs, first, second]
