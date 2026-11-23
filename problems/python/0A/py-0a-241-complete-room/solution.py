def shelve(locations: dict[str, int], title: str, shelf: int) -> dict[str, int]:
    locations[title] = shelf
    return locations
