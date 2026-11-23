def latest(rows: list[list[str]], station: str) -> str:
    trains = {}
    for name, train in rows:
        trains[name] = train
    return trains.get(station, "")
