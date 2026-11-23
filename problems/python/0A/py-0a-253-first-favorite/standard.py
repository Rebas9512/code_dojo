def favorite(log: list[str]) -> str:
    counts = {}
    for song in log:
        counts[song] = counts.get(song, 0) + 1
    best = ""
    maximum = 0
    for song, count in counts.items():
        if count > maximum:
            best = song
            maximum = count
    return best
