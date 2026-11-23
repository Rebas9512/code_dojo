def stop_count(route: list[int]) -> int:
    seen = set()
    for stop in route:
        seen.add(stop)
    return len(seen)
