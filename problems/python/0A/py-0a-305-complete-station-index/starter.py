def latest(rows: list[list[str]], station: str) -> str:
    trains = ____
    for name, train in rows:
        trains[name] = train
    return trains.get(station, "")
