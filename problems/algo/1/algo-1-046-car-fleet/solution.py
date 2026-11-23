def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    fleets = 0
    latest = 0
    for start, rate in sorted(zip(position, speed), reverse=True):
        arrival = (target - start) / rate
        if arrival > latest:
            fleets += 1
            latest = arrival
    return fleets
